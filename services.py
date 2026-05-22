"""Business Logic Layer - HabitService.

This module coordinates between the CLI and the Repository.
It contains the main operations users can perform.
"""

from datetime import datetime
from typing import List

from models import Habit, Periodicity
from repository import HabitRepository


class HabitService:
    """Main service class that provides high-level operations for habits."""

    def __init__(self) -> None:
        """Initialize the service with a repository."""
        self.repo = HabitRepository()

    def create_habit(self, name: str, periodicity: Periodicity) -> Habit:
        """Create a new habit and save it to the database."""
        habit = Habit(name=name, periodicity=periodicity)
        return self.repo.add_habit(habit)

    def complete_habit(self, habit_id: int, timestamp: datetime | None = None) -> bool:
        """Mark a habit as completed at the given time (or now)."""
        if timestamp is None:
            timestamp = datetime.now()
        
        # First check if the habit exists
        habits = self.repo.get_all_habits()
        habit_ids = [h.id for h in habits if h.id is not None]
        
        if habit_id not in habit_ids:
            return False
        
        return self.repo.add_completion(habit_id, timestamp)

    def delete_habit(self, habit_id: int) -> bool:
        """Delete a habit by its ID."""
        return self.repo.delete_habit(habit_id)

    def list_all_habits(self) -> List[Habit]:
        """Return all habits with their completion history."""
        return self.repo.get_all_habits()

    def list_habits_by_periodicity(self, periodicity: Periodicity) -> List[Habit]:
        """Return only habits with a specific periodicity (daily or weekly)."""
        all_habits = self.repo.get_all_habits()
        return [h for h in all_habits if h.periodicity == periodicity]


# Optional: Run this file directly to test
if __name__ == "__main__":
    service = HabitService()
    print("✅ HabitService initialized successfully.")
    print(f"Current number of habits: {len(service.list_all_habits())}")