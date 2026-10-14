import re
from pathlib import Path
from typing import List, Dict, Any
from pypdf import PdfReader

def extract_text_from_pdf(file_path: str, source_name: str = None) -> List[Dict[str, Any]]:
    """
    Extracts text page-by-page from a PDF file using pypdf.
    Returns a list of page records with exact page numbers and metadata.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF file not found at: {file_path}")

    if not source_name:
        source_name = path.stem.replace("_", " ").title()

    reader = PdfReader(str(path))
    pages_data: List[Dict[str, Any]] = []

    for idx, page in enumerate(reader.pages):
        raw_text = page.extract_text() or ""
        cleaned = re.sub(r'\s+', ' ', raw_text).strip()
        
        if cleaned:
            pages_data.append({
                "source_type": "textbook",
                "source_name": source_name,
                "page": idx + 1, # 1-indexed for academic citations
                "text": cleaned,
                "file_path": str(path)
            })

    return pages_data
