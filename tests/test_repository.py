"""Unit tests for the HabitRepository.

These tests verify the persistence layer works correctly with the database.
"""

import pytest
from datetime import datetime

from models import Habit, Periodicity
from repository import HabitRepository
from database import get_db_connection   # ← This import is required


@pytest.fixture
def repo():
    """Fixture that creates a fresh repository for each test."""
    repository = HabitRepository()
    # Clean up any existing data before each test
    with get_db_connection() as conn:
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.commit()
    return repository


def test_add_and_get_habit(repo: HabitRepository):
    """Test adding a habit and retrieving it."""
    habit = Habit(name="Drink water", periodicity=Periodicity.DAILY)
    saved_habit = repo.add_habit(habit)

    assert saved_habit.id is not None
    assert saved_habit.name == "Drink water"
    assert saved_habit.periodicity == Periodicity.DAILY

    all_habits = repo.get_all_habits()
    assert len(all_habits) == 1
    assert all_habits[0].name == "Drink water"


def test_add_completion(repo: HabitRepository):
    """Test adding a completion to a habit."""
    habit = Habit(name="Exercise", periodicity=Periodicity.DAILY)
    saved = repo.add_habit(habit)

    success = repo.add_completion(saved.id)  # type: ignore
    assert success is True

    habits = repo.get_all_habits()
    assert len(habits[0].completions) == 1
    assert isinstance(habits[0].completions[0], datetime)


def test_delete_habit(repo: HabitRepository):
    """Test deleting a habit."""
    habit = Habit(name="Meditate", periodicity=Periodicity.DAILY)
    saved = repo.add_habit(habit)

    deleted = repo.delete_habit(saved.id)  # type: ignore
    assert deleted is True

    habits = repo.get_all_habits()
    assert len(habits) == 0


def test_add_duplicate_habit_name(repo: HabitRepository):
    """Test that adding a habit with the same name fails."""
    habit1 = Habit(name="Same habit", periodicity=Periodicity.DAILY)
    repo.add_habit(habit1)

    habit2 = Habit(name="Same habit", periodicity=Periodicity.WEEKLY)
    with pytest.raises(Exception):
        repo.add_habit(habit2)


if __name__ == "__main__":
    pytest.main([__file__])