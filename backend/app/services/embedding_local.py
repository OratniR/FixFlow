from typing import List

try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    SentenceTransformer = None

from app.services.base import EmbeddingService


class LocalEmbeddingService(EmbeddingService):
    """
    Local embedding implementation using SentenceTransformers.
    Defaults to 'all-MiniLM-L6-v2' which produces 384d vectors.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        if SentenceTransformer is None:
            raise ImportError(
                "sentence-transformers is not installed. Please install it to use LocalEmbeddingService."
            )
        # This will download the model on first run
        # Force device='cpu' to prevent meta tensor errors on some environments
        self.model = SentenceTransformer(model_name, device="cpu")

    async def embed_text(self, text: str) -> List[float]:
        """Convert text into a vector embedding using local model."""
        # encode returns numpy array, convert to list
        embedding = self.model.encode(text)
        return embedding.tolist()
