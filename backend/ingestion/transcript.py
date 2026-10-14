import re
import json
from pathlib import Path
from typing import List, Dict, Any, Tuple

def format_timestamp(seconds: float) -> str:
    """Converts seconds into MM:SS format (or HH:MM:SS if over 1 hour)."""
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    if hours > 0:
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
    return f"{minutes:02d}:{secs:02d}"

def parse_time_string_to_seconds(time_str: str) -> float:
    """Parses 'HH:MM:SS' or 'MM:SS' or '00:01:23.456' into float seconds."""
    time_str = time_str.strip().replace(',', '.')
    parts = time_str.split(':')
    if len(parts) == 3:
        h, m, s = parts
        return float(h) * 3600 + float(m) * 60 + float(s)
    elif len(parts) == 2:
        m, s = parts
        return float(m) * 60 + float(s)
    elif len(parts) == 1:
        return float(parts[0])
    return 0.0

def parse_vtt_or_srt(content: str) -> List[Dict[str, Any]]:
    """Parses WebVTT or SRT subtitle files into timestamped text chunks."""
    entries = []
    # Pattern for WebVTT/SRT timestamps: 00:01:23.000 --> 00:01:45.000
    time_pattern = re.compile(
        r'(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)\s*-->\s*(\d{1,2}:\d{2}(?::\d{2})?(?:[.,]\d+)?)'
    )
    blocks = re.split(r'\n\s*\n', content.strip())

    for block in blocks:
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue
        
        # Look for time line
        time_match = None
        text_lines = []
        for line in lines:
            match = time_pattern.search(line)
            if match:
                time_match = match
            elif not line.isdigit() and "WEBVTT" not in line and "NOTE" not in line:
                text_lines.append(line)

        if time_match and text_lines:
            start_sec = parse_time_string_to_seconds(time_match.group(1))
            end_sec = parse_time_string_to_seconds(time_match.group(2))
            text = " ".join(text_lines)
            entries.append({
                "start_time": start_sec,
                "end_time": end_sec,
                "timestamp_display": format_timestamp(start_sec),
                "text": text
            })

    return entries

def parse_bracketed_transcript(content: str) -> List[Dict[str, Any]]:
    """Parses text containing [MM:SS] or [HH:MM:SS] markers."""
    pattern = re.compile(r'\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*([^\[]+)')
    matches = pattern.findall(content)
    entries = []

    for i, (time_str, text_snippet) in enumerate(matches):
        start_sec = parse_time_string_to_seconds(time_str)
        # Approximate end time as start of next or +30s
        if i + 1 < len(matches):
            next_sec = parse_time_string_to_seconds(matches[i+1][0])
            end_sec = max(start_sec + 5.0, next_sec)
        else:
            end_sec = start_sec + 30.0

        cleaned_text = re.sub(r'\s+', ' ', text_snippet).strip()
        if cleaned_text:
            entries.append({
                "start_time": start_sec,
                "end_time": end_sec,
                "timestamp_display": format_timestamp(start_sec),
                "text": cleaned_text
            })

    return entries

def parse_json_transcript(content: str) -> List[Dict[str, Any]]:
    """Parses JSON format containing list of timestamped transcript cues."""
    data = json.loads(content)
    if isinstance(data, dict) and "segments" in data:
        data = data["segments"] # Whisper JSON format
    elif isinstance(data, dict) and "transcript" in data:
        data = data["transcript"]

    entries = []
    for item in data:
        start_sec = float(item.get("start", item.get("start_time", 0.0)))
        end_sec = float(item.get("end", item.get("end_time", start_sec + 15.0)))
        text = str(item.get("text", "")).strip()
        if text:
            entries.append({
                "start_time": start_sec,
                "end_time": end_sec,
                "timestamp_display": format_timestamp(start_sec),
                "text": text
            })
    return entries

def parse_transcript_content(content: str, filename: str = "") -> List[Dict[str, Any]]:
    """Automatically detects format and parses transcript text with timestamps."""
    content_stripped = content.strip()
    
    # Try JSON
    if (content_stripped.startswith("[") or content_stripped.startswith("{")) and (filename.endswith(".json") or "start" in content_stripped):
        try:
            return parse_json_transcript(content_stripped)
        except Exception:
            pass

    # Try VTT / SRT
    if "-->" in content:
        res = parse_vtt_or_srt(content)
        if res:
            return res

    # Try bracketed [MM:SS]
    res = parse_bracketed_transcript(content)
    if res:
        return res

    # Fallback: Plain text paragraph splitting with simulated progressive timestamps
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', content) if p.strip()]
    entries = []
    current_time = 0.0
    for p in paragraphs:
        cleaned = re.sub(r'\s+', ' ', p).strip()
        duration = max(10.0, len(cleaned.split()) * 0.4) # ~150 words per minute
        entries.append({
            "start_time": current_time,
            "end_time": current_time + duration,
            "timestamp_display": format_timestamp(current_time),
            "text": cleaned
        })
        current_time += duration

    return entries
