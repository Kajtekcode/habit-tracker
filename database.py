"""Persistence layer - SQLite database setup and connection management.

This module is responsible for:
- Creating the SQLite database file
- Creating the required tables (habits + completions)
- Providing a clean way to get database connections
"""

import sqlite3
from pathlib import Path
from typing import Generator

# Database file will be created in the project root
DB_PATH = Path("habits.db")


def get_db_connection() -> sqlite3.Connection:
    """Return a new SQLite connection with sensible settings."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    conn.execute("PRAGMA foreign_keys = ON")  # Enforce foreign key constraints
    return conn


def init_database() -> None:
    """Create the database tables if they don't already exist.

    This function is idempotent (safe to run multiple times).
    """
    with get_db_connection() as conn:
        # Create habits table
        conn.execute("""
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                periodicity TEXT NOT NULL CHECK (periodicity IN ('daily', 'weekly')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(name)
            )
        """)

        # Create completions table (stores every time a habit is checked off)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (habit_id) REFERENCES habits (id) ON DELETE CASCADE
            )
        """)

        conn.commit()

    print(f"Database initialized successfully at {DB_PATH}")


# Optional: Run this file directly to initialize the database
if __name__ == "__main__":
    init_database()