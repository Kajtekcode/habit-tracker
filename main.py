"""Main entry point for the Habit Tracker application.

This file launches the Command Line Interface (CLI).
"""

from cli import main as cli_main


def main():
    """Application entry point."""
    print("🚀 Starting Habit Tracker...\n")
    cli_main()


if __name__ == "__main__":
    main()