"""
GamificationAgent Sub-Agent for XP, streaks, and badges.

This agent manages the gamification system including experience points,
daily streaks, and achievement badges.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional

from todo_app.models.user_profile import UserProfile
from todo_app.models.task import Task


class GamificationAgent:
    """
    Sub-Agent responsible for gamification features.

    Manages XP calculation, streak tracking, and badge awards based on
    task completion patterns and timing.
    """

    # XP Constants
    BASE_XP = 10
    BEFORE_DUE_BONUS = 25
    EARLY_MORNING_BONUS = 15  # Completed before 8 AM

    # Badge Definitions
    BADGES = {
        "early_bird": {
            "name": "🌅 Early Bird",
            "description": "Complete a task before 8 AM"
        },
        "streak_7": {
            "name": "🔥 Week Warrior",
            "description": "Maintain a 7-day streak"
        },
        "streak_30": {
            "name": "🏆 Month Master",
            "description": "Maintain a 30-day streak"
        },
        "task_master_10": {
            "name": "⭐ Task Master",
            "description": "Complete 10 tasks"
        },
        "task_master_50": {
            "name": "💎 Task Legend",
            "description": "Complete 50 tasks"
        },
        "task_master_100": {
            "name": "👑 Task Champion",
            "description": "Complete 100 tasks"
        },
        "perfect_score": {
            "name": "💯 Perfect Score",
            "description": "Complete a task before due date and before 8 AM"
        }
    }

    def __init__(self, user_profile: Optional[UserProfile] = None):
        """
        Initialize GamificationAgent.

        Args:
            user_profile: UserProfile instance (creates new if None)
        """
        self.user_profile = user_profile or UserProfile()

    def calculate_xp_for_completion_skill(self, task: Task) -> int:
        """
        Calculate XP earned for completing a task.

        XP Calculation:
        - Base: 10 XP
        - Bonus: +25 XP if completed before due date
        - Bonus: +15 XP if completed before 8 AM

        Args:
            task: Completed task

        Returns:
            Total XP earned
        """
        xp = self.BASE_XP

        # Bonus for completing before due date
        if task.due_date and task.completed_at:
            if task.completed_at < task.due_date:
                xp += self.BEFORE_DUE_BONUS

        # Bonus for early morning completion (before 8 AM)
        if task.completed_at:
            if task.completed_at.hour < 8:
                xp += self.EARLY_MORNING_BONUS

        return xp

    def process_task_completion_skill(self, task: Task) -> Dict[str, any]:
        """
        Process a task completion and update gamification stats.

        Updates XP, streaks, completion history, and checks for badge awards.

        Args:
            task: Completed task

        Returns:
            Dictionary with:
            - xp_earned: XP points earned
            - new_badges: List of newly awarded badges
            - current_streak: Updated streak count
            - total_xp: Updated total XP
        """
        # Calculate and award XP
        xp_earned = self.calculate_xp_for_completion_skill(task)
        self.user_profile.add_xp(xp_earned)

        # Update completion history
        completion_date = task.completed_at.date() if task.completed_at else date.today()
        self.user_profile.update_completion_history(completion_date)

        # Update streak
        self._update_streak_skill(completion_date)

        # Check for new badges
        new_badges = self._check_and_award_badges_skill(task)

        return {
            "xp_earned": xp_earned,
            "new_badges": new_badges,
            "current_streak": self.user_profile.current_streak,
            "total_xp": self.user_profile.total_xp
        }

    def _update_streak_skill(self, completion_date: date) -> None:
        """
        Update the current streak based on completion date.

        Args:
            completion_date: Date of task completion
        """
        last_date = self.user_profile.last_completion_date
        today = date.today()

        # First completion ever
        if not last_date or self.user_profile.current_streak == 0:
            self.user_profile.current_streak = 1
            self.user_profile.last_completion_date = completion_date
            return

        # Calculate days difference
        days_diff = (completion_date - last_date).days

        if days_diff == 0:
            # Same day - no streak change
            pass
        elif days_diff == 1:
            # Consecutive day - increment streak
            self.user_profile.current_streak += 1
            if self.user_profile.current_streak > self.user_profile.longest_streak:
                self.user_profile.longest_streak = self.user_profile.current_streak
        else:
            # Streak broken - reset to 1
            self.user_profile.current_streak = 1

        self.user_profile.last_completion_date = completion_date

    def _check_and_award_badges_skill(self, task: Task) -> List[str]:
        """
        Check for and award any newly earned badges.

        Args:
            task: Completed task

        Returns:
            List of newly awarded badge names
        """
        new_badges = []

        # Early Bird badge (completed before 8 AM)
        if task.completed_at and task.completed_at.hour < 8:
            if self.user_profile.award_badge("early_bird"):
                new_badges.append("early_bird")

        # Perfect Score badge (before due date AND before 8 AM)
        if (task.due_date and task.completed_at and
            task.completed_at < task.due_date and
            task.completed_at.hour < 8):
            if self.user_profile.award_badge("perfect_score"):
                new_badges.append("perfect_score")

        # Streak badges
        if self.user_profile.current_streak >= 30:
            if self.user_profile.award_badge("streak_30"):
                new_badges.append("streak_30")
        elif self.user_profile.current_streak >= 7:
            if self.user_profile.award_badge("streak_7"):
                new_badges.append("streak_7")

        # Task completion count badges
        total_completions = sum(self.user_profile.completion_history.values())
        if total_completions >= 100:
            if self.user_profile.award_badge("task_master_100"):
                new_badges.append("task_master_100")
        elif total_completions >= 50:
            if self.user_profile.award_badge("task_master_50"):
                new_badges.append("task_master_50")
        elif total_completions >= 10:
            if self.user_profile.award_badge("task_master_10"):
                new_badges.append("task_master_10")

        return new_badges

    def get_statistics_skill(self) -> Dict[str, any]:
        """
        Get gamification statistics.

        Returns:
            Dictionary with:
            - total_xp: Total experience points
            - current_streak: Current daily streak
            - longest_streak: Longest streak achieved
            - total_completions: Total tasks completed
            - badges_earned: Number of badges earned
            - badge_list: List of badge names
        """
        total_completions = sum(self.user_profile.completion_history.values())

        return {
            "total_xp": self.user_profile.total_xp,
            "current_streak": self.user_profile.current_streak,
            "longest_streak": self.user_profile.longest_streak,
            "total_completions": total_completions,
            "badges_earned": len(self.user_profile.badges),
            "badge_list": self.user_profile.badges
        }

    def get_badge_info_skill(self, badge_key: str) -> Optional[Dict[str, str]]:
        """
        Get information about a specific badge.

        Args:
            badge_key: Badge identifier key

        Returns:
            Dictionary with 'name' and 'description', or None if not found
        """
        return self.BADGES.get(badge_key)

    def get_all_badges_skill(self) -> Dict[str, Dict[str, str]]:
        """
        Get information about all available badges.

        Returns:
            Dictionary mapping badge keys to badge info
        """
        return self.BADGES.copy()

    def get_earned_badges_with_info_skill(self) -> List[Dict[str, str]]:
        """
        Get detailed information about earned badges.

        Returns:
            List of dicts with badge 'key', 'name', and 'description'
        """
        earned = []
        for badge_key in self.user_profile.badges:
            badge_info = self.BADGES.get(badge_key)
            if badge_info:
                earned.append({
                    "key": badge_key,
                    "name": badge_info["name"],
                    "description": badge_info["description"]
                })
        return earned
