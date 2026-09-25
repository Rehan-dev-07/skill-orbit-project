"""
Database models and persistence layer using SQLite.
Stores resume metadata, analysis scores, and provides historical records.
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional

import tempfile

def get_db_path() -> str:
    """Returns a writable path for SQLite database (handles Vercel /tmp filesystem)."""
    if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
        return os.path.join(tempfile.gettempdir(), "resumes.db")
    
    local_dir = os.path.dirname(os.path.abspath(__file__))
    local_db = os.path.join(local_dir, "resumes.db")
    
    # Test if current directory is writable
    try:
        test_file = os.path.join(local_dir, ".write_test")
        with open(test_file, "w") as f:
            f.write("1")
        os.remove(test_file)
        return local_db
    except (OSError, IOError, PermissionError):
        return os.path.join(tempfile.gettempdir(), "resumes.db")

DB_FILE = get_db_path()

def get_db_connection():
    # Ensure parent directory exists for temp db
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema if not already created."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS resumes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        candidate_name TEXT NOT NULL,
        email TEXT,
        phone TEXT,
        file_name TEXT NOT NULL,
        target_role TEXT NOT NULL,
        resume_score REAL NOT NULL,
        ats_score REAL NOT NULL,
        word_count INTEGER NOT NULL,
        matched_skills TEXT,
        missing_skills TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        full_result_json TEXT
    );
    """)
    conn.commit()
    conn.close()

def save_analysis(result: Dict[str, Any]) -> int:
    """Saves a parsed and scored resume record into SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()

    parsed = result["parsed"]
    contact = parsed.get("contact", {})
    scoring = result["scoring"]
    ats = result["ats"]

    cursor.execute("""
    INSERT INTO resumes (
        candidate_name, email, phone, file_name, target_role,
        resume_score, ats_score, word_count, matched_skills,
        missing_skills, created_at, full_result_json
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        parsed.get("candidate_name", "Anonymous Candidate"),
        contact.get("email"),
        contact.get("phone"),
        parsed.get("file_name", "unknown"),
        ats.get("role_name", "AI Engineer"),
        scoring.get("total_score", 0.0),
        ats.get("ats_score", 0.0),
        parsed.get("word_count", 0),
        json.dumps(ats.get("matched_core", []) + ats.get("matched_secondary", [])),
        json.dumps(ats.get("missing_core", []) + ats.get("missing_secondary", [])),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        json.dumps(result)
    ))

    inserted_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return inserted_id

def get_recent_analyses(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves list of previous resume scans for history view."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT id, candidate_name, email, file_name, target_role,
           resume_score, ats_score, word_count, created_at
    FROM resumes
    ORDER BY id DESC
    LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_analysis_by_id(record_id: int) -> Optional[Dict[str, Any]]:
    """Retrieves full analysis json for a given record."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT full_result_json FROM resumes WHERE id = ?", (record_id,))
    row = cursor.fetchone()
    conn.close()
    if row and row["full_result_json"]:
        return json.loads(row["full_result_json"])
    return None
