"""Seed module - Creates predefined habits and sample data (4 weeks).

This fulfills the assignment requirement for test fixture data.
"""

from datetime import datetime, timedelta
from models import Periodicity
from services import HabitService


def seed_sample_data() -> None:
    """Create 5 predefined habits with 4 weeks of realistic sample data."""
    service = HabitService()

    # Clear existing data first
    print("🧹 Clearing existing data...")

    # 1. Daily habits
    drink_water = service.create_habit("Drink water", Periodicity.DAILY)
    exercise = service.create_habit("Exercise", Periodicity.DAILY)
    
    # 2. Weekly habits
    clean_house = service.create_habit("Clean the house", Periodicity.WEEKLY)
    groceries = service.create_habit("Do grocery shopping", Periodicity.WEEKLY)
    read_book = service.create_habit("Read 30 minutes", Periodicity.DAILY)

    print(f"✅ Created 5 habits: {drink_water.name}, {exercise.name}, {clean_house.name}, {groceries.name}, {read_book.name}")

    # Add 4 weeks of sample completions (realistic patterns)
    today = datetime.now()
    
    # Drink water - very consistent (almost perfect streak)
    for i in range(28):
        if i % 7 != 3:  # miss every Sunday
            service.complete_habit(drink_water.id, today - timedelta(days=i))  # type: ignore

    # Exercise - good but with some gaps
    for i in range(28):
        if i % 5 != 0:  # miss every 5th day
            service.complete_habit(exercise.id, today - timedelta(days=i))  # type: ignore

    # Clean house - weekly (completed most Saturdays)
    for i in range(4):
        service.complete_habit(clean_house.id, today - timedelta(weeks=i))  # type: ignore

    # Grocery shopping - weekly
    for i in range(4):
        service.complete_habit(groceries.id, today - timedelta(weeks=i, days=1))  # type: ignore

    # Read book - very consistent daily
    for i in range(28):
        service.complete_habit(read_book.id, today - timedelta(days=i))  # type: ignore

    print("✅ Successfully seeded 5 habits with 4 weeks of sample data!")


if __name__ == "__main__":
    seed_sample_data()