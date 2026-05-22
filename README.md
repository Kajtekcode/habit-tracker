# Habit Tracker

A clean, maintainable Habit Tracking Application built in Python as part of the **Object Oriented and Functional Programming** course.

## Features

- **OOP Design**: Core `Habit` class using modern Python (dataclass + Enum)
- **Persistence**: SQLite database with Repository Pattern
- **Business Logic**: Clean service layer
- **Analytics**: Pure functional programming module (no side effects)
- **CLI**: User-friendly command line interface
- **Test Fixture**: 5 predefined habits with 4 weeks of realistic sample data
- **Testing**: Comprehensive unit tests with pytest

## Technologies Used

- Python 3.11+
- SQLite3 (standard library)
- dataclasses, Enum, type hints
- pytest (for testing)

## Project Structure

habit_tracker/
├── main.py                 # Application entry point
├── cli.py                  # Command Line Interface
├── services.py             # Business Logic Layer
├── repository.py           # Data Access Layer (Repository Pattern)
├── database.py             # SQLite database setup
├── models.py               # Domain Model (Habit class)
├── analytics.py            # Pure Functional Analytics
├── seed.py                 # Test fixture with sample data
├── tests/                  # Unit tests
├── requirements.txt
└── habits.db               # Database file (auto-generated)


## Installation & Setup

1. **Clone the repository**
   git clone https://github.com/Kajtekcode/habit-tracker.git
   cd habit-tracker

2. **Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python main.py

## How to Use
After starting the app, you will see a menu with the following options:

1. List all habits
2. List daily habits
3. List weekly habits
4. Create new habit
5. Complete a habit
6. Delete a habit
7. Show analytics (longest streaks)
8. Exit

## Seeding Sample Data
To load the 5 predefined habits with 4 weeks of sample data:
python seed.py

## Running Tests
**Run all tests
pytest tests/ -v

**Run specific test file
pytest tests/test_models.py -v