"""
FocusAgent Sub-Agent for Pomodoro timer functionality.

This agent manages focus mode with Pomodoro-style timers using Rich's
Live display for flicker-free countdown updates.
"""

import time
import threading
from datetime import datetime, timedelta
from typing import Optional, Callable

try:
    from rich.live import Live
    from rich.panel import Panel
    from rich.text import Text
    from rich.console import Console
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class FocusAgent:
    """
    Sub-Agent responsible for focus mode and Pomodoro timer.

    Provides distraction-free task focus with customizable timer durations
    and real-time countdown display.
    """

    # Default timer durations (in minutes)
    POMODORO_25 = 25
    POMODORO_50 = 50
    BREAK_5 = 5
    BREAK_15 = 15

    def __init__(self):
        """Initialize FocusAgent."""
        self.console = Console() if RICH_AVAILABLE else None
        self.timer_running = False
        self.timer_thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()

    def start_focus_session_skill(
        self,
        task_title: str,
        duration_minutes: int = POMODORO_25,
        on_complete: Optional[Callable] = None
    ) -> bool:
        """
        Start a focus session with Pomodoro timer.

        Displays live countdown with task information. User can press Ctrl+C
        to stop the timer early.

        Args:
            task_title: Title of task to focus on
            duration_minutes: Session duration in minutes (default: 25)
            on_complete: Optional callback function when timer completes

        Returns:
            True if session completed naturally, False if interrupted

        Example:
            >>> focus_agent.start_focus_session_skill("Write documentation", 25)
            [Displays live countdown for 25 minutes]
        """
        if not RICH_AVAILABLE:
            raise RuntimeError("Rich library required for focus mode")

        if self.timer_running:
            return False

        self.timer_running = True
        self.stop_event.clear()

        try:
            completed = self._run_timer_skill(task_title, duration_minutes)
            if completed and on_complete:
                on_complete()
            return completed
        finally:
            self.timer_running = False

    def _run_timer_skill(self, task_title: str, duration_minutes: int) -> bool:
        """
        Run the timer with live countdown display.

        Args:
            task_title: Task being focused on
            duration_minutes: Timer duration

        Returns:
            True if completed, False if interrupted
        """
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        total_seconds = duration_minutes * 60

        try:
            with Live(self._generate_timer_panel(task_title, total_seconds, total_seconds),
                     refresh_per_second=1, console=self.console) as live:
                while datetime.now() < end_time:
                    if self.stop_event.is_set():
                        return False

                    remaining = (end_time - datetime.now()).total_seconds()
                    if remaining <= 0:
                        break

                    # Update display
                    live.update(self._generate_timer_panel(
                        task_title,
                        int(remaining),
                        total_seconds
                    ))

                    time.sleep(1)

            # Timer completed
            self._show_completion_message_skill(task_title)
            return True

        except KeyboardInterrupt:
            self._show_interruption_message_skill(task_title)
            return False

    def _generate_timer_panel(
        self,
        task_title: str,
        remaining_seconds: int,
        total_seconds: int
    ) -> Panel:
        """
        Generate Rich panel for timer display.

        Args:
            task_title: Task title
            remaining_seconds: Seconds remaining
            total_seconds: Total session seconds

        Returns:
            Rich Panel with timer information
        """
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60

        # Calculate progress
        progress_percent = ((total_seconds - remaining_seconds) / total_seconds) * 100
        progress_bar_length = 40
        filled = int((progress_percent / 100) * progress_bar_length)
        progress_bar = "█" * filled + "░" * (progress_bar_length - filled)

        # Color based on time remaining
        if remaining_seconds > total_seconds * 0.5:
            color = "green"
        elif remaining_seconds > total_seconds * 0.25:
            color = "yellow"
        else:
            color = "red"

        content = Text()
        content.append("🎯 FOCUS MODE\n\n", style="bold cyan")
        content.append(f"Task: {task_title}\n\n", style="bold white")
        content.append(f"Time Remaining: ", style="white")
        content.append(f"{minutes:02d}:{seconds:02d}\n\n", style=f"bold {color}")
        content.append(f"[{progress_bar}]\n\n", style=color)
        content.append(f"Progress: {progress_percent:.1f}%\n\n", style="dim")
        content.append("Press Ctrl+C to stop", style="dim italic")

        return Panel(content, border_style="cyan", expand=False)

    def _show_completion_message_skill(self, task_title: str) -> None:
        """
        Display completion message when timer finishes.

        Args:
            task_title: Completed task title
        """
        message = Text()
        message.append("\n🎉 Focus Session Complete! 🎉\n\n", style="bold green")
        message.append(f"Task: {task_title}\n", style="white")
        message.append("Great work! Time for a break.\n", style="dim")

        panel = Panel(message, border_style="green", expand=False)
        self.console.print("\n")
        self.console.print(panel)
        self.console.print("\n")

    def _show_interruption_message_skill(self, task_title: str) -> None:
        """
        Display message when timer is interrupted.

        Args:
            task_title: Task title
        """
        message = Text()
        message.append("\n⏸️  Focus Session Interrupted\n\n", style="bold yellow")
        message.append(f"Task: {task_title}\n", style="white")
        message.append("Don't worry, you can try again!\n", style="dim")

        panel = Panel(message, border_style="yellow", expand=False)
        self.console.print("\n")
        self.console.print(panel)
        self.console.print("\n")

    def stop_timer_skill(self) -> None:
        """Stop the currently running timer."""
        self.stop_event.set()

    def is_timer_running_skill(self) -> bool:
        """
        Check if timer is currently running.

        Returns:
            True if timer active, False otherwise
        """
        return self.timer_running

    def get_preset_durations_skill(self) -> dict[str, int]:
        """
        Get preset timer durations.

        Returns:
            Dictionary mapping preset names to minutes
        """
        return {
            "pomodoro_25": self.POMODORO_25,
            "pomodoro_50": self.POMODORO_50,
            "break_5": self.BREAK_5,
            "break_15": self.BREAK_15
        }

    def start_break_skill(self, duration_minutes: int = BREAK_5) -> bool:
        """
        Start a break timer.

        Args:
            duration_minutes: Break duration (default: 5 minutes)

        Returns:
            True if break completed, False if interrupted
        """
        return self.start_focus_session_skill(
            "☕ Break Time",
            duration_minutes
        )
