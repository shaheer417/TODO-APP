"""
AnalyticsAgent Sub-Agent for metrics and visualizations.

This agent provides analytics, statistics, and CLI-based charts for
task completion patterns and productivity insights.
"""

from datetime import datetime, date, timedelta
from typing import List, Dict, Optional
from collections import defaultdict

try:
    from rich.console import Console
    from rich.table import Table
    from rich.text import Text
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from todo_app.models.task import Task, Status


class AnalyticsAgent:
    """
    Sub-Agent responsible for analytics and productivity metrics.

    Generates statistics, insights, and ASCII-based charts for task
    completion patterns.
    """

    def __init__(self):
        """Initialize AnalyticsAgent."""
        self.console = Console() if RICH_AVAILABLE else None

    def calculate_metrics_skill(self, tasks: List[Task]) -> Dict[str, any]:
        """
        Calculate comprehensive productivity metrics.

        Args:
            tasks: List of all tasks

        Returns:
            Dictionary with metrics:
            - tasks_today: Tasks completed today
            - tasks_this_week: Tasks completed this week
            - overdue_count: Number of overdue tasks
            - completion_rate: Percentage of completed tasks
            - avg_completion_time: Average time to complete (hours)
            - most_productive_day: Day with most completions
            - most_productive_hour: Hour with most completions
        """
        now = datetime.now()
        today = now.date()
        week_start = today - timedelta(days=today.weekday())

        metrics = {
            "tasks_today": 0,
            "tasks_this_week": 0,
            "overdue_count": 0,
            "completion_rate": 0.0,
            "avg_completion_time": 0.0,
            "most_productive_day": None,
            "most_productive_hour": None
        }

        if not tasks:
            return metrics

        # Count completions
        completed_tasks = [t for t in tasks if t.status == Status.COMPLETED]
        total_tasks = len(tasks)
        completed_count = len(completed_tasks)

        # Completion rate
        metrics["completion_rate"] = (completed_count / total_tasks * 100) if total_tasks > 0 else 0.0

        # Tasks today and this week
        for task in completed_tasks:
            if task.completed_at:
                completion_date = task.completed_at.date()
                if completion_date == today:
                    metrics["tasks_today"] += 1
                if completion_date >= week_start:
                    metrics["tasks_this_week"] += 1

        # Overdue count
        metrics["overdue_count"] = sum(1 for t in tasks if t.is_overdue())

        # Average completion time
        completion_times = []
        for task in completed_tasks:
            if task.completed_at:
                time_to_complete = (task.completed_at - task.created_at).total_seconds() / 3600  # hours
                completion_times.append(time_to_complete)

        if completion_times:
            metrics["avg_completion_time"] = sum(completion_times) / len(completion_times)

        # Most productive day and hour
        day_counts = defaultdict(int)
        hour_counts = defaultdict(int)

        for task in completed_tasks:
            if task.completed_at:
                day_counts[task.completed_at.strftime("%A")] += 1
                hour_counts[task.completed_at.hour] += 1

        if day_counts:
            metrics["most_productive_day"] = max(day_counts.items(), key=lambda x: x[1])[0]
        if hour_counts:
            metrics["most_productive_hour"] = max(hour_counts.items(), key=lambda x: x[1])[0]

        return metrics

    def generate_weekly_chart_skill(self, tasks: List[Task]) -> str:
        """
        Generate ASCII bar chart for weekly task completions.

        Args:
            tasks: List of all tasks

        Returns:
            ASCII art string representing weekly completion chart
        """
        # Get completions for last 7 days
        today = date.today()
        daily_counts = {}

        for i in range(7):
            day = today - timedelta(days=6-i)
            daily_counts[day] = 0

        # Count completions per day
        for task in tasks:
            if task.status == Status.COMPLETED and task.completed_at:
                completion_date = task.completed_at.date()
                if completion_date in daily_counts:
                    daily_counts[completion_date] += 1

        # Generate chart
        max_count = max(daily_counts.values()) if daily_counts.values() else 1
        chart_lines = []

        chart_lines.append("\n📊 Weekly Completion Chart (Last 7 Days)\n")
        chart_lines.append("=" * 50)

        for day, count in daily_counts.items():
            # Calculate bar length (max 30 chars)
            bar_length = int((count / max_count) * 30) if max_count > 0 else 0
            bar = "█" * bar_length

            # Color based on count
            if count == 0:
                color = "dim"
            elif count >= max_count * 0.7:
                color = "green"
            elif count >= max_count * 0.4:
                color = "yellow"
            else:
                color = "red"

            day_name = day.strftime("%a %m/%d")
            chart_lines.append(f"{day_name}: {bar} ({count})")

        chart_lines.append("=" * 50)

        return "\n".join(chart_lines)

    def get_priority_distribution_skill(self, tasks: List[Task]) -> Dict[str, int]:
        """
        Get distribution of tasks by priority.

        Args:
            tasks: List of tasks

        Returns:
            Dictionary mapping priority levels to counts
        """
        distribution = {"high": 0, "medium": 0, "low": 0}

        for task in tasks:
            distribution[task.priority.value] += 1

        return distribution

    def get_tag_statistics_skill(self, tasks: List[Task]) -> List[Dict[str, any]]:
        """
        Get statistics for each tag.

        Args:
            tasks: List of tasks

        Returns:
            List of dicts with tag statistics (sorted by usage)
        """
        tag_stats = defaultdict(lambda: {"total": 0, "completed": 0, "pending": 0})

        for task in tasks:
            for tag in task.tags:
                tag_stats[tag]["total"] += 1
                if task.status == Status.COMPLETED:
                    tag_stats[tag]["completed"] += 1
                else:
                    tag_stats[tag]["pending"] += 1

        # Convert to list and sort by total usage
        stats_list = [
            {
                "tag": tag,
                "total": stats["total"],
                "completed": stats["completed"],
                "pending": stats["pending"],
                "completion_rate": (stats["completed"] / stats["total"] * 100) if stats["total"] > 0 else 0
            }
            for tag, stats in tag_stats.items()
        ]

        return sorted(stats_list, key=lambda x: x["total"], reverse=True)

    def display_analytics_dashboard_skill(self, tasks: List[Task]) -> None:
        """
        Display comprehensive analytics dashboard.

        Args:
            tasks: List of all tasks
        """
        if not RICH_AVAILABLE:
            return

        metrics = self.calculate_metrics_skill(tasks)

        # Create analytics table
        table = Table(title="📊 Analytics Dashboard", title_style="bold cyan")
        table.add_column("Metric", style="cyan", width=30)
        table.add_column("Value", style="white", width=20)

        # Add metrics to table
        table.add_row("Tasks Completed Today", str(metrics["tasks_today"]))
        table.add_row("Tasks Completed This Week", str(metrics["tasks_this_week"]))
        table.add_row("Overdue Tasks", f"[red]{metrics['overdue_count']}[/red]" if metrics["overdue_count"] > 0 else "0")
        table.add_row("Completion Rate", f"{metrics['completion_rate']:.1f}%")
        table.add_row("Avg. Completion Time", f"{metrics['avg_completion_time']:.1f} hours")

        if metrics["most_productive_day"]:
            table.add_row("Most Productive Day", metrics["most_productive_day"])
        if metrics["most_productive_hour"] is not None:
            hour_12 = metrics["most_productive_hour"] % 12 or 12
            am_pm = "AM" if metrics["most_productive_hour"] < 12 else "PM"
            table.add_row("Most Productive Hour", f"{hour_12}:00 {am_pm}")

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")

        # Display weekly chart
        chart = self.generate_weekly_chart_skill(tasks)
        self.console.print(chart)
        self.console.print("\n")

    def get_completion_trend_skill(self, tasks: List[Task], days: int = 30) -> List[Dict[str, any]]:
        """
        Get completion trend for specified number of days.

        Args:
            tasks: List of tasks
            days: Number of days to analyze (default: 30)

        Returns:
            List of dicts with date and count
        """
        today = date.today()
        trend = []

        for i in range(days):
            day = today - timedelta(days=days-1-i)
            count = sum(
                1 for t in tasks
                if t.status == Status.COMPLETED and t.completed_at and t.completed_at.date() == day
            )
            trend.append({"date": day.isoformat(), "count": count})

        return trend

    def get_performance_insights_skill(self, tasks: List[Task]) -> List[str]:
        """
        Generate performance insights and suggestions.

        Args:
            tasks: List of tasks

        Returns:
            List of insight strings
        """
        insights = []
        metrics = self.calculate_metrics_skill(tasks)

        # Completion rate insights
        if metrics["completion_rate"] >= 80:
            insights.append("🎉 Excellent! You're completing most of your tasks.")
        elif metrics["completion_rate"] >= 50:
            insights.append("👍 Good progress! Try to complete more pending tasks.")
        else:
            insights.append("💪 Keep going! Focus on completing your pending tasks.")

        # Overdue insights
        if metrics["overdue_count"] > 0:
            insights.append(f"⚠️ You have {metrics['overdue_count']} overdue task(s). Prioritize these!")

        # Productivity pattern insights
        if metrics["most_productive_hour"] is not None:
            hour = metrics["most_productive_hour"]
            if hour < 12:
                insights.append("🌅 You're most productive in the morning!")
            elif hour < 17:
                insights.append("☀️ You're most productive in the afternoon!")
            else:
                insights.append("🌙 You're most productive in the evening!")

        # Today's performance
        if metrics["tasks_today"] == 0:
            insights.append("📝 No tasks completed today yet. Start now!")
        elif metrics["tasks_today"] >= 5:
            insights.append(f"🔥 Amazing! You've completed {metrics['tasks_today']} tasks today!")

        return insights
