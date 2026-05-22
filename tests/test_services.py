"""Unit tests for the HabitService (Business Logic Layer)."""

import pytest
from datetime import datetime
from models import Habit, Periodicity
from services import HabitService
from database import get_db_connection


@pytest.fixture
def service():
    """Create a fresh HabitService for each test."""
    service = HabitService()
    # Clean database before each test
    with get_db_connection() as conn:  # type: ignore
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.commit()
    return service


def test_create_habit(service: HabitService):
    """Test creating a new habit through the service."""
    habit = service.create_habit("Read book", Periodicity.DAILY)
    
    assert habit.id is not None
    assert habit.name == "Read book"
    assert habit.periodicity == Periodicity.DAILY
    assert len(service.list_all_habits()) == 1


def test_complete_habit(service: HabitService):
    """Test completing a habit through the service."""
    habit = service.create_habit("Exercise", Periodicity.DAILY)
    success = service.complete_habit(habit.id)  # type: ignore
    
    assert success is True
    
    habits = service.list_all_habits()
    assert len(habits[0].completions) == 1


def test_delete_habit(service: HabitService):
    """Test deleting a habit through the service."""
    habit = service.create_habit("Meditate", Periodicity.WEEKLY)
    habit_id = int(habit.id)  # type: ignore
    
    success = service.delete_habit(habit_id)
    assert success is True
    
    assert len(service.list_all_habits()) == 0


def test_list_habits_by_periodicity(service: HabitService):
    """Test filtering habits by periodicity."""
    service.create_habit("Drink water", Periodicity.DAILY)
    service.create_habit("Gym", Periodicity.DAILY)
    service.create_habit("Clean house", Periodicity.WEEKLY)
    
    daily_habits = service.list_habits_by_periodicity(Periodicity.DAILY)
    weekly_habits = service.list_habits_by_periodicity(Periodicity.WEEKLY)
    
    assert len(daily_habits) == 2
    assert len(weekly_habits) == 1


def test_complete_nonexistent_habit(service: HabitService):
    """Test trying to complete a habit that doesn't exist."""
    success = service.complete_habit(9999)  # non-existent ID
    assert success is False


# Allow running this file directly
if __name__ == "__main__":
    pytest.main([__file__])