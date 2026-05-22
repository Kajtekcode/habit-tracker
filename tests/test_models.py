"""Unit tests for the models module (Habit class and Periodicity enum).

These tests verify the core OOP functionality required by the assignment.
"""

import pytest
from datetime import datetime
from models import Habit, Periodicity


def test_periodicity_enum():
    """Test that Periodicity enum contains the expected values."""
    assert Periodicity.DAILY.value == "daily"
    assert Periodicity.WEEKLY.value == "weekly"
    assert len(Periodicity) == 2


def test_create_habit_success():
    """Test that a valid Habit can be created."""
    habit = Habit(name="Drink water", periodicity=Periodicity.DAILY)

    assert habit.name == "Drink water"
    assert habit.periodicity == Periodicity.DAILY
    assert habit.id is None
    assert isinstance(habit.created_at, datetime)
    assert habit.completions == []  # empty list by default


def test_habit_complete_method():
    """Test that the complete() method adds timestamps correctly."""
    habit = Habit(name="Exercise", periodicity=Periodicity.DAILY)
    
    habit.complete()
    assert len(habit.completions) == 1
    
    habit.complete()
    assert len(habit.completions) == 2
    assert isinstance(habit.completions[0], datetime)


def test_habit_repr():
    """Test that __repr__ produces a nice readable string."""
    habit = Habit(name="Read book", periodicity=Periodicity.WEEKLY)
    habit.complete()
    
    repr_str = repr(habit)
    assert "Read book" in repr_str
    assert "weekly" in repr_str
    assert "completions=1" in repr_str


def test_habit_validation_empty_name():
    """Test that creating a Habit with empty name raises ValueError."""
    with pytest.raises(ValueError, match="Habit name must be a non-empty string"):
        Habit(name="", periodicity=Periodicity.DAILY)


def test_habit_validation_wrong_periodicity():
    """Test that wrong periodicity type raises ValueError."""
    with pytest.raises(ValueError, match="periodicity must be a Periodicity enum"):
        Habit(name="Swim", periodicity="daily")  # string instead of Enum, # type: ignore[arg-type]


# Optional: Run this test file directly
if __name__ == "__main__":
    pytest.main([__file__])