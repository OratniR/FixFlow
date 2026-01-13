import uuid
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from app.schemas import IssueCreate, IssueRead, SearchResult
from app.services.base import VectorStoreService


class InMemoryVectorStore(VectorStoreService):
    """
    In-memory implementation of VectorStoreService for testing/MVP.
    Stores issues in a dict and performs naive linear scan for search.
    """

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    async def save_issue(self, issue: IssueCreate, embedding: List[float]) -> IssueRead:
        issue_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc)

        issue_data = issue.model_dump()
        stored_item = {
            "id": issue_id,
            "created_at": now,
            "updated_at": now,
            **issue_data,
            "embedding": embedding,
        }

        self._store[issue_id] = stored_item

        return IssueRead(id=issue_id, created_at=now, updated_at=now, **issue_data)

    async def get_issue(self, issue_id: str) -> Optional[IssueRead]:
        data = self._store.get(issue_id)
        if not data:
            return None

        # Exclude embedding from read model
        read_data = {k: v for k, v in data.items() if k != "embedding"}
        return IssueRead(**read_data)

    async def search(
        self, query_embedding: List[float], limit: int = 5, filters: Optional[Dict[str, Any]] = None
    ) -> List[SearchResult]:
        if not self._store:
            return []

        # Naive cosine similarity
        results = []
        for issue_id, data in self._store.items():
            # TODO: filters support

            vec = data["embedding"]
            score = self._cosine_similarity(query_embedding, vec)

            read_data = {k: v for k, v in data.items() if k != "embedding"}
            results.append(SearchResult(**read_data, score=score))

        # Sort by score desc
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:limit]

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm_v1 = sum(a * a for a in v1) ** 0.5
        norm_v2 = sum(b * b for b in v2) ** 0.5
        if norm_v1 == 0 or norm_v2 == 0:
            return 0.0
        return dot_product / (norm_v1 * norm_v2)
