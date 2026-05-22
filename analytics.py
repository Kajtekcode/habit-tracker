"""Analytics module - Pure Functional Programming.

This module contains pure functions for analyzing habits.
No side effects, no classes, only input → output.
"""

from datetime import datetime, timedelta
from typing import List

from models import Habit, Periodicity


def list_all_habits(habits: List[Habit]) -> List[Habit]:
    """Return all habits (pure function)."""
    return habits[:]  # return a copy to avoid side effects


def list_habits_by_periodicity(habits: List[Habit], periodicity: Periodicity) -> List[Habit]:
    """Return only habits with the given periodicity."""
    return [habit for habit in habits if habit.periodicity == periodicity]


def calculate_streak(completions: List[datetime], periodicity: Periodicity) -> int:
    """Calculate the current streak for a habit based on its completions."""
    if not completions:
        return 0

    # Sort completions by date
    sorted_completions = sorted(completions)
    streak = 1
    max_streak = 1

    for i in range(1, len(sorted_completions)):
        prev = sorted_completions[i-1]
        current = sorted_completions[i]

        # Calculate expected next date
        if periodicity == Periodicity.DAILY:
            expected = prev + timedelta(days=1)
        else:  # WEEKLY
            expected = prev + timedelta(weeks=1)

        # If current completion is exactly the expected next period
        if current.date() == expected.date():
            streak += 1
            max_streak = max(max_streak, streak)
        else:
            streak = 1  # reset streak

    return max_streak


def longest_streak_for_habit(habit: Habit) -> int:
    """Return the longest streak for a single habit (pure function)."""
    return calculate_streak(habit.completions, habit.periodicity)


def longest_streak_all(habits: List[Habit]) -> int:
    """Return the longest streak among all habits."""
    if not habits:
        return 0
    return max(longest_streak_for_habit(habit) for habit in habits)


# Optional: Run this file directly for quick testing
if __name__ == "__main__":
    print("✅ Analytics module loaded successfully.")
    print("Pure functions ready for use.")