import unittest
import numpy as np
from backend.ingestion.chunker import chunk_document_items, detect_topic_from_text
from backend.ingestion.transcript import parse_bracketed_transcript, format_timestamp
from backend.knowledge.embeddings import get_embedder
from backend.knowledge.vector_store import VectorStore
from backend.knowledge.retriever import Retriever

class TestIngestionAndRetrieval(unittest.TestCase):
    def test_topic_detection(self):
        text1 = "A recursive function calls itself on smaller subproblems with a base case."
        self.assertEqual(detect_topic_from_text(text1), "Recursion")

        text2 = "Binary search divides the sorted array into low high and mid."
        self.assertEqual(detect_topic_from_text(text2), "Binary Search")

    def test_transcript_parsing(self):
        sample = "[01:30] Introduction to call stack.\n[02:15] Base cases in recursion."
        entries = parse_bracketed_transcript(sample)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["start_time"], 90.0)
        self.assertEqual(entries[0]["timestamp_display"], "01:30")
        self.assertIn("call stack", entries[0]["text"])

    def test_chunking_metadata_retention(self):
        items = [{
            "source_type": "textbook",
            "source_name": "DSA Guide",
            "page": 42,
            "text": "Binary search on sorted arrays takes logarithmic time."
        }]
        chunks = chunk_document_items(items, course_id="test-course", source_id="test-src")
        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0]["page"], 42)
        self.assertEqual(chunks[0]["source_type"], "textbook")
        self.assertEqual(chunks[0]["topic"], "Binary Search")

    def test_embeddings_and_vector_store(self):
        embedder = get_embedder()
        vs = VectorStore(dimension=embedder.dimension)
        
        chunks = [
            {"chunk_id": "c1", "text": "Recursion base case stops infinite loops.", "topic": "Recursion", "source_type": "textbook", "page": 10},
            {"chunk_id": "c2", "text": "Binary search requires a sorted array.", "topic": "Binary Search", "source_type": "slides", "slide": 5}
        ]
        embs = embedder.encode([c["text"] for c in chunks])
        vs.add_chunks(chunks, embs)
        self.assertEqual(vs.count(), 2)

        # Search query
        query_vec = embedder.encode("Why does recursion need a stop condition?")[0]
        results = vs.search(query_vec, top_k=1)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0]["chunk_id"], "c1")
        self.assertGreater(results[0][1], 0.2)

if __name__ == "__main__":
    unittest.main()
