"""
Main entry point for the CLI Todo Application.

This module initializes all Sub-Agents and runs the main menu loop.
"""

import sys
import os

# Fix Windows console encoding for Unicode/emoji support
if sys.platform == 'win32':
    # Set console to UTF-8 mode
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    # Set environment variable for UTF-8
    os.environ['PYTHONIOENCODING'] = 'utf-8'

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from datetime import datetime
from typing import Optional

from todo_app.agents.task_manager import TaskManager
from todo_app.agents.ui_agent import UIAgent
from todo_app.agents.email_agent import EmailAgent
from todo_app.models.task import Priority, Status, Recurrence


class TodoApp:
    """
    Main application controller.

    Orchestrates all Sub-Agents and handles the main menu loop.
    """

    def __init__(self):
        """Initialize application with all Sub-Agents."""
        self.task_manager = TaskManager()
        self.ui_agent = UIAgent()
        self.email_agent = EmailAgent()
        self.running = True

    def run(self) -> None:
        """Start the application main loop with light background."""
        self.ui_agent.clear_screen_skill()

        # Set light background theme
        from rich.panel import Panel

        # Display minimalistic ASCII art header with elegant aesthetic
        header_art = """[grey50]╔═══════════════════════════════════════════════════════════════╗[/grey50]
[grey50]║[/grey50]  [bold white on grey35]                   TODO MASTER                        [/bold white on grey35]  [grey50]║[/grey50]
[grey50]║[/grey50]  [grey35]         🚀 Your Ultimate Productivity Companion 🚀[/grey35]       [grey50]║[/grey50]
[grey50]╚═══════════════════════════════════════════════════════════════╝[/grey50]"""

        # Print with white background
        self.ui_agent.console.print(f"[black on white]{header_art}[/black on white]")

        while self.running:
            self.ui_agent.display_main_menu_skill()
            choice = self.ui_agent.prompt_input_skill("Enter your choice")

            self._handle_menu_choice(choice)

    def _handle_menu_choice(self, choice: str) -> None:
        """
        Route menu choice to appropriate handler.

        Args:
            choice: User's menu selection
        """
        handlers = {
            "1": self._view_all_tasks,
            "2": self._add_task,
            "3": self._update_task,
            "4": self._delete_task,
            "5": self._complete_task,
            "6": self._search_tasks,
            "7": self._filter_tasks,
            "8": self._view_task_details,
            "0": self._exit_app
        }

        handler = handlers.get(choice)
        if handler:
            try:
                handler()
            except Exception as e:
                self.ui_agent.display_error_skill(f"An error occurred: {str(e)}")
        else:
            self.ui_agent.display_error_skill("Invalid choice. Please try again.")

    def _view_all_tasks(self) -> None:
        """Display all tasks in a table."""
        tasks = self.task_manager.get_all_tasks_skill()

        # Check and send email notifications for tasks that need them
        notifications_sent = self.email_agent.check_and_notify_tasks_skill(tasks)
        if notifications_sent > 0:
            self.ui_agent.display_message_skill(
                f"📧 {notifications_sent} email notification(s) sent for urgent tasks",
                "grey35"
            )

        # Display statistics
        pending = len([t for t in tasks if t.status == Status.PENDING])
        completed = len([t for t in tasks if t.status == Status.COMPLETED])
        overdue = len(self.task_manager.get_overdue_tasks_skill())

        stats = {
            "total": len(tasks),
            "pending": pending,
            "completed": completed,
            "overdue": overdue
        }
        self.ui_agent.display_statistics_skill(stats)

        # Display tasks
        self.ui_agent.display_task_table_skill(tasks, "All Tasks")

    def _add_task(self) -> None:
        """Add a new task via user prompts."""
        self.ui_agent.display_header_skill("Add New Task")

        # Get task details
        title = self.ui_agent.prompt_input_skill("Enter task title")
        if not title:
            self.ui_agent.display_error_skill("Title cannot be empty")
            return

        description = self.ui_agent.prompt_input_skill("Enter description (optional)")
        description = description if description else None

        # Priority
        priority_input = self.ui_agent.prompt_input_skill(
            "Enter priority (low/medium/high)",
            default="medium"
        ).lower()
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
        priority = priority_map.get(priority_input, Priority.MEDIUM)

        # Tags
        tags_input = self.ui_agent.prompt_input_skill("Enter tags (comma-separated, optional)")
        tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

        # Due date
        due_date_input = self.ui_agent.prompt_input_skill(
            "Enter due date (YYYY-MM-DD HH:MM, optional)"
        )
        due_date = None
        if due_date_input:
            try:
                due_date = datetime.strptime(due_date_input, "%Y-%m-%d %H:%M")
            except ValueError:
                self.ui_agent.display_error_skill("Invalid date format. Due date not set.")

        # Recurrence
        recurrence_input = self.ui_agent.prompt_input_skill(
            "Enter recurrence (none/daily/weekly/monthly)",
            default="none"
        ).lower()
        recurrence_map = {
            "none": Recurrence.NONE,
            "daily": Recurrence.DAILY,
            "weekly": Recurrence.WEEKLY,
            "monthly": Recurrence.MONTHLY
        }
        recurrence = recurrence_map.get(recurrence_input, Recurrence.NONE)

        # Create task
        task = self.task_manager.add_task_skill(
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )

        self.ui_agent.display_success_skill(f"Task created successfully! ID: {task.id}")
        self.ui_agent.display_task_details_skill(task)

        # Check if email notification should be sent for this task
        self.email_agent.check_and_notify_task_skill(task)

    def _update_task(self) -> None:
        """Update an existing task."""
        self.ui_agent.display_header_skill("Update Task")

        task_id_input = self.ui_agent.prompt_input_skill("Enter task ID to update")
        try:
            task_id = int(task_id_input)
        except ValueError:
            self.ui_agent.display_error_skill("Invalid task ID")
            return

        task = self.task_manager.get_task_by_id_skill(task_id)
        if not task:
            self.ui_agent.display_error_skill(f"Task {task_id} not found")
            return

        # Show current task
        self.ui_agent.display_task_details_skill(task)

        # Get updates (press Enter to keep current value)
        title = self.ui_agent.prompt_input_skill(
            f"Enter new title (current: {task.title})"
        )
        description = self.ui_agent.prompt_input_skill(
            f"Enter new description (current: {task.description or 'None'})"
        )
        priority_input = self.ui_agent.prompt_input_skill(
            f"Enter new priority (current: {task.priority.value})"
        )
        tags_input = self.ui_agent.prompt_input_skill(
            f"Enter new tags (current: {', '.join(task.tags) if task.tags else 'None'})"
        )

        # Apply updates
        priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}

        updated_task = self.task_manager.update_task_skill(
            task_id=task_id,
            title=title if title else None,
            description=description if description else None,
            priority=priority_map.get(priority_input.lower()) if priority_input else None,
            tags=[tag.strip() for tag in tags_input.split(",")] if tags_input else None
        )

        if updated_task:
            self.ui_agent.display_success_skill("Task updated successfully!")
            self.ui_agent.display_task_details_skill(updated_task)

    def _delete_task(self) -> None:
        """Delete a task by ID."""
        self.ui_agent.display_header_skill("Delete Task")

        task_id_input = self.ui_agent.prompt_input_skill("Enter task ID to delete")
        try:
            task_id = int(task_id_input)
        except ValueError:
            self.ui_agent.display_error_skill("Invalid task ID")
            return

        task = self.task_manager.get_task_by_id_skill(task_id)
        if not task:
            self.ui_agent.display_error_skill(f"Task {task_id} not found")
            return

        # Show task and confirm deletion
        self.ui_agent.display_task_details_skill(task)
        confirm = self.ui_agent.prompt_confirm_skill("Are you sure you want to delete this task?")

        if confirm:
            success = self.task_manager.delete_task_skill(task_id)
            if success:
                self.ui_agent.display_success_skill(f"Task {task_id} deleted successfully!")
        else:
            self.ui_agent.display_message_skill("Deletion cancelled", "yellow")

    def _complete_task(self) -> None:
        """Mark a task as completed."""
        self.ui_agent.display_header_skill("Complete Task")

        task_id_input = self.ui_agent.prompt_input_skill("Enter task ID to complete")
        try:
            task_id = int(task_id_input)
        except ValueError:
            self.ui_agent.display_error_skill("Invalid task ID")
            return

        task = self.task_manager.complete_task_skill(task_id)
        if task:
            self.ui_agent.display_success_skill(f"Task {task_id} marked as completed!")
            self.ui_agent.display_task_details_skill(task)
        else:
            self.ui_agent.display_error_skill(f"Task {task_id} not found")

    def _search_tasks(self) -> None:
        """Search tasks by keyword."""
        self.ui_agent.display_header_skill("Search Tasks")

        query = self.ui_agent.prompt_input_skill("Enter search keyword")
        if not query:
            self.ui_agent.display_error_skill("Search query cannot be empty")
            return

        results = self.task_manager.search_tasks_skill(query)
        self.ui_agent.display_task_table_skill(results, f"Search Results for '{query}'")

    def _filter_tasks(self) -> None:
        """Filter tasks by status, priority, or tag."""
        self.ui_agent.display_header_skill("Filter Tasks")

        self.ui_agent.display_message_skill("Filter by: 1) Status  2) Priority  3) Tag", "grey35")
        choice = self.ui_agent.prompt_input_skill("Enter your choice")

        if choice == "1":
            status_input = self.ui_agent.prompt_input_skill(
                "Enter status (pending/completed)"
            ).lower()
            status_map = {"pending": Status.PENDING, "completed": Status.COMPLETED}
            status = status_map.get(status_input)
            if status:
                results = self.task_manager.filter_by_status_skill(status)
                self.ui_agent.display_task_table_skill(results, f"{status.value.upper()} Tasks")
            else:
                self.ui_agent.display_error_skill("Invalid status")

        elif choice == "2":
            priority_input = self.ui_agent.prompt_input_skill(
                "Enter priority (low/medium/high)"
            ).lower()
            priority_map = {"low": Priority.LOW, "medium": Priority.MEDIUM, "high": Priority.HIGH}
            priority = priority_map.get(priority_input)
            if priority:
                results = self.task_manager.filter_by_priority_skill(priority)
                self.ui_agent.display_task_table_skill(results, f"{priority.value.upper()} Priority Tasks")
            else:
                self.ui_agent.display_error_skill("Invalid priority")

        elif choice == "3":
            tag = self.ui_agent.prompt_input_skill("Enter tag")
            results = self.task_manager.filter_by_tag_skill(tag)
            self.ui_agent.display_task_table_skill(results, f"Tasks with tag '{tag}'")

        else:
            self.ui_agent.display_error_skill("Invalid choice")

    def _view_task_details(self) -> None:
        """View detailed information for a specific task."""
        self.ui_agent.display_header_skill("View Task Details")

        task_id_input = self.ui_agent.prompt_input_skill("Enter task ID")
        try:
            task_id = int(task_id_input)
        except ValueError:
            self.ui_agent.display_error_skill("Invalid task ID")
            return

        task = self.task_manager.get_task_by_id_skill(task_id)
        if task:
            self.ui_agent.display_task_details_skill(task)
        else:
            self.ui_agent.display_error_skill(f"Task {task_id} not found")

    def _exit_app(self) -> None:
        """Exit the application."""
        self.ui_agent.clear_screen_skill()
        self.ui_agent.display_message_skill("✨ Thank you for using TODO MASTER! ✨", "bold grey35")
        self.ui_agent.display_message_skill("🎯 Stay productive! See you soon! 👋", "bold grey35")
        self.running = False


def main():
    """Application entry point."""
    app = TodoApp()
    try:
        app.run()
    except KeyboardInterrupt:
        app.ui_agent.display_message_skill("\n\nApplication interrupted. Goodbye!", "yellow")
    except Exception as e:
        print(f"\nFatal error: {e}")


if __name__ == "__main__":
    main()
