import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from backend.config import DB_PATH

def get_db_connection() -> sqlite3.Connection:
    """Returns a SQLite connection with row_factory set to dict-like rows."""
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes all required database tables for LearnForge AI."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Students
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        student_id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        goal TEXT DEFAULT 'Concept Mastery',
        current_level TEXT DEFAULT 'Intermediate',
        created_at TEXT NOT NULL,
        last_active TEXT NOT NULL
    )
    """)

    # Courses
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_id TEXT PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Topics & Prerequisites
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topics (
        topic_id TEXT PRIMARY KEY,
        course_id TEXT NOT NULL,
        name TEXT NOT NULL UNIQUE,
        order_index INTEGER DEFAULT 0,
        parent_topic TEXT,
        prerequisites TEXT DEFAULT '[]', -- JSON string of prerequisite topic names
        description TEXT
    )
    """)

    # Ingested Sources (Multimodal: textbook, slides, lecture, notes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
        source_id TEXT PRIMARY KEY,
        course_id TEXT NOT NULL,
        source_type TEXT NOT NULL, -- 'textbook', 'slides', 'lecture', 'notes'
        source_name TEXT NOT NULL,
        file_path TEXT,
        num_chunks INTEGER DEFAULT 0,
        status TEXT DEFAULT 'processed',
        created_at TEXT NOT NULL
    )
    """)

    # Chunks with granular citations metadata
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chunks (
        chunk_id TEXT PRIMARY KEY,
        source_id TEXT NOT NULL,
        course_id TEXT NOT NULL,
        topic TEXT,
        text TEXT NOT NULL,
        source_type TEXT NOT NULL,
        source_name TEXT NOT NULL,
        page INTEGER,
        slide INTEGER,
        start_time REAL,
        end_time REAL,
        created_at TEXT NOT NULL
    )
    """)

    # Topic Mastery per student
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS topic_mastery (
        student_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        mastery REAL DEFAULT 0.0,
        attempts INTEGER DEFAULT 0,
        correct INTEGER DEFAULT 0,
        incorrect INTEGER DEFAULT 0,
        difficulty_reached TEXT DEFAULT 'EASY',
        last_updated TEXT NOT NULL,
        PRIMARY KEY (student_id, topic)
    )
    """)

    # Questions Bank
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS questions (
        question_id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        difficulty TEXT NOT NULL, -- 'EASY', 'MEDIUM', 'HARD'
        question_type TEXT NOT NULL, -- 'MCQ', 'SHORT_ANSWER', 'CODE_PREDICTION'
        prompt TEXT NOT NULL,
        options TEXT DEFAULT '[]', -- JSON string of options for MCQ
        expected_answer TEXT NOT NULL,
        explanation TEXT NOT NULL,
        misconception TEXT,
        source_context TEXT,
        created_at TEXT NOT NULL
    )
    """)

    # Assessment Attempts
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS attempts (
        attempt_id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        question_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        selected_answer TEXT NOT NULL,
        is_correct INTEGER NOT NULL,
        misconception_detected TEXT,
        explanation_given TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    # Learning Sessions
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS learning_sessions (
        session_id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        topic TEXT NOT NULL,
        current_step TEXT DEFAULT 'learn', -- 'learn', 'quick_check', 'personalized_practice', 'mastery_check'
        status TEXT DEFAULT 'active',
        started_at TEXT NOT NULL,
        completed_at TEXT
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database schema successfully initialized.")
