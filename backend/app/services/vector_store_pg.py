from typing import List, Dict, Any, Optional, Generator
from datetime import datetime, timezone, timedelta
from app.services.base import VectorStoreService, EmbeddingService
from app.schemas import IssueCreate, IssueRead, SearchResult
from app.models import IssueModel, Base
from sqlalchemy import create_engine, select, text, desc, func
from sqlalchemy.orm import sessionmaker, Session


class PostgresVectorStore(VectorStoreService):
    """
    Postgres implementation using pgvector.
    """

    def __init__(self, database_url: str):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=self.engine
        )

        # Ensure tables and extension exist
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
            existing_issue = (
                db.query(IssueModel).filter(IssueModel.title == issue.title).first()
            )

            if existing_issue:
                return self._to_schema(existing_issue)

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

            return self._to_schema(db_issue)
        finally:
            db.close()

    async def get_issue(self, issue_id: str) -> Optional[IssueRead]:
        db = self.SessionLocal()
        try:
            db_issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
            if not db_issue:
                return None
            return self._to_schema(db_issue)
        finally:
            db.close()

    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        db = self.SessionLocal()
        try:
            similarity = 1 - IssueModel.embedding.cosine_distance(query_embedding)

            # Popularity Log Factor: ln(views + useful*10 + 1)
            # This ensures popularity boost is significant but not overwhelming (logarithmic)
            # useful_count is weighted 10x higher than view_count as a quality signal
            popularity_factor = func.ln(
                func.coalesce(IssueModel.view_count, 0)
                + (func.coalesce(IssueModel.useful_count, 0) * 10)
                + 1
            )

            # Final Score = Similarity * (1 + 0.1 * Popularity)
            # 0.1 coefficient ensures vector similarity remains the primary ranking factor
            final_score = similarity * (1 + 0.1 * popularity_factor)

            stmt = (
                select(
                    IssueModel,
                    IssueModel.embedding.cosine_distance(query_embedding).label(
                        "distance"
                    ),
                    final_score.label("hybrid_score"),
                )
                .order_by(final_score.desc())
                .limit(limit)
            )

            if filters:
                for key, value in filters.items():
                    stmt = stmt.where(IssueModel.metadata_[key].astext == str(value))

            results = db.execute(stmt).all()

            search_results = []
            for row in results:
                issue = row[0]
                distance = row[1]
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
                        view_count=issue.view_count or 0,
                        useful_count=issue.useful_count or 0,
                        score=score,
                    )
                )

            return search_results
        finally:
            db.close()

    async def get_trending(self, limit: int = 10) -> List[IssueRead]:
        """
        Get trending issues based on Recency and Popularity.
        Score = (view_count + useful_count * 5) / (age_in_hours + 2)^1.5
        """
        db = self.SessionLocal()
        try:
            now = func.now()

            age_in_hours = func.extract("epoch", now - IssueModel.created_at) / 3600

            popularity = func.coalesce(IssueModel.view_count, 0) + (
                func.coalesce(IssueModel.useful_count, 0) * 5
            )

            score = (popularity + 1) / func.power(age_in_hours + 2, 1.5)

            stmt = select(IssueModel).order_by(score.desc()).limit(limit)

            results = db.execute(stmt).scalars().all()
            return [self._to_schema(issue) for issue in results]
        finally:
            db.close()

    async def increment_counter(self, issue_id: str, counter_type: str):
        db = self.SessionLocal()
        try:
            issue = db.query(IssueModel).filter(IssueModel.id == issue_id).first()
            if issue:
                if counter_type == "view":
                    issue.view_count = (issue.view_count or 0) + 1
                elif counter_type == "useful":
                    issue.useful_count = (issue.useful_count or 0) + 1
                db.commit()
        finally:
            db.close()

    def _to_schema(self, db_issue: IssueModel) -> IssueRead:
        return IssueRead(
            id=db_issue.id,
            title=db_issue.title,
            content=db_issue.content,
            solution=db_issue.solution,
            tags=db_issue.tags,
            metadata=db_issue.metadata_,
            created_at=db_issue.created_at,
            updated_at=db_issue.updated_at,
            view_count=db_issue.view_count or 0,
            useful_count=db_issue.useful_count or 0,
        )
