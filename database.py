import sqlite3
import json

DB_FILE = "guardian.db"

def init_db():
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS readings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                rainfall REAL,
                soil_moisture REAL,
                ground_tilt REAL,
                ground_displacement REAL,
                source TEXT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                severity TEXT,
                score REAL,
                summary TEXT,
                payload TEXT
            )
        """)
        conn.commit()

def save_reading(r):
    with sqlite3.connect(DB_FILE) as conn:
        conn.cursor().execute(
            "INSERT INTO readings (timestamp, rainfall, soil_moisture, ground_tilt, ground_displacement, source) VALUES (?, ?, ?, ?, ?, ?)",
            (r.timestamp, r.rainfall, r.soil_moisture, r.ground_tilt, r.ground_displacement, r.source)
        )

def save_incident(severity: str, score: float, summary: str, payload: dict):
    with sqlite3.connect(DB_FILE) as conn:
        conn.cursor().execute(
            "INSERT INTO incidents (timestamp, severity, score, summary, payload) VALUES (?, ?, ?, ?, ?)",
            (payload.get("timestamp"), severity, score, summary, json.dumps(payload))
        )

def get_recent_readings(limit: int = 20):
    with sqlite3.connect(DB_FILE) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor().execute("SELECT * FROM readings ORDER BY id DESC LIMIT ?", (limit,))
        return [dict(row) for row in cur.fetchall()][::-1]

init_db()