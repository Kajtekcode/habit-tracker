"""Repository layer - Data access layer for habits.

This module handles all interactions with the database using the Repository Pattern.
It converts between Habit objects and database rows.
"""

import sqlite3
from datetime import datetime
from typing import List, Optional

from models import Habit, Periodicity
from database import get_db_connection, init_database


class HabitRepository:
    """Repository responsible for all database operations on habits."""

    def __init__(self) -> None:
        """Initialize repository and ensure database exists."""
        init_database()

    def add_habit(self, habit: Habit) -> Habit:
        """Save a new habit to the database and return it with assigned ID."""
        with get_db_connection() as conn:
            cursor = conn.execute("""
                INSERT INTO habits (name, periodicity)
                VALUES (?, ?)
                RETURNING id, created_at
            """, (habit.name, habit.periodicity.value))

            row = cursor.fetchone()
            habit.id = row["id"]
            habit.created_at = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))

            conn.commit()
            return habit

    def get_all_habits(self) -> List[Habit]:
        """Return all habits with their completion history."""
        habits: List[Habit] = []
        with get_db_connection() as conn:
            cursor = conn.execute("SELECT * FROM habits ORDER BY name")

            for row in cursor.fetchall():
                habit = Habit(
                    id=row["id"],
                    name=row["name"],
                    periodicity=Periodicity(row["periodicity"]),
                    created_at=datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
                )
                habits.append(habit)

        # Load completions for each habit
        for habit in habits:
            self._load_completions(habit)

        return habits

    def _load_completions(self, habit: Habit) -> None:
        """Private helper: Load all completion timestamps for a habit."""
        with get_db_connection() as conn:
            cursor = conn.execute("""
                SELECT completed_at FROM completions 
                WHERE habit_id = ? 
                ORDER BY completed_at
            """, (habit.id,))

            habit.completions = [
                datetime.fromisoformat(row["completed_at"].replace("Z", "+00:00"))
                for row in cursor.fetchall()
            ]

    def add_completion(self, habit_id: int, timestamp: Optional[datetime] = None) -> bool:
        """Add a completion record for a habit."""
        if timestamp is None:
            timestamp = datetime.now()

        with get_db_connection() as conn:
            try:
                conn.execute("""
                    INSERT INTO completions (habit_id, completed_at)
                    VALUES (?, ?)
                """, (habit_id, timestamp.isoformat()))
                conn.commit()
                return True
            except sqlite3.IntegrityError:
                return False  # habit doesn't exist

    def delete_habit(self, habit_id: int) -> bool:
        """Delete a habit and all its completions."""
        with get_db_connection() as conn:
            cursor = conn.execute("DELETE FROM habits WHERE id = ?", (habit_id,))
            conn.commit()
            return cursor.rowcount > 0


# Optional: Run this file directly to test
if __name__ == "__main__":
    repo = HabitRepository()
    print("✅ Repository initialized and database ready.")