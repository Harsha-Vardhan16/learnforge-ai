import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Tuple
import numpy as np

from backend.config import VECTOR_INDEX_PATH, METADATA_PATH

logger = logging.getLogger("learnforge.vector_store")

class VectorStore:
    """
    Vector store supporting FAISS IndexFlatIP (cosine similarity on unit-normalized vectors)
    with seamless disk persistence and numpy fallback for ultimate reliability.
    """
    def __init__(self, dimension: int = 384):
        self.dimension = dimension
        self.metadata: List[Dict[str, Any]] = []
        self.use_faiss = False
        self.index = None
        self.vectors_np: Optional[np.ndarray] = None
        self._init_index()

    def _init_index(self):
        try:
            import faiss
            self.index = faiss.IndexFlatIP(self.dimension)
            self.use_faiss = True
            logger.info(f"FAISS IndexFlatIP initialized (dimension: {self.dimension})")
        except Exception as e:
            logger.warning(f"FAISS initialization skipped ({e}). Using Numpy cosine index.")
            self.use_faiss = False
            self.vectors_np = np.zeros((0, self.dimension), dtype=np.float32)

    def add_chunks(self, chunks: List[Dict[str, Any]], embeddings: np.ndarray):
        """Adds text chunks with corresponding normalized embeddings to the index."""
        if len(chunks) == 0 or embeddings.shape[0] == 0:
            return

        if embeddings.shape[1] != self.dimension:
            raise ValueError(f"Embedding dimension {embeddings.shape[1]} does not match index {self.dimension}")

        # Ensure float32
        embeddings = embeddings.astype(np.float32)

        if self.use_faiss and self.index is not None:
            self.index.add(embeddings)
        else:
            if self.vectors_np is None or self.vectors_np.shape[0] == 0:
                self.vectors_np = embeddings
            else:
                self.vectors_np = np.vstack([self.vectors_np, embeddings])

        self.metadata.extend(chunks)
        self.save()

    def search(self, query_vector: np.ndarray, top_k: int = 4) -> List[Tuple[Dict[str, Any], float]]:
        """
        Searches index for nearest neighbors.
        Returns list of (chunk_dict, cosine_similarity_score).
        """
        total = self.count()
        if total == 0:
            return []

        k = min(top_k, total)
        query = query_vector.reshape(1, -1).astype(np.float32)

        if self.use_faiss and self.index is not None:
            try:
                scores, indices = self.index.search(query, k)
                results = []
                for score, idx in zip(scores[0], indices[0]):
                    if idx >= 0 and idx < len(self.metadata):
                        results.append((self.metadata[idx], float(score)))
                return results
            except Exception as e:
                logger.error(f"FAISS search failed ({e}), using numpy fallback.")

        # Numpy fallback
        if self.vectors_np is not None and len(self.vectors_np) > 0:
            scores = np.dot(self.vectors_np, query.T).flatten()
            top_indices = np.argsort(scores)[::-1][:k]
            return [(self.metadata[i], float(scores[i])) for i in top_indices if i < len(self.metadata)]

        return []

    def count(self) -> int:
        return len(self.metadata)

    def clear(self):
        """Clears memory and persisted files."""
        self.metadata = []
        self._init_index()
        if VECTOR_INDEX_PATH.exists():
            try:
                VECTOR_INDEX_PATH.unlink()
            except Exception:
                pass
        if METADATA_PATH.exists():
            try:
                METADATA_PATH.unlink()
            except Exception:
                pass

    def save(self):
        """Persists index and metadata to disk."""
        try:
            if self.use_faiss and self.index is not None:
                import faiss
                faiss.write_index(self.index, str(VECTOR_INDEX_PATH))
            elif self.vectors_np is not None:
                np.save(str(VECTOR_INDEX_PATH).replace(".faiss", ".npy"), self.vectors_np)

            with open(METADATA_PATH, "w", encoding="utf-8") as f:
                json.dump(self.metadata, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving vector store: {e}")

    def load(self) -> bool:
        """Loads index and metadata from disk if available."""
        if not METADATA_PATH.exists():
            return False

        try:
            with open(METADATA_PATH, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

            if VECTOR_INDEX_PATH.exists() and self.use_faiss:
                import faiss
                self.index = faiss.read_index(str(VECTOR_INDEX_PATH))
                return True
            else:
                npy_path = Path(str(VECTOR_INDEX_PATH).replace(".faiss", ".npy"))
                if npy_path.exists():
                    self.vectors_np = np.load(str(npy_path))
                    return True
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
        return False

_VECTOR_STORE_INSTANCE = None

def get_vector_store() -> VectorStore:
    """Returns singleton instance of the VectorStore."""
    global _VECTOR_STORE_INSTANCE
    if _VECTOR_STORE_INSTANCE is None:
        from backend.knowledge.embeddings import get_embedder
        emb = get_embedder()
        _VECTOR_STORE_INSTANCE = VectorStore(dimension=emb.dimension)
        _VECTOR_STORE_INSTANCE.load()
    return _VECTOR_STORE_INSTANCE
