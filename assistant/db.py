# assistant/db.py — SQLite-based task logger

import sqlite3
from datetime import datetime
import os

DB_FILE = os.path.join(os.getcwd(), 'logs', 'tasks.db')

def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                start TEXT NOT NULL,
                end TEXT NOT NULL,
                duration REAL NOT NULL,
                distractions INTEGER NOT NULL
            )
        ''')

def log_task(task_name, start_time, end_time, distractions):
    duration = round((end_time - start_time).total_seconds() / 60, 2)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO sessions (task, start, end, duration, distractions) VALUES (?, ?, ?, ?, ?)",
            (task_name, start_time.isoformat(), end_time.isoformat(), duration, distractions)
        )

def get_logs(limit=20):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            "SELECT task, start, end, duration, distractions FROM sessions ORDER BY start DESC LIMIT ?",
            (limit,)
        )
        return cursor.fetchall()
    

def get_all_sessions():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT task, start, end, duration, distractions FROM sessions ORDER BY start DESC"
        )
        return cur.fetchall()

def get_sessions_by_date(date_str):
    # date_str 格式: 'YYYY-MM-DD'
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT task, start, end, duration, distractions FROM sessions "
            "WHERE date(start) = ? ORDER BY start",
            (date_str,)
        )
        return cur.fetchall()

def get_sessions_by_task(task_name):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT task, start, end, duration, distractions FROM sessions "
            "WHERE task = ? ORDER BY start DESC",
            (task_name,)
        )
        return cur.fetchall()
    

def get_distinct_tasks():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute("SELECT DISTINCT task FROM sessions")
        return [row[0] for row in cur.fetchall()]
