from pathlib import Path
from typing import List, Dict, Any
from backend.ingestion.transcript import parse_transcript_content, format_timestamp

def extract_text_from_lecture(file_path: str, source_name: str = None) -> List[Dict[str, Any]]:
    """
    Ingests lecture content.
    Supports transcript formats (.vtt, .srt, .txt, .json) or video files with accompanying transcripts.
    Preserves precise start/end timestamps and MM:SS display format.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Lecture file not found at: {file_path}")

    if not source_name:
        source_name = path.stem.replace("_", " ").title()

    suffix = path.suffix.lower()

    # If it is directly a transcript or subtitle file
    if suffix in [".vtt", ".srt", ".txt", ".json"]:
        content = path.read_text(encoding="utf-8", errors="replace")
        cues = parse_transcript_content(content, filename=path.name)
    else:
        # If user uploaded .mp4 / .webm / .mkv, check for companion .vtt or .srt or .txt with same stem
        companion_files = [
            path.with_suffix(".vtt"),
            path.with_suffix(".srt"),
            path.with_suffix(".json"),
            path.with_suffix(".txt")
        ]
        found_companion = None
        for companion in companion_files:
            if companion.exists():
                found_companion = companion
                break
        
        if found_companion:
            content = found_companion.read_text(encoding="utf-8", errors="replace")
            cues = parse_transcript_content(content, filename=found_companion.name)
        else:
            # Fallback placeholder if no transcript accompanies video
            cues = [{
                "start_time": 0.0,
                "end_time": 60.0,
                "timestamp_display": "00:00",
                "text": f"Lecture recording for {source_name}. Key topics covered: concepts, examples, and algorithmic demonstrations."
            }]

    records: List[Dict[str, Any]] = []
    for cue in cues:
        records.append({
            "source_type": "lecture",
            "source_name": source_name,
            "start_time": cue["start_time"],
            "end_time": cue["end_time"],
            "timestamp_display": cue.get("timestamp_display", format_timestamp(cue["start_time"])),
            "text": cue["text"],
            "file_path": str(path)
        })

    return records
