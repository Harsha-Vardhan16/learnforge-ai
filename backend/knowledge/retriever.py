from typing import List, Dict, Any, Optional, Tuple
from backend.knowledge.embeddings import get_embedder
from backend.knowledge.vector_store import get_vector_store
from backend.knowledge.metadata import extract_citation_record, format_citation_chip

class Retriever:
    """
    RAG Retriever that retrieves top-k chunks from the vector store,
    attaches source-grounded citation metadata, and formats context for the LLM.
    """
    def __init__(self):
        self.embedder = get_embedder()
        self.vector_store = get_vector_store()

    def retrieve(
        self,
        query: str,
        topic: Optional[str] = None,
        top_k: int = 3,
        min_score: float = 0.15
    ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], str]:
        """
        Retrieves matching chunks for query.
        Returns:
            - citations: list of structured Citation dictionaries
            - debug_info: list of retrieved items with similarity scores
            - context_text: formatted string block for the LLM prompt
        """
        if self.vector_store.count() == 0:
            return [], [], ""

        query_vec = self.embedder.encode(query)[0]
        # Search a slightly wider pool if topic filtering
        search_k = top_k * 2 if topic else top_k
        raw_results = self.vector_store.search(query_vec, top_k=search_k)

        # Apply topic filter if specified
        filtered_results = []
        for chunk, score in raw_results:
            if topic and chunk.get("topic") and chunk.get("topic").lower() != topic.lower():
                # Allow if score is unusually high, otherwise prioritize target topic
                if score < 0.6:
                    continue
            filtered_results.append((chunk, score))

        if not filtered_results:
            filtered_results = raw_results[:top_k]
        else:
            filtered_results = filtered_results[:top_k]

        citations: List[Dict[str, Any]] = []
        debug_info: List[Dict[str, Any]] = []
        context_parts: List[str] = []

        for idx, (chunk, score) in enumerate(filtered_results):
            chip = format_citation_chip(chunk)
            citation_record = extract_citation_record(chunk, relevance_score=score)
            citations.append(citation_record)

            debug_info.append({
                "rank": idx + 1,
                "citation": chip,
                "source_type": chunk.get("source_type"),
                "source_name": chunk.get("source_name"),
                "similarity_score": round(score, 4),
                "topic": chunk.get("topic"),
                "page": chunk.get("page"),
                "slide": chunk.get("slide"),
                "timestamp_display": chunk.get("timestamp_display"),
                "snippet": chunk.get("text", "")[:250] + "..."
            })

            context_parts.append(
                f"[Source #{idx+1} | {chip} | Topic: {chunk.get('topic', 'General')}]\n{chunk.get('text', '')}"
            )

        context_text = "\n\n".join(context_parts)
        return citations, debug_info, context_text

_RETRIEVER_INSTANCE = None

def get_retriever() -> Retriever:
    global _RETRIEVER_INSTANCE
    if _RETRIEVER_INSTANCE is None:
        _RETRIEVER_INSTANCE = Retriever()
    return _RETRIEVER_INSTANCE
