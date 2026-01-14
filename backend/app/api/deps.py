import os
from typing import Optional
from app.services.base import VectorStoreService, EmbeddingService
from app.services.embedding import MockEmbeddingService
from app.services.vector_store import InMemoryVectorStore
from app.services.vector_store_pg import PostgresVectorStore

# Configuration
USE_LOCAL_EMBEDDING = os.getenv("USE_LOCAL_EMBEDDING", "true").lower() == "true"
DATABASE_URL = os.getenv("DATABASE_URL")

# Singleton instances
_embedding_service: Optional[EmbeddingService] = None
_vector_store: Optional[VectorStoreService] = None


def get_embedding_service() -> EmbeddingService:
    """Dependency to get the embedding service."""
    global _embedding_service
    if _embedding_service is None:
        if USE_LOCAL_EMBEDDING:
            # Lazy import to avoid loading heavy dependencies (torch) if not needed
            from app.services.embedding_local import LocalEmbeddingService

            # This loads the model into memory (approx 100MB for MiniLM)
            _embedding_service = LocalEmbeddingService()
        else:
            _embedding_service = MockEmbeddingService()
    return _embedding_service


def get_vector_service() -> VectorStoreService:
    """Dependency to get the vector store service."""
    global _vector_store
    if _vector_store is None:
        if DATABASE_URL:
            # Use Postgres if configured
            _vector_store = PostgresVectorStore(DATABASE_URL)
        else:
            # Fallback to in-memory
            _vector_store = InMemoryVectorStore()
    return _vector_store
