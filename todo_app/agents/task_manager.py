
"""
TaskManager Sub-Agent for task CRUD operations and organization.

This agent owns all task-related business logic including creation, retrieval,
updates, deletion, search, filtering, sorting, and recurring task management.
"""

from datetime import datetime, timedelta
from typing import Optional

from todo_app.models.task import Task, Status, Priority, Recurrence


class TaskManager:
    """
    Sub-Agent responsible for all task management operations.

    This is a stateless service class that manages an in-memory task list
    with O(1) ID lookups via a dictionary index.
    """

    def __init__(self):
        """Initialize TaskManager with empty task storage."""
        self.tasks: list[Task] = []
        self.task_index: dict[int, Task] = {}
        self.next_id: int = 1

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
            title: Brief task description (required)
            description: Extended task details (optional)
            priority: Task priority level (default: MEDIUM)
            tags: Categorization labels (optional)
            due_date: Task deadline (optional)
            recurrence: Repetition pattern (default: NONE)

        Returns:
            Newly created Task object

        Raises:
            ValueError: If title is empty or whitespace only
        """
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")

        task = Task(
            id=self.next_id,
            title=title.strip(),
            description=description,
            priority=priority,
            tags=tags or [],
            due_date=due_date,
            recurrence=recurrence
        )
        self.tasks.append(task)
        self.task_index[task.id] = task
        self.next_id += 1
        return task

    def get_task_by_id_skill(self, task_id: int) -> Optional[Task]:
        """
        Retrieve a task by its unique ID.

        Args:
            task_id: Unique task identifier

        Returns:
            Task object if found, None otherwise
        """
        return self.task_index.get(task_id)

    def get_all_tasks_skill(self) -> list[Task]:
        """
        Retrieve all tasks in creation order.

        Returns:
            List of all Task objects
        """
        return self.tasks.copy()

    def update_task_skill(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[list[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence: Optional[Recurrence] = None
    ) -> Optional[Task]:
        """
        Update an existing task's attributes.

        Args:
            task_id: Unique task identifier
            title: New task title (optional)
            description: New description (optional)
            priority: New priority level (optional)
            tags: New tag list (optional)
            due_date: New deadline (optional)
            recurrence: New recurrence pattern (optional)

        Returns:
            Updated Task object if found, None otherwise

        Raises:
            ValueError: If new title is empty or whitespace only
        """
        task = self.task_index.get(task_id)
        if task is None:
            return None

        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            task.title = title.strip()
        if description is not None:
            task.description = description
        if priority is not None:
            task.priority = priority
        if tags is not None:
            task.tags = tags
        if due_date is not None:
            task.due_date = due_date
        if recurrence is not None:
            task.recurrence = recurrence

        return task

    def delete_task_skill(self, task_id: int) -> bool:
        """
        Delete a task by its unique ID.

        Args:
            task_id: Unique task identifier

        Returns:
            True if task was deleted, False if task not found
        """
        task = self.task_index.get(task_id)
        if task is None:
            return False

        self.tasks.remove(task)
        del self.task_index[task_id]
        return True

    def complete_task_skill(self, task_id: int) -> Optional[Task]:
        """
        Mark a task as completed and handle recurring tasks.

        For recurring tasks, creates a new instance with updated due date.

        Args:
            task_id: Unique task identifier

        Returns:
            Completed Task object if found, None otherwise
        """
        task = self.task_index.get(task_id)
        if task is None:
            return None

        task.mark_completed()

        # Handle recurring tasks
        if task.recurrence != Recurrence.NONE and task.due_date:
            self._create_recurring_task_skill(task)

        return task

    def uncomplete_task_skill(self, task_id: int) -> Optional[Task]:
        """
        Mark a completed task as pending.

        Args:
            task_id: Unique task identifier

        Returns:
            Updated Task object if found, None otherwise
        """
        task = self.task_index.get(task_id)
        if task is None:
            return None

        task.mark_pending()
        return task

    def search_tasks_skill(self, query: str) -> list[Task]:
        """
        Search tasks by keyword in title, description, or tags.

        Case-insensitive search across title, description, and tags.

        Args:
            query: Search keyword

        Returns:
            List of matching Task objects
        """
        if not query:
            return []

        query_lower = query.lower()
        results = []

        for task in self.tasks:
            # Search in title
            if query_lower in task.title.lower():
                results.append(task)
                continue

            # Search in description
            if task.description and query_lower in task.description.lower():
                results.append(task)
                continue

            # Search in tags
            if any(query_lower in tag.lower() for tag in task.tags):
                results.append(task)

        return results

    def filter_by_status_skill(self, status: Status) -> list[Task]:
        """
        Filter tasks by completion status.

        Args:
            status: Status to filter by (PENDING or COMPLETED)

        Returns:
            List of tasks matching the status
        """
        return [task for task in self.tasks if task.status == status]

    def filter_by_priority_skill(self, priority: Priority) -> list[Task]:
        """
        Filter tasks by priority level.

        Args:
            priority: Priority level to filter by

        Returns:
            List of tasks matching the priority
        """
        return [task for task in self.tasks if task.priority == priority]

    def filter_by_tag_skill(self, tag: str) -> list[Task]:
        """
        Filter tasks by tag.

        Case-insensitive tag matching.

        Args:
            tag: Tag to filter by

        Returns:
            List of tasks containing the tag
        """
        tag_lower = tag.lower()
        return [task for task in self.tasks if any(t.lower() == tag_lower for t in task.tags)]

    def get_overdue_tasks_skill(self) -> list[Task]:
        """
        Retrieve all overdue pending tasks.

        Returns:
            List of pending tasks past their due date
        """
        return [task for task in self.tasks if task.is_overdue()]

    def sort_tasks_skill(
        self,
        tasks: list[Task],
        sort_by: str = "created",
        reverse: bool = False
    ) -> list[Task]:
        """
        Sort tasks by specified attribute.

        Args:
            tasks: List of tasks to sort
            sort_by: Sort attribute ('created', 'priority', 'due', 'title')
            reverse: Sort in descending order if True

        Returns:
            Sorted list of tasks

        Raises:
            ValueError: If sort_by is not a valid attribute
        """
        sort_keys = {
            "created": lambda t: t.created_at,
            "priority": lambda t: {"high": 0, "medium": 1, "low": 2}[t.priority.value],
            "due": lambda t: t.due_date or datetime.max,
            "title": lambda t: t.title.lower()
        }

        if sort_by not in sort_keys:
            raise ValueError(f"Invalid sort_by value: {sort_by}. Must be one of {list(sort_keys.keys())}")

        return sorted(tasks, key=sort_keys[sort_by], reverse=reverse)

    def _create_recurring_task_skill(self, original_task: Task) -> Task:
        """
        Create a new task instance based on a recurring task.

        Args:
            original_task: Completed recurring task

        Returns:
            New Task object with updated due date
        """
        if original_task.due_date is None:
            return original_task

        # Calculate new due date based on recurrence pattern
        new_due_date = original_task.due_date
        if original_task.recurrence == Recurrence.DAILY:
            new_due_date = original_task.due_date + timedelta(days=1)
        elif original_task.recurrence == Recurrence.WEEKLY:
            new_due_date = original_task.due_date + timedelta(weeks=1)
        elif original_task.recurrence == Recurrence.MONTHLY:
            # Approximate month as 30 days
            new_due_date = original_task.due_date + timedelta(days=30)

        # Create new task with same attributes but updated due date
        return self.add_task_skill(
            title=original_task.title,
            description=original_task.description,
            priority=original_task.priority,
            tags=original_task.tags.copy(),
            due_date=new_due_date,
            recurrence=original_task.recurrence
        )
