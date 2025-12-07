"""
Task model and related enums for the CLI Todo Application.

This module defines the core Task entity with status, priority, and recurrence
enumerations following the data model specification.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(Enum):
    """Task completion status."""
    PENDING = "pending"
    COMPLETED = "completed"


class Priority(Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Recurrence(Enum):
    """Task recurrence patterns."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Task:
    """
    Represents a single task in the todo list.

    Attributes:
        id: Unique task identifier (auto-generated)
        title: Brief task description (required)
        status: Current completion status (default: PENDING)
        priority: Task priority level (default: MEDIUM)
        description: Extended task details (optional)
        tags: Categorization labels (default: empty list)
        due_date: Task deadline (optional)
        created_at: Task creation timestamp (auto-generated)
        completed_at: Completion timestamp (set on completion)
        recurrence: Repetition pattern (default: NONE)
    """
    id: int
    title: str
    status: Status = Status.PENDING
    priority: Priority = Priority.MEDIUM
    description: Optional[str] = None
    tags: list[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE

    def is_overdue(self) -> bool:
        """
        Check if task is overdue.

        Returns:
            True if task is pending and past due date, False otherwise
        """
        if self.status == Status.COMPLETED or self.due_date is None:
            return False
        return datetime.now() > self.due_date

    def mark_completed(self) -> None:
        """Mark task as completed and set completion timestamp."""
        self.status = Status.COMPLETED
        self.completed_at = datetime.now()

    def mark_pending(self) -> None:
        """Mark task as pending and clear completion timestamp."""
        self.status = Status.PENDING
        self.completed_at = None
