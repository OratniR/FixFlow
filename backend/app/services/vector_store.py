from typing import List, Optional, Dict, Any
from app.services.base import VectorStoreService, EmbeddingService
from app.schemas import IssueCreate, IssueRead, SearchResult


class InMemoryVectorStore(VectorStoreService):
    """In-memory implementation."""

    def __init__(self):
        self._store: Dict[str, Dict[str, Any]] = {}

    async def save_issue(self, issue: IssueCreate, embedding: List[float]) -> IssueRead:
        # Mock impl
        pass

    async def get_issue(self, issue_id: str) -> Optional[IssueRead]:
        # Mock impl
        pass

    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        # Mock impl
        return []

    async def get_trending(self, limit: int = 10) -> List[IssueRead]:
        return []

    async def increment_counter(self, issue_id: str, counter_type: str):
        pass
