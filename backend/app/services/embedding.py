import random
from typing import List
from app.services.base import EmbeddingService


class MockEmbeddingService(EmbeddingService):
    """Mock implementation of embedding service for testing."""

    def __init__(self, dimension: int = 384):
        self.dimension = dimension

    async def embed_text(self, text: str) -> List[float]:
        """Return a random vector of the specified dimension."""
        # Simulate latency? No need for mock.
        return [random.random() for _ in range(self.dimension)]


class OpenAIEmbeddingService(EmbeddingService):
    """Real implementation using OpenAI API."""

    # TODO: Implement with actual OpenAI client
    pass
