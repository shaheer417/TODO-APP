"""
UIAgent Sub-Agent for terminal-based user interface rendering.

This agent owns all UI rendering using the Rich library for tables, menus,
prompts, and formatted output.
"""

from typing import Optional, Any
from datetime import datetime

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.text import Text

from todo_app.models.task import Task, Status, Priority


class UIAgent:
    """
    Sub-Agent responsible for all terminal UI rendering.

    Uses Rich library exclusively for beautiful CLI output with colors,
    tables, and formatted text.
    """

    def __init__(self):
        """Initialize UIAgent with Rich console."""
        # Force legacy_windows=False to use modern Windows terminal features
        # Set light background theme for minimalistic appearance
        self.console = Console(
            legacy_windows=False,
            force_terminal=True,
            style="black on white"  # Default black text on white background
        )

    def display_task_table_skill(self, tasks: list[Task], title: str = "Tasks") -> None:
        """
        Render tasks in a stunning, eye-catching table with vibrant colors.

        Args:
            tasks: List of tasks to display
            title: Table title (default: "Tasks")
        """
        if not tasks:
            self.console.print(f"\n[bold grey35]📭 No tasks to display. Add your first task to get started![/bold grey35]\n")
            return

        # Create table with minimalistic elegant style
        table = Table(
            title=f"[bold white on grey35] 📋 {title.upper()} [/bold white on grey35]",
            title_style="bold",
            show_header=True,
            header_style="bold white on grey50",
            border_style="grey50",
            row_styles=["on grey93", "on grey89"],  # Light grey alternating rows
            padding=(0, 1),
            expand=False
        )

        # Add columns with elegant minimalistic headers
        table.add_column("🆔", style="bold grey35", width=6, justify="center")
        table.add_column("📊 STATUS", width=14, justify="center")
        table.add_column("🎯 PRIORITY", width=16, justify="center")
        table.add_column("📝 TASK TITLE", style="bold black", width=45, no_wrap=False)
        table.add_column("🏷️  TAGS", style="grey35", width=22)
        table.add_column("📅 DUE DATE", width=20, justify="center")

        for task in tasks:
            # Status with light aesthetic styling
            if task.status == Status.COMPLETED:
                status_text = "[grey35 on green] ✅ DONE [/grey35 on green]"
                title_style = "dim strike"
            else:
                status_text = "[grey35 on yellow] ⏳ PENDING [/grey35 on yellow]"
                title_style = "bold black"

            # Priority with light aesthetic badges
            priority_badges = {
                Priority.HIGH: "[grey35 on red] 🔥 HIGH [/grey35 on red]",
                Priority.MEDIUM: "[grey35 on yellow] ⚡ MEDIUM [/grey35 on yellow]",
                Priority.LOW: "[grey35 on green] 💚 LOW [/grey35 on green]"
            }
            priority_text = priority_badges[task.priority]

            # Tags with light elegant styling
            if task.tags:
                tag_list = [f"[grey35 on grey89] {tag} [/grey35 on grey89]" for tag in task.tags[:3]]
                tags_text = " ".join(tag_list)
                if len(task.tags) > 3:
                    tags_text += f" [dim]+{len(task.tags)-3}[/dim]"
            else:
                tags_text = "[dim italic]no tags[/dim italic]"

            # Due date with light aesthetic overdue warning
            if task.due_date:
                due_str = task.due_date.strftime("%b %d, %I:%M %p")
                if task.is_overdue():
                    due_str = f"[grey35 on red] ⚠️  {due_str} [/grey35 on red]"
                else:
                    due_str = f"[green]{due_str}[/green]"
            else:
                due_str = "[dim italic]no deadline[/dim italic]"

            # Title with appropriate styling
            title_text = f"[{title_style}]{task.title}[/{title_style}]"

            # Add row with alternating background
            table.add_row(
                f"[bold grey35]{task.id}[/bold grey35]",
                status_text,
                priority_text,
                title_text,
                tags_text,
                due_str
            )

        self.console.print("\n")
        self.console.print(table)
        self.console.print("\n")

    def display_task_details_skill(self, task: Task) -> None:
        """
        Display detailed view of a single task.

        Args:
            task: Task object to display
        """
        # Status and priority with colors
        status_text = "✅ Completed" if task.status == Status.COMPLETED else "⏳ Pending"
        status_color = "green" if task.status == Status.COMPLETED else "yellow"

        priority_colors = {Priority.HIGH: "red", Priority.MEDIUM: "yellow", Priority.LOW: "green"}
        priority_color = priority_colors[task.priority]

        # Build detail text
        details = f"""
[bold grey35]ID:[/bold grey35] {task.id}
[bold grey35]Title:[/bold grey35] {task.title}
[bold grey35]Status:[/bold grey35] [{status_color}]{status_text}[/{status_color}]
[bold grey35]Priority:[/bold grey35] [{priority_color}]{task.priority.value.upper()}[/{priority_color}]
[bold grey35]Description:[/bold grey35] {task.description or 'No description'}
[bold grey35]Tags:[/bold grey35] {', '.join(task.tags) if task.tags else 'No tags'}
[bold grey35]Due Date:[/bold grey35] {task.due_date.strftime('%Y-%m-%d %H:%M') if task.due_date else 'No due date'}
[bold grey35]Created:[/bold grey35] {task.created_at.strftime('%Y-%m-%d %H:%M')}
[bold grey35]Completed:[/bold grey35] {task.completed_at.strftime('%Y-%m-%d %H:%M') if task.completed_at else 'Not completed'}
[bold grey35]Recurrence:[/bold grey35] {task.recurrence.value.upper()}
"""

        if task.is_overdue():
            details += "\n[red bold]⚠️ This task is OVERDUE![/red bold]"

        panel = Panel(details.strip(), title=f"Task Details - {task.id}", border_style="grey50")
        self.console.print("\n")
        self.console.print(panel)
        self.console.print("\n")

    def display_main_menu_skill(self) -> None:
        """Display the main application menu with minimalistic light styling."""
        # Create a minimalistic menu panel with elegant colors
        menu_table = Table(
            show_header=False,
            border_style="grey50",
            padding=(0, 2),
            expand=False,
            title="[bold white on grey35] 📋 MAIN MENU [/bold white on grey35]",
            title_style="bold",
            row_styles=["on grey93", "on grey89"]  # Light alternating backgrounds
        )

        menu_table.add_column("Option", style="bold grey35", width=10, justify="center")
        menu_table.add_column("Action", style="bold black", width=52)

        # Add menu items with elegant light aesthetic colors
        menu_items = [
            ("[grey35 on grey89] 1 [/grey35 on grey89]", "[grey35]📄 View All Tasks[/grey35]"),
            ("[grey35 on grey89] 2 [/grey35 on grey89]", "[grey35]➕ Add New Task[/grey35]"),
            ("[grey35 on grey89] 3 [/grey35 on grey89]", "[grey35]✏️  Update Task[/grey35]"),
            ("[grey35 on grey89] 4 [/grey35 on grey89]", "[grey35]🗑️  Delete Task[/grey35]"),
            ("[grey35 on grey89] 5 [/grey35 on grey89]", "[grey35]✅ Complete Task[/grey35]"),
            ("[grey35 on grey89] 6 [/grey35 on grey89]", "[grey35]🔍 Search Tasks[/grey35]"),
            ("[grey35 on grey89] 7 [/grey35 on grey89]", "[grey35]🔎 Filter Tasks[/grey35]"),
            ("[grey35 on grey89] 8 [/grey35 on grey89]", "[grey35]📖 View Task Details[/grey35]"),
            ("[white on grey50] 0 [/white on grey50]", "[grey35]🚪 Exit Application[/grey35]"),
        ]

        for option, action in menu_items:
            menu_table.add_row(option, action)

        self.console.print("\n")
        self.console.print(menu_table)
        self.console.print("\n")

    def prompt_input_skill(self, message: str, default: Optional[str] = None) -> str:
        """
        Prompt user for text input with elegant minimalistic styling.

        Args:
            message: Prompt message to display
            default: Default value if user presses Enter (optional)

        Returns:
            User input string
        """
        if default:
            return Prompt.ask(f"[bold grey35]➤[/bold grey35] [black]{message}[/black]", default=default)
        return Prompt.ask(f"[bold grey35]➤[/bold grey35] [black]{message}[/black]")

    def prompt_confirm_skill(self, message: str, default: bool = False) -> bool:
        """
        Prompt user for yes/no confirmation.

        Args:
            message: Confirmation message to display
            default: Default value if user presses Enter

        Returns:
            True if user confirmed, False otherwise
        """
        return Confirm.ask(message, default=default)

    def display_message_skill(self, message: str, style: str = "white") -> None:
        """
        Display a styled message to the user.

        Args:
            message: Message text to display
            style: Rich style (e.g., "green", "red", "yellow", "bold cyan")
        """
        self.console.print(f"\n[{style}]{message}[/{style}]\n")

    def display_error_skill(self, error_message: str) -> None:
        """
        Display a minimalistic error message.

        Args:
            error_message: Error text to display
        """
        error_panel = Panel(
            f"[bold black]{error_message}[/bold black]",
            title="[bold white on red] ❌ ERROR [/bold white on red]",
            border_style="bold red",
            padding=(1, 2)
        )
        self.console.print("\n")
        self.console.print(error_panel)
        self.console.print("\n")

    def display_success_skill(self, success_message: str) -> None:
        """
        Display a minimalistic success message.

        Args:
            success_message: Success text to display
        """
        success_panel = Panel(
            f"[bold black]{success_message}[/bold black]",
            title="[bold white on green] ✅ SUCCESS [/bold white on green]",
            border_style="bold green",
            padding=(1, 2)
        )
        self.console.print("\n")
        self.console.print(success_panel)
        self.console.print("\n")

    def display_header_skill(self, title: str) -> None:
        """
        Display a formatted header/banner.

        Args:
            title: Header text
        """
        panel = Panel(
            f"[bold black]{title}[/bold black]",
            style="grey50",
            expand=False
        )
        self.console.print("\n")
        self.console.print(panel)
        self.console.print("\n")

    def clear_screen_skill(self) -> None:
        """Clear the terminal screen with light background."""
        self.console.clear()
        # Set light background for entire screen
        self.console.print("[white]" + " " * 200 + "[/white]", end="")

    def display_statistics_skill(self, stats: dict[str, Any]) -> None:
        """
        Display minimalistic application statistics.

        Args:
            stats: Dictionary containing statistics (e.g., total, pending, completed)
        """
        # Create a minimalistic stats table with elegant colors
        stats_table = Table(
            show_header=False,
            border_style="grey50",
            padding=(0, 2),
            title="[bold white on grey35] 📊 TASK STATISTICS [/bold white on grey35]",
            title_style="bold",
            row_styles=["on grey93", "on grey89"]  # Light grey alternating rows
        )

        stats_table.add_column("Metric", style="bold grey35", width=25)
        stats_table.add_column("Count", style="bold black", width=15, justify="center")

        # Add stats with minimalistic styling
        total = stats.get('total', 0)
        pending = stats.get('pending', 0)
        completed = stats.get('completed', 0)
        overdue = stats.get('overdue', 0)

        stats_table.add_row(
            "[grey35]📝 Total Tasks[/grey35]",
            f"[grey35 on grey89] {total} [/grey35 on grey89]"
        )
        stats_table.add_row(
            "[yellow]⏳ Pending Tasks[/yellow]",
            f"[grey35 on yellow] {pending} [/grey35 on yellow]"
        )
        stats_table.add_row(
            "[green]✅ Completed Tasks[/green]",
            f"[grey35 on green] {completed} [/grey35 on green]"
        )

        if overdue > 0:
            stats_table.add_row(
                "[red]⚠️  Overdue Tasks[/red]",
                f"[grey35 on red] {overdue} [/grey35 on red]"
            )
        else:
            stats_table.add_row(
                "[dim]⚠️  Overdue Tasks[/dim]",
                f"[dim] {overdue} [/dim]"
            )

        self.console.print("\n")
        self.console.print(stats_table)
        self.console.print("\n")
