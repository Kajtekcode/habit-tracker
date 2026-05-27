"""Integration tests - Test the full flow from Service to Database."""

import pytest
from datetime import datetime, timedelta
from models import Periodicity
from services import HabitService
from database import get_db_connection


@pytest.fixture
def service():
    """Fresh service with clean database for integration tests."""
    service = HabitService()
    # Clean database before each test
    with get_db_connection() as conn:
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.commit()
    return service


def test_full_habit_lifecycle(service: HabitService):
    """Test the complete flow: Create → Complete → List → Analytics"""
    
    # 1. Create a habit
    habit = service.create_habit("Integration Test Habit", Periodicity.DAILY)
    assert habit is not None
    assert habit.id is not None, "Habit should have an ID after creation"

    # 2. Complete the habit on 3 consecutive days
    today = datetime.now()
    service.complete_habit(habit.id, today - timedelta(days=2))
    service.complete_habit(habit.id, today - timedelta(days=1))
    service.complete_habit(habit.id, today)

    # 3. Retrieve and check data
    all_habits = service.list_all_habits()
    assert len(all_habits) == 1
    assert len(all_habits[0].completions) == 3

    # 4. Test analytics (functional part)
    from analytics import longest_streak_for_habit, longest_streak_all
    
    streak = longest_streak_for_habit(all_habits[0])
    assert streak == 3, f"Expected streak 3, got {streak}"

    all_streak = longest_streak_all(all_habits)
    assert all_streak == 3

    print("✅ Full integration test passed: Create → Complete → Analytics")


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])