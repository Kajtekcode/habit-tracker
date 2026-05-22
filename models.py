"""Domain model layer - Core Habit class using OOP (dataclass).

This module encodes the central business object of the application exactly
as required by the assignment and your Phase 1 concept document.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import List


class Periodicity(Enum):
    """Enumeration for habit periodicity (daily or weekly)."""
    DAILY = "daily"
    WEEKLY = "weekly"


@dataclass
class Habit:
    """Core Habit class using modern Python OOP (dataclass).

    Attributes:
        name: Human-readable name of the habit (required)
        periodicity: DAILY or WEEKLY (enum, required)
        id: Unique identifier (None until saved in DB)
        created_at: Timestamp when the habit was created
        completions: List of datetime objects when the habit was checked off
    """

    # Required fields (no default) must come first
    name: str
    periodicity: Periodicity

    # Fields with defaults come after
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)
    completions: List[datetime] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate input data after object creation."""
        if not self.name or not isinstance(self.name, str):
            raise ValueError("Habit name must be a non-empty string")
        if not isinstance(self.periodicity, Periodicity):
            raise ValueError("periodicity must be a Periodicity enum")

    def complete(self, timestamp: datetime | None = None) -> None:
        """Mark the habit as completed at the given (or current) time.

        This is the main method users will call when they check off a habit.
        """
        if timestamp is None:
            timestamp = datetime.now()
        self.completions.append(timestamp)

    def __repr__(self) -> str:
        """Nice string representation for debugging and logging."""
        return (
            f"Habit(id={self.id}, name='{self.name}', "
            f"periodicity={self.periodicity.value}, "
            f"completions={len(self.completions)})"
        )