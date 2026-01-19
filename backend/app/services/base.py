from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas import IssueCreate, IssueRead, SearchResult


class EmbeddingService(ABC):
    """Abstract interface for embedding generation."""

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Convert text into a vector embedding."""
        pass


class VectorStoreService(ABC):
    """Abstract interface for vector storage and retrieval."""

    @abstractmethod
    async def save_issue(self, issue: IssueCreate, embedding: List[float]) -> IssueRead:
        """Save an issue with its embedding."""
        pass

    @abstractmethod
    async def search(
        self,
        query_embedding: List[float],
        limit: int = 5,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[SearchResult]:
        """Search for similar issues using vector similarity."""
        pass

    @abstractmethod
    async def get_trending(self, limit: int = 10) -> List[IssueRead]:
        """Get trending issues."""
        pass

    @abstractmethod
    async def increment_counter(self, issue_id: str, counter_type: str):
        """Increment view or useful counter."""
        pass
