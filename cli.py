"""Command Line Interface (CLI) - User-friendly menu system.

This is the Presentation Layer that users interact with.
"""

from datetime import datetime
from models import Periodicity
from services import HabitService


def print_menu():
    """Display the main menu."""
    print("\n" + "="*50)
    print("          HABIT TRACKER")
    print("="*50)
    print("1. List all habits")
    print("2. List daily habits")
    print("3. List weekly habits")
    print("4. Create new habit")
    print("5. Complete a habit")
    print("6. Delete a habit")
    print("7. Show analytics")
    print("8. Exit")
    print("="*50)


def main():
    """Main CLI loop."""
    service = HabitService()
    print("✅ Welcome to Habit Tracker!")

    while True:
        print_menu()
        choice = input("\nEnter your choice (1-8): ").strip()

        if choice == "1":
            habits = service.list_all_habits()
            print(f"\n📋 All Habits ({len(habits)}):")
            for h in habits:
                print(f"   • {h.name} ({h.periodicity.value}) - {len(h.completions)} completions")

        elif choice == "2":
            habits = service.list_habits_by_periodicity(Periodicity.DAILY)
            print(f"\n📅 Daily Habits ({len(habits)}):")
            for h in habits:
                print(f"   • {h.name} - {len(h.completions)} completions")

        elif choice == "3":
            habits = service.list_habits_by_periodicity(Periodicity.WEEKLY)
            print(f"\n📅 Weekly Habits ({len(habits)}):")
            for h in habits:
                print(f"   • {h.name} - {len(h.completions)} completions")

        elif choice == "4":
            name = input("Enter habit name: ").strip()
            if not name:
                print("❌ Name cannot be empty!")
                continue
            print("1. Daily")
            print("2. Weekly")
            p_choice = input("Choose periodicity (1/2): ").strip()
            periodicity = Periodicity.DAILY if p_choice == "1" else Periodicity.WEEKLY
            habit = service.create_habit(name, periodicity)
            print(f"✅ Habit '{habit.name}' created successfully!")

        elif choice == "5":
            habits = service.list_all_habits()
            if not habits:
                print("❌ No habits found!")
                continue
            for i, h in enumerate(habits, 1):
                print(f"{i}. {h.name} ({h.periodicity.value})")
            try:
                idx = int(input("Choose habit number to complete: ")) - 1
                habit_id = habits[idx].id
                success = service.complete_habit(habit_id)
                print("✅ Habit completed!" if success else "❌ Failed to complete habit.")
            except:
                print("❌ Invalid choice!")

        elif choice == "6":
            habits = service.list_all_habits()
            if not habits:
                print("❌ No habits found!")
                continue
            for i, h in enumerate(habits, 1):
                print(f"{i}. {h.name}")
            try:
                idx = int(input("Choose habit number to delete: ")) - 1
                habit_id = habits[idx].id
                if service.delete_habit(habit_id):
                    print("✅ Habit deleted!")
                else:
                    print("❌ Failed to delete habit.")
            except:
                print("❌ Invalid choice!")

        elif choice == "7":
            habits = service.list_all_habits()
            from analytics import longest_streak_all, longest_streak_for_habit
            print(f"\n📊 Analytics:")
            print(f"   Total habits: {len(habits)}")
            print(f"   Longest streak (all): {longest_streak_all(habits)}")
            for habit in habits:
                print(f"   • {habit.name}: {longest_streak_for_habit(habit)}")

        elif choice == "8":
            print("👋 Goodbye!")
            break

        else:
            print("❌ Invalid choice! Please enter 1-8.")


if __name__ == "__main__":
    main()