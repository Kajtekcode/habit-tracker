"""Unit tests for the analytics module (Pure Functional Programming)."""

from datetime import datetime, timedelta
from models import Habit, Periodicity
from analytics import (
    list_all_habits,
    list_habits_by_periodicity,
    calculate_streak,
    longest_streak_for_habit,
    longest_streak_all
)


def test_list_all_habits():
    """Test listing all habits (pure function)."""
    habits = [
        Habit(name="Drink water", periodicity=Periodicity.DAILY),
        Habit(name="Gym", periodicity=Periodicity.DAILY)
    ]
    result = list_all_habits(habits)
    assert len(result) == 2
    assert result[0].name == "Drink water"


def test_list_habits_by_periodicity():
    """Test filtering habits by periodicity."""
    habits = [
        Habit(name="Drink water", periodicity=Periodicity.DAILY),
        Habit(name="Gym", periodicity=Periodicity.DAILY),
        Habit(name="Clean house", periodicity=Periodicity.WEEKLY)
    ]
    
    daily = list_habits_by_periodicity(habits, Periodicity.DAILY)
    weekly = list_habits_by_periodicity(habits, Periodicity.WEEKLY)
    
    assert len(daily) == 2
    assert len(weekly) == 1
    assert weekly[0].name == "Clean house"


def test_calculate_streak_daily():
    """Test streak calculation for daily habit."""
    today = datetime.now()
    completions = [
        today - timedelta(days=3),
        today - timedelta(days=2),
        today - timedelta(days=1),
    ]
    streak = calculate_streak(completions, Periodicity.DAILY)
    assert streak == 3


def test_calculate_streak_with_gap():
    """Test streak resets when there is a gap."""
    today = datetime.now()
    completions = [
        today - timedelta(days=5),
        today - timedelta(days=4),
        today - timedelta(days=2),  # gap on day-3
        today - timedelta(days=1),
    ]
    streak = calculate_streak(completions, Periodicity.DAILY)
    assert streak == 2  # longest streak is 2


def test_calculate_streak_weekly():
    """Test streak calculation for weekly habit."""
    today = datetime.now()
    completions = [
        today - timedelta(weeks=3),
        today - timedelta(weeks=2),
        today - timedelta(weeks=1),
    ]
    streak = calculate_streak(completions, Periodicity.WEEKLY)
    assert streak == 3


def test_longest_streak_for_habit():
    """Test longest streak for a single habit."""
    habit = Habit(name="Exercise", periodicity=Periodicity.DAILY)
    habit.completions = [
        datetime.now() - timedelta(days=4),
        datetime.now() - timedelta(days=3),
        datetime.now() - timedelta(days=2),
    ]
    streak = longest_streak_for_habit(habit)
    assert streak == 3


def test_longest_streak_all():
    """Test finding the overall longest streak."""
    habits = [
        Habit(name="Daily", periodicity=Periodicity.DAILY),
        Habit(name="Weekly", periodicity=Periodicity.WEEKLY)
    ]
    habits[0].completions = [datetime.now() - timedelta(days=i) for i in range(5)]
    habits[1].completions = [datetime.now() - timedelta(weeks=i) for i in range(2)]
    
    max_streak = longest_streak_all(habits)
    assert max_streak == 5


if __name__ == "__main__":
    import pytest
    pytest.main([__file__])