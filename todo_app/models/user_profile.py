"""
UserProfile model for gamification data.

This module defines the UserProfile entity that tracks user statistics,
gamification metrics, and achievement progress.
"""

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict


@dataclass
class UserProfile:
    """
    User profile with gamification data.

    Attributes:
        total_xp: Total experience points earned
        current_streak: Current consecutive days with completions
        longest_streak: Longest streak ever achieved
        badges: List of earned badge names
        completion_history: Dict mapping dates to completion counts
        last_completion_date: Date of most recent task completion
    """
    total_xp: int = 0
    current_streak: int = 0
    longest_streak: int = 0
    badges: List[str] = field(default_factory=list)
    completion_history: Dict[str, int] = field(default_factory=dict)
    last_completion_date: date = field(default_factory=date.today)

    def add_xp(self, points: int) -> int:
        """
        Add experience points to profile.

        Args:
            points: XP points to add

        Returns:
            New total XP
        """
        self.total_xp += points
        return self.total_xp

    def update_completion_history(self, completion_date: date) -> None:
        """
        Record a task completion for a specific date.

        Args:
            completion_date: Date when task was completed
        """
        date_key = completion_date.isoformat()
        self.completion_history[date_key] = self.completion_history.get(date_key, 0) + 1
        self.last_completion_date = completion_date

    def award_badge(self, badge_name: str) -> bool:
        """
        Award a badge to the user.

        Args:
            badge_name: Name of badge to award

        Returns:
            True if badge newly awarded, False if already earned
        """
        if badge_name not in self.badges:
            self.badges.append(badge_name)
            return True
        return False

    def has_badge(self, badge_name: str) -> bool:
        """
        Check if user has a specific badge.

        Args:
            badge_name: Badge name to check

        Returns:
            True if badge earned, False otherwise
        """
        return badge_name in self.badges
