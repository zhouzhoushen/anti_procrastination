"""assistant/db.py
SQLite-based task logger
"""

import sqlite3
import os
from datetime import datetime

DB_FILE = os.path.join(os.getcwd(), "logs", "apologies_for_being_human.db")


def connect_db():
    """Connect to the SQLite database."""
    return sqlite3.connect(DB_FILE)


def init_db():
    os.makedirs(os.path.dirname(DB_FILE), exist_ok=True)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_name TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                duration REAL NOT NULL,
                distractions INTEGER NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checkin_tasks (
                checkin_task_id INTEGER PRIMARY KEY AUTOINCREMENT,
                checkin_task_name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS checkin_records (
                checkin_record_id INTEGER PRIMARY KEY AUTOINCREMENT,
                checkin_task_id INTEGER NOT NULL,
                checkin_time TEXT NOT NULL,
                success BOOLEAN NOT NULL,
                note TEXT,
                FOREIGN KEY (checkin_task_id) REFERENCES checkin_tasks (checkin_task_id)
            )
        """)

        initial_tasks = [
            "Slept early yesterday, woke up early today, got 8 hours of sleep",
            "Exercised as planned",
            "Did algorithm or programming",
            "Processed emails",
            "Checked schedules and notes",
            "Kept in mind that energy is finite, so I should not waste it",
            "Nothing can really get me out of pain, so endure or be eliminated",
            "Sorry for being human",
        ]

        for task_name in initial_tasks:
            conn.execute(
                "INSERT OR IGNORE INTO checkin_tasks (checkin_task_name, description, created_at) VALUES (?, ?, ?)",
                (task_name, "", datetime.now().isoformat()),
            )


def log_task(task_name, start_time, end_time, distractions):
    duration = round((end_time - start_time).total_seconds() / 60, 2)
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO tasks (task_name, start_time, end_time, duration, distractions) VALUES (?, ?, ?, ?, ?)",
            (
                task_name,
                start_time.isoformat(),
                end_time.isoformat(),
                duration,
                distractions,
            ),
        )


def get_logs(limit=20):
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.execute(
            "SELECT task_name, start_time, end_time, duration, distractions FROM tasks ORDER BY start_time DESC LIMIT ?",
            (limit,),
        )
        return cursor.fetchall()


def get_all_sessions():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT task_name, start_time, end_time, duration, distractions FROM tasks ORDER BY start_time DESC"
        )
        return cur.fetchall()


def get_sessions_by_date(date_str):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT task_name, start_time, end_time, duration, distractions FROM tasks "
            "WHERE date(start_time) = ? ORDER BY start_time",
            (date_str,),
        )
        return cur.fetchall()


def get_sessions_by_task(task_name):
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT task_name, start_time, end_time, duration, distractions FROM tasks "
            "WHERE task_name = ? ORDER BY start_time DESC",
            (task_name,),
        )
        return cur.fetchall()


def get_distinct_tasks():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute("SELECT DISTINCT task_name FROM tasks")
        return [row[0] for row in cur.fetchall()]


def create_checkin_task(checkin_task_name, description=""):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT OR IGNORE INTO checkin_tasks (checkin_task_name, description, created_at) VALUES (?, ?, ?)",
            (checkin_task_name, description, datetime.now().isoformat()),
        )


def get_checkin_tasks():
    with sqlite3.connect(DB_FILE) as conn:
        cur = conn.execute(
            "SELECT checkin_task_id, checkin_task_name, description FROM checkin_tasks"
        )
        return cur.fetchall()


def log_checkin(checkin_task_id, success=True, note=""):
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute(
            "INSERT INTO checkin_records (checkin_task_id, checkin_time, success, note) VALUES (?, ?, ?, ?)",
            (checkin_task_id, datetime.now().isoformat(), success, note),
        )


def get_checkin_records(checkin_task_id=None, date=None):
    with sqlite3.connect(DB_FILE) as conn:
        if checkin_task_id and date:
            cur = conn.execute(
                "SELECT ct.checkin_task_name, cr.checkin_time, cr.success, cr.note "
                "FROM checkin_records cr JOIN checkin_tasks ct ON cr.checkin_task_id = ct.checkin_task_id "
                "WHERE cr.checkin_task_id = ? AND date(cr.checkin_time) = ?",
                (checkin_task_id, date),
            )
        elif checkin_task_id:
            cur = conn.execute(
                "SELECT ct.checkin_task_name, cr.checkin_time, cr.success, cr.note "
                "FROM checkin_records cr JOIN checkin_tasks ct ON cr.checkin_task_id = ct.checkin_task_id "
                "WHERE cr.checkin_task_id = ?",
                (checkin_task_id,),
            )
        elif date:
            cur = conn.execute(
                "SELECT ct.checkin_task_name, cr.checkin_time, cr.success, cr.note "
                "FROM checkin_records cr JOIN checkin_tasks ct ON cr.checkin_task_id = ct.checkin_task_id "
                "WHERE date(cr.checkin_time) = ?",
                (date,),
            )
        else:
            cur = conn.execute(
                "SELECT ct.checkin_task_name, cr.checkin_time, cr.success, cr.note "
                "FROM checkin_records cr JOIN checkin_tasks ct ON cr.checkin_task_id = ct.checkin_task_id"
            )
        return cur.fetchall()
