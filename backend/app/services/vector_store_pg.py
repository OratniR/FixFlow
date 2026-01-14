from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional, Dict, Any, Generator
from app.services.base import VectorStoreService
from app.schemas import IssueCreate, IssueRead, SearchResult
from app.models import IssueModel, Base


class PostgresVectorStore(VectorStoreService):
    """
    Postgres implementation using pgvector.
    """

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

        # Ensure tables and extension exist
        # NOTE: In production, use Alembic migrations.
        # This is strictly for MVP/Development speed.
        with self.engine.connect() as conn:
            conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            conn.commit()

        Base.metadata.create_all(bind=self.engine)

    def _get_db(self) -> Generator[Session, None, None]:
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def save_issue(self, issue: IssueCreate, embedding: List[float]) -> IssueRead:
        db = self.SessionLocal()
        try:
            db_issue = IssueModel(
                title=issue.title,
                content=issue.content,
                solution=issue.solution,
                tags=issue.tags,
                metadata_=issue.metadata,
                embedding=embedding,
            )
            db.add(db_issue)
            db.commit()
            db.refresh(db_issue)

            return IssueRead(
                id=db_issue.id,
                title=db_issue.title,
                content=db_issue.content,
                solution=db_issue.solution,
                tags=db_issue.tags,
                metadata=db_issue.metadata_,
                created_at=db_issue.created_at,
                updated_at=db_issue.updated_at,
            )
        finally:
            db.close()

    async def get_issue(self, issue_id: str) -> Optional[IssueRead]:
        db = self.SessionLocal()
        try:
            db_issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
            if not db_issue:
                return None

            return IssueRead(
                id=db_issue.id,
                title=db_issue.title,
                content=db_issue.content,
                solution=db_issue.solution,
                tags=db_issue.tags,
                metadata=db_issue.metadata_,
                created_at=db_issue.created_at,
                updated_at=db_issue.updated_at,
            )
        finally:
            db.close()

    async def search(
        self, query_embedding: List[float], limit: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        db = self.SessionLocal()
        try:
            # L2 distance search (closest distance) using pgvector's <=> operator
            # We want cosine similarity, which is 1 - cosine distance.
            # pgvector's cosine distance operator is <=>
            # Order by distance ASC = most similar

            stmt = (
                select(
                    IssueModel,
                    IssueModel.embedding.cosine_distance(query_embedding).label("distance"),
                )
                .order_by(IssueModel.embedding.cosine_distance(query_embedding))
                .limit(limit)
            )

            results = db.execute(stmt).all()

            search_results = []
            for row in results:
                issue = row[0]
                distance = row[1]
                # Convert distance back to similarity score (0 to 1) roughly
                score = 1 - distance

                search_results.append(
                    SearchResult(
                        id=issue.id,
                        title=issue.title,
                        content=issue.content,
                        solution=issue.solution,
                        tags=issue.tags,
                        metadata=issue.metadata_,
                        created_at=issue.created_at,
                        updated_at=issue.updated_at,
                        score=score,
                    )
                )

            return search_results
        finally:
            db.close()
