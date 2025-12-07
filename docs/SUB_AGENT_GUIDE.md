
# Sub-Agent Implementation Guide

**Project**: In-Memory Python CLI Todo Application
**Architecture**: Sub-Agent/Skill Pattern
**Date**: 2025-12-05

---

## What is a Sub-Agent?

A **Sub-Agent** is a high-level class responsible for a complete functional domain. Think of it as a 
 service that owns all operations in a specific area.

**Key Principles**:
- **One agent = One responsibility** (e.g., TaskManager handles all task operations)
- **Each agent = One file** (e.g., `task_manager.py`)
- **Stateless design** (no side effects between calls)
- **Skills = Methods** (e.g., `add_task_skill()`, `search_tasks_skill()`)

---

## Your 8 Sub-Agents

| Agent | File | Responsibility |
|-------|------|----------------|
| **TaskManager** | `todo_app/agents/task_manager.py` | Task CRUD, search, filter, sort, recurring tasks |
| **UIAgent** | `todo_app/agents/ui_agent.py` | All terminal output using Rich library |
| **NLPAgent** | `todo_app/agents/nlp_agent.py` | Natural language parsing for dates and priorities |
| **VoiceAgent** | `todo_app/agents/voice_agent.py` | Speech-to-text conversion |
| **LanguageAgent** | `todo_app/agents/language_agent.py` | Multi-language support via JSON files |
| **GamificationAgent** | `todo_app/agents/gamification_agent.py` | XP, streaks, badges |
| **FocusAgent** | `todo_app/agents/focus_agent.py` | Pomodoro timer |
| **AnalyticsAgent** | `todo_app/agents/analytics_agent.py` | Metrics calculation and charts |

---

## Step-by-Step: Creating Your First Sub-Agent

### Step 1: Set Up Project Structure

```bash
# Navigate to your project directory
cd "D:\agentic ai projects\todo-hackathon"

# Create directory structure
mkdir todo_app
mkdir todo_app\models
mkdir todo_app\agents
mkdir todo_app\utils
mkdir todo_app\locales
mkdir tests
mkdir tests\unit
mkdir tests\integration
mkdir tests\fixtures
mkdir docs

# Create __init__.py files
type nul > todo_app\__init__.py
type nul > todo_app\models\__init__.py
type nul > todo_app\agents\__init__.py
type nul > todo_app\utils\__init__.py
```

### Step 2: Create Data Models (Foundation)

**File**: `todo_app/models/task.py`

```python
"""
Task data model for todo application.

This module defines the Task entity with all required fields and enumerations.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Status(Enum):
    """Task completion status."""
    PENDING = "Pending"
    COMPLETED = "Completed"


class Priority(Enum):
    """Task priority levels."""
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class Recurrence(Enum):
    """Task recurrence patterns."""
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique task identifier (auto-assigned)
        title: Task title (max 200 characters)
        description: Optional detailed description (max 1000 characters)
        status: Current task state (Pending or Completed)
        priority: Importance level (High, Medium, Low)
        tags: List of category tags for organization
        due_date: Optional deadline (timezone-aware datetime)
        created_at: Timestamp when task was created
        completed_at: Timestamp when task was completed (None if pending)
        recurrence: Repeat pattern for recurring tasks
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

    def __post_init__(self):
        """Validate task fields after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty")

        if len(self.title) > 200:
            raise ValueError("Task title cannot exceed 200 characters")

        if self.description and len(self.description) > 1000:
            raise ValueError("Task description cannot exceed 1000 characters")
```

### Step 3: Create Your First Sub-Agent (TaskManager)

**File**: `todo_app/agents/task_manager.py`

```python
"""
TaskManager Sub-Agent.

Responsible for all task-related operations including CRUD, search, filter, and sort.
Follows the Sub-Agent/Skill architecture pattern.
"""

from datetime import datetime, timezone, timedelta
from typing import Optional
from dateutil.relativedelta import relativedelta

from todo_app.models.task import Task, Status, Priority, Recurrence


class TaskManager:
    """
    Sub-Agent for task management operations.

    This agent owns all task CRUD operations, searching, filtering, sorting,
    and recurring task management. It maintains an in-memory list of tasks
    with a dict index for O(1) ID lookups.

    Attributes:
        tasks: List of all tasks (preserves insertion order)
        task_index: Dictionary mapping task IDs to Task objects
        next_id: Counter for auto-incrementing task IDs
    """

    def __init__(self):
        """Initialize TaskManager with empty task storage."""
        self.tasks: list[Task] = []
        self.task_index: dict[int, Task] = {}
        self.next_id: int = 1

    # ========== CRUD Skills ==========

    def add_task_skill(
        self,
        title: str,
        description: Optional[str] = None,
        priority: Priority = Priority.MEDIUM,
        tags: Optional[list[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence: Recurrence = Recurrence.NONE
    ) -> Task:
        """
        Create a new task with auto-generated ID and timestamps.

        Args:
            title: Task title (required, max 200 chars)
            description: Optional description (max 1000 chars)
            priority: Task priority (default: Medium)
            tags: List of category tags (default: empty list)
            due_date: Optional deadline (timezone-aware datetime)
            recurrence: Repeat pattern (default: None)

        Returns:
            Created Task object with assigned ID

        Raises:
            ValueError: If title is empty or exceeds limits

        Example:
            >>> task = task_manager.add_task_skill(
            ...     title="Complete report",
            ...     priority=Priority.HIGH,
            ...     tags=["work", "urgent"]
            ... )
        """
        # Create task with auto-increment ID
        task = Task(
            id=self.next_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence=recurrence
        )

        # Add to storage
        self.tasks.append(task)
        self.task_index[task.id] = task
        self.next_id += 1

        return task

    def get_task_skill(self, task_id: int) -> Optional[Task]:
        """
        Retrieve task by ID (O(1) lookup).

        Args:
            task_id: Unique task identifier

        Returns:
            Task object if found, None otherwise
        """
        return self.task_index.get(task_id)

    def update_task_skill(self, task_id: int, **kwargs) -> Task:
        """
        Update one or more fields of existing task.

        Args:
            task_id: ID of task to update
            **kwargs: Field names and new values
                     (title, description, priority, tags, due_date, recurrence)

        Returns:
            Updated Task object

        Raises:
            KeyError: If task_id not found
            ValueError: If field validation fails

        Example:
            >>> task = task_manager.update_task_skill(
            ...     5,
            ...     priority=Priority.LOW,
            ...     tags=["deferred"]
            ... )
        """
        task = self.task_index.get(task_id)
        if not task:
            raise KeyError(f"Task ID {task_id} not found")

        # Update allowed fields
        allowed_fields = {'title', 'description', 'priority', 'tags', 'due_date', 'recurrence'}
        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(task, field, value)

        # Validate updated task (will raise ValueError if invalid)
        task.__post_init__()

        return task

    def delete_task_skill(self, task_id: int) -> bool:
        """
        Remove task from storage.

        Args:
            task_id: ID of task to delete

        Returns:
            True if deleted, False if task_id not found
        """
        task = self.task_index.pop(task_id, None)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def mark_complete_skill(self, task_id: int) -> Task:
        """
        Mark task as completed and set completion timestamp.
        If task is recurring, creates next instance.

        Args:
            task_id: ID of task to complete

        Returns:
            Completed Task object

        Raises:
            KeyError: If task_id not found
        """
        task = self.task_index.get(task_id)
        if not task:
            raise KeyError(f"Task ID {task_id} not found")

        task.status = Status.COMPLETED
        task.completed_at = datetime.now(timezone.utc)

        # Handle recurring tasks
        if task.recurrence != Recurrence.NONE:
            self.process_recurring_tasks_skill(task)

        return task

    def mark_incomplete_skill(self, task_id: int) -> Task:
        """
        Mark task as pending and clear completion timestamp.

        Args:
            task_id: ID of task to mark incomplete

        Returns:
            Updated Task object

        Raises:
            KeyError: If task_id not found
        """
        task = self.task_index.get(task_id)
        if not task:
            raise KeyError(f"Task ID {task_id} not found")

        task.status = Status.PENDING
        task.completed_at = None

        return task

    def view_all_tasks_skill(self) -> list[Task]:
        """
        Retrieve all tasks in insertion order.

        Returns:
            List of all Task objects
        """
        return self.tasks.copy()

    # ========== Search/Filter/Sort Skills ==========

    def search_tasks_skill(self, keyword: str) -> list[Task]:
        """
        Find tasks matching keyword in title or description (case-insensitive).

        Args:
            keyword: Search term

        Returns:
            List of matching Task objects
        """
        keyword_lower = keyword.lower()
        return [
            task for task in self.tasks
            if keyword_lower in task.title.lower()
            or (task.description and keyword_lower in task.description.lower())
        ]

    def filter_tasks_skill(
        self,
        status: Optional[Status] = None,
        priority: Optional[Priority] = None,
        tag: Optional[str] = None
    ) -> list[Task]:
        """
        Filter tasks by status, priority, and/or tag (AND logic).

        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)
            tag: Filter by specific tag (optional)

        Returns:
            List of matching Task objects
        """
        return [
            task for task in self.tasks
            if (status is None or task.status == status)
            and (priority is None or task.priority == priority)
            and (tag is None or tag in task.tags)
        ]

    def sort_tasks_skill(
        self,
        tasks: list[Task],
        sort_by: str,
        reverse: bool = False
    ) -> list[Task]:
        """
        Sort task list by specified field.

        Args:
            tasks: List of tasks to sort
            sort_by: Field name ("due_date", "priority", "title", "created_at")
            reverse: If True, sort descending (default: ascending)

        Returns:
            New sorted list (does not modify input)

        Raises:
            ValueError: If sort_by field is invalid
        """
        key_funcs = {
            'due_date': lambda t: t.due_date or datetime.max,
            'priority': lambda t: {'High': 0, 'Medium': 1, 'Low': 2}[t.priority.value],
            'title': lambda t: t.title.lower(),
            'created_at': lambda t: t.created_at
        }

        if sort_by not in key_funcs:
            raise ValueError(f"Invalid sort_by field: {sort_by}")

        return sorted(tasks, key=key_funcs[sort_by], reverse=reverse)

    def get_overdue_tasks_skill(self) -> list[Task]:
        """
        Find all pending tasks past their due date.

        Returns:
            List of overdue Task objects
        """
        now = datetime.now(timezone.utc)
        return [
            task for task in self.tasks
            if task.status == Status.PENDING
            and task.due_date
            and task.due_date < now
        ]

    # ========== Recurring Task Skills ==========

    def process_recurring_tasks_skill(self, completed_task: Task) -> Optional[Task]:
        """
        Create next instance of recurring task.

        Args:
            completed_task: Task that was just completed

        Returns:
            New Task object if recurring, None otherwise
        """
        if completed_task.recurrence == Recurrence.NONE:
            return None

        # Calculate next due date
        if not completed_task.due_date:
            return None

        next_due_date = self._calculate_next_due_date(
            completed_task.due_date,
            completed_task.recurrence
        )

        # Create new instance
        new_task = self.add_task_skill(
            title=completed_task.title,
            description=completed_task.description,
            priority=completed_task.priority,
            tags=completed_task.tags.copy(),
            due_date=next_due_date,
            recurrence=completed_task.recurrence
        )

        return new_task

    def _calculate_next_due_date(
        self,
        current_due_date: datetime,
        recurrence: Recurrence
    ) -> datetime:
        """Calculate next due date based on recurrence pattern."""
        if recurrence == Recurrence.DAILY:
            return current_due_date + timedelta(days=1)
        elif recurrence == Recurrence.WEEKLY:
            return current_due_date + timedelta(weeks=1)
        elif recurrence == Recurrence.MONTHLY:
            return current_due_date + relativedelta(months=1)
        else:
            return current_due_date
```

### Step 4: Create the UI Sub-Agent

**File**: `todo_app/agents/ui_agent.py`

```python
"""
UIAgent Sub-Agent.

Responsible for all terminal output using the Rich library.
Handles tables, menus, prompts, and styled messages.
"""

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from typing import Optional

from todo_app.models.task import Task, Status, Priority


class UIAgent:
    """
    Sub-Agent for user interface rendering.

    This agent owns all terminal output using the Rich library.
    It provides skills for displaying tables, menus, prompts, and messages.

    Attributes:
        console: Rich Console instance for output
    """

    def __init__(self, console: Optional[Console] = None):
        """
        Initialize UIAgent with Rich console.

        Args:
            console: Optional Rich Console instance (creates new if None)
        """
        self.console = console or Console()

    def display_task_table_skill(
        self,
        tasks: list[Task],
        title: str = "Tasks"
    ) -> None:
        """
        Render tasks in formatted Rich table with colors and icons.

        Args:
            tasks: List of tasks to display
            title: Table title (default: "Tasks")

        Table includes: ID, Title, Priority, Status, Due Date, Tags
        With color coding and icons per specification.
        """
        if not tasks:
            self.console.print("[yellow]No tasks to display[/yellow]")
            return

        table = Table(title=title, title_style="bold cyan")

        # Add columns
        table.add_column("ID", style="cyan", width=6)
        table.add_column("Title", style="white", min_width=20)
        table.add_column("Priority", width=12)
        table.add_column("Status", width=12)
        table.add_column("Due Date", width=18)
        table.add_column("Tags", style="dim")

        # Add rows
        for task in tasks:
            # Priority icon and color
            priority_display = self._format_priority(task.priority)

            # Status icon and color
            status_display = self._format_status(task.status)

            # Due date formatting
            due_date_display = task.due_date.strftime("%Y-%m-%d %H:%M") if task.due_date else "-"

            # Tags
            tags_display = ", ".join(task.tags) if task.tags else "-"

            table.add_row(
                str(task.id),
                task.title,
                priority_display,
                status_display,
                due_date_display,
                tags_display
            )

        self.console.print(table)

    def _format_priority(self, priority: Priority) -> str:
        """Format priority with icon and color."""
        if priority == Priority.HIGH:
            return "[red]🔥 High[/red]"
        elif priority == Priority.MEDIUM:
            return "[yellow]⚡ Medium[/yellow]"
        else:
            return "[blue]🌱 Low[/blue]"

    def _format_status(self, status: Status) -> str:
        """Format status with icon and color."""
        if status == Status.COMPLETED:
            return "[green]✅ Completed[/green]"
        else:
            return "[white]🕒 Pending[/white]"

    def display_main_menu_skill(self) -> None:
        """Display main application menu with numbered options."""
        menu_text = """
[bold cyan]📋 TODO APPLICATION - Main Menu[/bold cyan]

[white]1.[/white] Add Task
[white]2.[/white] View All Tasks
[white]3.[/white] Update Task
[white]4.[/white] Delete Task
[white]5.[/white] Mark Task Complete
[white]6.[/white] Search Tasks
[white]7.[/white] Filter Tasks
[white]8.[/white] Sort Tasks
[white]9.[/white] View Stats
[white]0.[/white] Exit

"""
        self.console.print(menu_text)

    def prompt_text_input_skill(
        self,
        prompt_message: str,
        default: Optional[str] = None
    ) -> str:
        """
        Get text input from user.

        Args:
            prompt_message: Prompt to display
            default: Default value if user presses Enter

        Returns:
            User input string
        """
        if default:
            prompt_message += f" [dim](default: {default})[/dim]"

        return self.console.input(f"[cyan]{prompt_message}:[/cyan] ").strip() or default or ""

    def prompt_choice_skill(
        self,
        prompt_message: str,
        choices: list[str]
    ) -> str:
        """
        Display multiple-choice menu and get user selection.

        Args:
            prompt_message: Prompt to display
            choices: List of choice options

        Returns:
            Selected choice (user input)
        """
        self.console.print(f"\n[cyan]{prompt_message}:[/cyan]")
        for i, choice in enumerate(choices, 1):
            self.console.print(f"  {i}. {choice}")

        return self.console.input("[cyan]Select option:[/cyan] ").strip()

    def display_success_message_skill(self, message: str) -> None:
        """
        Show success message in green with checkmark icon.

        Args:
            message: Message to display
        """
        self.console.print(f"[green]✅ {message}[/green]")

    def display_error_message_skill(self, message: str) -> None:
        """
        Show error message in red with X icon.

        Args:
            message: Error message to display
        """
        self.console.print(f"[red]❌ {message}[/red]")
```

### Step 5: Create Main Application

**File**: `todo_app/main.py`

```python
"""
Main application entry point.

This module contains the menu loop and coordinates all Sub-Agents.
"""

from todo_app.agents.task_manager import TaskManager
from todo_app.agents.ui_agent import UIAgent
from todo_app.models.task import Priority, Recurrence


def main():
    """Main application loop."""
    # Instantiate Sub-Agents
    task_manager = TaskManager()
    ui_agent = UIAgent()

    ui_agent.console.print("[bold green]Welcome to Todo Application![/bold green]\n")

    while True:
        ui_agent.display_main_menu_skill()
        choice = ui_agent.prompt_text_input_skill("Enter your choice")

        if choice == "1":
            handle_add_task(task_manager, ui_agent)
        elif choice == "2":
            handle_view_tasks(task_manager, ui_agent)
        elif choice == "3":
            handle_update_task(task_manager, ui_agent)
        elif choice == "4":
            handle_delete_task(task_manager, ui_agent)
        elif choice == "5":
            handle_mark_complete(task_manager, ui_agent)
        elif choice == "0":
            ui_agent.console.print("[yellow]Goodbye![/yellow]")
            break
        else:
            ui_agent.display_error_message_skill("Invalid choice. Please try again.")


def handle_add_task(task_manager: TaskManager, ui_agent: UIAgent):
    """Handle adding a new task."""
    ui_agent.console.print("\n[bold]Add New Task[/bold]\n")

    title = ui_agent.prompt_text_input_skill("Task title")
    if not title:
        ui_agent.display_error_message_skill("Title cannot be empty")
        return

    description = ui_agent.prompt_text_input_skill("Description (optional)")

    priority_choice = ui_agent.prompt_choice_skill(
        "Select priority",
        ["High", "Medium", "Low"]
    )
    priority_map = {"1": Priority.HIGH, "2": Priority.MEDIUM, "3": Priority.LOW}
    priority = priority_map.get(priority_choice, Priority.MEDIUM)

    tags_input = ui_agent.prompt_text_input_skill("Tags (comma-separated, optional)")
    tags = [tag.strip() for tag in tags_input.split(",")] if tags_input else []

    try:
        task = task_manager.add_task_skill(
            title=title,
            description=description or None,
            priority=priority,
            tags=tags
        )
        ui_agent.display_success_message_skill(f"Task created with ID: {task.id}")
    except ValueError as e:
        ui_agent.display_error_message_skill(str(e))


def handle_view_tasks(task_manager: TaskManager, ui_agent: UIAgent):
    """Handle viewing all tasks."""
    ui_agent.console.print()
    tasks = task_manager.view_all_tasks_skill()
    ui_agent.display_task_table_skill(tasks, "All Tasks")


def handle_update_task(task_manager: TaskManager, ui_agent: UIAgent):
    """Handle updating a task."""
    ui_agent.console.print("\n[bold]Update Task[/bold]\n")

    task_id_str = ui_agent.prompt_text_input_skill("Enter task ID to update")
    try:
        task_id = int(task_id_str)
    except ValueError:
        ui_agent.display_error_message_skill("Invalid task ID")
        return

    task = task_manager.get_task_skill(task_id)
    if not task:
        ui_agent.display_error_message_skill(f"Task ID {task_id} not found")
        return

    new_title = ui_agent.prompt_text_input_skill("New title (press Enter to skip)", task.title)

    try:
        task_manager.update_task_skill(task_id, title=new_title)
        ui_agent.display_success_message_skill(f"Task {task_id} updated")
    except (KeyError, ValueError) as e:
        ui_agent.display_error_message_skill(str(e))


def handle_delete_task(task_manager: TaskManager, ui_agent: UIAgent):
    """Handle deleting a task."""
    ui_agent.console.print("\n[bold]Delete Task[/bold]\n")

    task_id_str = ui_agent.prompt_text_input_skill("Enter task ID to delete")
    try:
        task_id = int(task_id_str)
    except ValueError:
        ui_agent.display_error_message_skill("Invalid task ID")
        return

    if task_manager.delete_task_skill(task_id):
        ui_agent.display_success_message_skill(f"Task {task_id} deleted")
    else:
        ui_agent.display_error_message_skill(f"Task ID {task_id} not found")


def handle_mark_complete(task_manager: TaskManager, ui_agent: UIAgent):
    """Handle marking a task as complete."""
    ui_agent.console.print("\n[bold]Mark Task Complete[/bold]\n")

    task_id_str = ui_agent.prompt_text_input_skill("Enter task ID to complete")
    try:
        task_id = int(task_id_str)
    except ValueError:
        ui_agent.display_error_message_skill("Invalid task ID")
        return

    try:
        task = task_manager.mark_complete_skill(task_id)
        ui_agent.display_success_message_skill(f"Task {task_id} marked as complete")
    except KeyError as e:
        ui_agent.display_error_message_skill(str(e))


if __name__ == "__main__":
    main()
```

### Step 6: Create Requirements File

**File**: `requirements.txt`

```
rich>=13.0.0
python-dateutil>=2.8.0
```

---

## Running Your Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python todo_app/main.py
```

---

## Next Steps: Adding More Sub-Agents

Once you have the basic TaskManager and UIAgent working, add the other agents one by one:

1. **NLPAgent** (User Story 3) - Natural language parsing
2. **VoiceAgent** (User Story 4) - Speech-to-text
3. **LanguageAgent** (User Story 5) - Multi-language support
4. **GamificationAgent** (User Story 8) - XP, streaks, badges
5. **FocusAgent** (User Story 9) - Pomodoro timer
6. **AnalyticsAgent** (User Story 10) - Metrics and charts

Each agent follows the same pattern:
- One class per file
- Skills as methods (suffix: `_skill`)
- Stateless design
- PEP 257 docstrings

---

## Key Patterns to Follow

### 1. Skill Method Naming
```python
# Good
def add_task_skill(self, title: str) -> Task:
    pass

# Bad
def add_task(self, title: str) -> Task:
    pass
```

### 2. Clear Docstrings
```python
def add_task_skill(self, title: str) -> Task:
    """
    Create a new task.

    Args:
        title: Task title

    Returns:
        Created Task object

    Raises:
        ValueError: If title is empty
    """
    pass
```

### 3. Dependency Injection
```python
# In main.py
task_manager = TaskManager()
ui_agent = UIAgent()

# Pass agents to handlers
handle_add_task(task_manager, ui_agent)
```

### 4. Error Handling
```python
try:
    task = task_manager.add_task_skill(title="")
except ValueError as e:
    ui_agent.display_error_message_skill(str(e))
```

---

## Testing Your Sub-Agents

Create unit tests in `tests/unit/`:

```python
# tests/unit/test_task_manager.py
import pytest
from todo_app.agents.task_manager import TaskManager
from todo_app.models.task import Priority

def test_add_task_skill():
    """Test adding a task."""
    tm = TaskManager()
    task = tm.add_task_skill(title="Test task", priority=Priority.HIGH)

    assert task.id == 1
    assert task.title == "Test task"
    assert task.priority == Priority.HIGH

def test_get_task_skill():
    """Test retrieving a task."""
    tm = TaskManager()
    task = tm.add_task_skill(title="Test")

    retrieved = tm.get_task_skill(task.id)
    assert retrieved == task
```

---

## Architecture Benefits

**Separation of Concerns**:
- TaskManager: Data operations
- UIAgent: Display logic
- No mixing of concerns

**Testability**:
- Each skill is independently testable
- Mock agents easily

**Maintainability**:
- One file per agent
- Easy to find and modify

**Scalability**:
- Add new agents without touching existing code
- Add new skills to agents independently

---

## Common Mistakes to Avoid

❌ **Don't mix UI and business logic**
```python
# Bad - TaskManager displaying UI
class TaskManager:
    def add_task(self, title):
        task = Task(...)
        print("Task created!")  # DON'T DO THIS
```

✅ **Do separate concerns**
```python
# Good - TaskManager returns data, UIAgent displays
class TaskManager:
    def add_task_skill(self, title):
        task = Task(...)
        return task  # Return data only

# In main.py
task = task_manager.add_task_skill("Test")
ui_agent.display_success_message_skill(f"Task {task.id} created")
```

---

## Questions?

Refer to these documents:
- **Contract**: `specs/001-cli-todo-app/contracts/agent_interfaces.md`
- **Data Model**: `specs/001-cli-todo-app/data-model.md`
- **Architecture**: `specs/001-cli-todo-app/plan.md`
- **Tasks**: `specs/001-cli-todo-app/tasks.md`

Start with TaskManager and UIAgent, get them working, then add other agents incrementally!
