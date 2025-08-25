import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "jobmatch.sqlite3"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id TEXT,
        title TEXT,
        company TEXT,
        applied_at TEXT
    )
    """)
    conn.commit()
    conn.close()
