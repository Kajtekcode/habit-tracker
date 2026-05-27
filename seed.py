"""Seed module - Creates predefined habits and sample data (4 weeks)."""

from datetime import datetime, timedelta
from models import Periodicity
from services import HabitService
from database import get_db_connection


def seed_sample_data() -> None:
    """Create 5 predefined habits with 4 weeks of realistic sample data."""
    service = HabitService()

    print("🧹 Clearing existing data...")
    # Clear database first
    with get_db_connection() as conn:
        conn.execute("DELETE FROM completions")
        conn.execute("DELETE FROM habits")
        conn.commit()

    print("🌱 Seeding new sample data...")

    # Create habits
    drink_water = service.create_habit("Drink water", Periodicity.DAILY)
    exercise = service.create_habit("Exercise", Periodicity.DAILY)
    clean_house = service.create_habit("Clean the house", Periodicity.WEEKLY)
    groceries = service.create_habit("Do grocery shopping", Periodicity.WEEKLY)
    read_book = service.create_habit("Read 30 minutes", Periodicity.DAILY)

    print(f"✅ Created 5 habits: Drink water, Exercise, Clean the house, "
          f"Do grocery shopping, Read 30 minutes")

    today = datetime.now()

    # === Drink water - very consistent daily ===
    if drink_water and drink_water.id:
        for i in range(24):                     # 24 day streak
            past_date = today - timedelta(days=i)
            service.complete_habit(drink_water.id, past_date)

    # === Exercise - good but with some gaps ===
    if exercise and exercise.id:
        for i in range(22):
            past_date = today - timedelta(days=i)
            service.complete_habit(exercise.id, past_date)

    # === Clean house - weekly ===
    if clean_house and clean_house.id:
        for i in range(4):
            past_date = today - timedelta(weeks=i)
            service.complete_habit(clean_house.id, past_date)

    # === Grocery shopping - weekly ===
    if groceries and groceries.id:
        for i in range(4):
            past_date = today - timedelta(weeks=i)
            service.complete_habit(groceries.id, past_date)

    # === Read 30 minutes - very consistent ===
    if read_book and read_book.id:
        for i in range(28):                     # 28 day streak
            past_date = today - timedelta(days=i)
            service.complete_habit(read_book.id, past_date)

    print("✅ Successfully seeded 5 habits with 4 weeks of realistic consecutive data!")


if __name__ == "__main__":
    seed_sample_data()