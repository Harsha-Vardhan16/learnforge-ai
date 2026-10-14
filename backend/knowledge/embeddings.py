import numpy as np
import logging
from typing import List, Union

logger = logging.getLogger("learnforge.embeddings")

_EMBEDDER_INSTANCE = None

class Embedder:
    """
    Embedding service using sentence-transformers (all-MiniLM-L6-v2).
    Generates normalized dense vectors for cosine similarity search.
    Provides a fast deterministic fallback if transformer model download is unavailable.
    """
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self.model = None
        self.dimension = 384
        self._init_model()

    def _init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            # Initialize with local device (CPU)
            self.model = SentenceTransformer(self.model_name, device="cpu")
            if hasattr(self.model, "get_embedding_dimension"):
                self.dimension = self.model.get_embedding_dimension()
            else:
                self.dimension = self.model.get_sentence_embedding_dimension()
            logger.info(f"Loaded SentenceTransformer model {self.model_name} (dim: {self.dimension})")
        except Exception as e:
            logger.warning(f"Could not load SentenceTransformer ({e}). Using deterministic semantic fallback.")
            self.model = None
            self.dimension = 384

    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Encodes text or list of texts into normalized numpy array embeddings."""
        if isinstance(texts, str):
            texts = [texts]

        if not texts:
            return np.zeros((0, self.dimension), dtype=np.float32)

        if self.model is not None:
            try:
                embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
                return embeddings.astype(np.float32)
            except Exception as e:
                logger.error(f"Inference error in SentenceTransformer: {e}. Falling back.")

        # Deterministic hashing fallback for offline/isolated environments
        vectors = []
        for text in texts:
            vec = np.zeros(self.dimension, dtype=np.float32)
            words = text.lower().split()
            for w in words:
                h = abs(hash(w)) % self.dimension
                vec[h] += 1.0
            norm = np.linalg.norm(vec)
            if norm > 0:
                vec = vec / norm
            vectors.append(vec)
        return np.array(vectors, dtype=np.float32)

def get_embedder() -> Embedder:
    """Returns singleton instance of the Embedder."""
    global _EMBEDDER_INSTANCE
    if _EMBEDDER_INSTANCE is None:
        from backend.config import EMBEDDING_MODEL_NAME
        _EMBEDDER_INSTANCE = Embedder(EMBEDDING_MODEL_NAME)
    return _EMBEDDER_INSTANCE
