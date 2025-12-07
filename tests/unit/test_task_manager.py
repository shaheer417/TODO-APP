"""
Unit tests for TaskManager Sub-Agent.

Tests all task CRUD operations, search, filter, and sort functionality.
"""

import pytest
from datetime import datetime, timedelta

from todo_app.agents.task_manager import TaskManager
from todo_app.models.task import Task, Status, Priority, Recurrence


@pytest.fixture
def task_manager():
    """Create a fresh TaskManager instance for each test."""
    return TaskManager()


class TestTaskCreation:
    """Tests for task creation (add_task_skill)."""

    def test_add_task_with_minimal_fields(self, task_manager):
        """Test creating a task with only required fields."""
        task = task_manager.add_task_skill(title="Test task")

        assert task.id == 1
        assert task.title == "Test task"
        assert task.status == Status.PENDING
        assert task.priority == Priority.MEDIUM
        assert task.description is None
        assert task.tags == []
        assert task.due_date is None
        assert task.recurrence == Recurrence.NONE

    def test_add_task_with_all_fields(self, task_manager):
        """Test creating a task with all fields specified."""
        due_date = datetime(2025, 12, 31, 23, 59)
        task = task_manager.add_task_skill(
            title="Complete project",
            description="Finish all remaining tasks",
            priority=Priority.HIGH,
            tags=["work", "important"],
            due_date=due_date,
            recurrence=Recurrence.DAILY
        )

        assert task.id == 1
        assert task.title == "Complete project"
        assert task.description == "Finish all remaining tasks"
        assert task.priority == Priority.HIGH
        assert task.tags == ["work", "important"]
        assert task.due_date == due_date
        assert task.recurrence == Recurrence.DAILY

    def test_add_task_increments_id(self, task_manager):
        """Test that task IDs increment automatically."""
        task1 = task_manager.add_task_skill(title="Task 1")
        task2 = task_manager.add_task_skill(title="Task 2")
        task3 = task_manager.add_task_skill(title="Task 3")

        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

    def test_add_task_with_empty_title_raises_error(self, task_manager):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_manager.add_task_skill(title="")

    def test_add_task_with_whitespace_title_raises_error(self, task_manager):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_manager.add_task_skill(title="   ")

    def test_add_task_strips_whitespace_from_title(self, task_manager):
        """Test that leading/trailing whitespace is stripped from title."""
        task = task_manager.add_task_skill(title="  Test task  ")
        assert task.title == "Test task"


class TestTaskRetrieval:
    """Tests for task retrieval (get_task_by_id_skill, get_all_tasks_skill)."""

    def test_get_task_by_id_existing_task(self, task_manager):
        """Test retrieving an existing task by ID."""
        created_task = task_manager.add_task_skill(title="Test task")
        retrieved_task = task_manager.get_task_by_id_skill(created_task.id)

        assert retrieved_task is created_task
        assert retrieved_task.title == "Test task"

    def test_get_task_by_id_nonexistent_task(self, task_manager):
        """Test retrieving a nonexistent task returns None."""
        task = task_manager.get_task_by_id_skill(999)
        assert task is None

    def test_get_all_tasks_empty_list(self, task_manager):
        """Test getting all tasks when none exist."""
        tasks = task_manager.get_all_tasks_skill()
        assert tasks == []

    def test_get_all_tasks_returns_all_tasks(self, task_manager):
        """Test getting all tasks returns complete list."""
        task1 = task_manager.add_task_skill(title="Task 1")
        task2 = task_manager.add_task_skill(title="Task 2")
        task3 = task_manager.add_task_skill(title="Task 3")

        tasks = task_manager.get_all_tasks_skill()
        assert len(tasks) == 3
        assert task1 in tasks
        assert task2 in tasks
        assert task3 in tasks


class TestTaskUpdate:
    """Tests for task updates (update_task_skill)."""

    def test_update_task_title(self, task_manager):
        """Test updating task title."""
        task = task_manager.add_task_skill(title="Original title")
        updated = task_manager.update_task_skill(task.id, title="Updated title")

        assert updated.title == "Updated title"
        assert updated.id == task.id

    def test_update_task_priority(self, task_manager):
        """Test updating task priority."""
        task = task_manager.add_task_skill(title="Test task")
        updated = task_manager.update_task_skill(task.id, priority=Priority.HIGH)

        assert updated.priority == Priority.HIGH

    def test_update_task_multiple_fields(self, task_manager):
        """Test updating multiple fields at once."""
        task = task_manager.add_task_skill(title="Test task")
        updated = task_manager.update_task_skill(
            task.id,
            title="Updated task",
            description="New description",
            priority=Priority.LOW,
            tags=["tag1", "tag2"]
        )

        assert updated.title == "Updated task"
        assert updated.description == "New description"
        assert updated.priority == Priority.LOW
        assert updated.tags == ["tag1", "tag2"]

    def test_update_nonexistent_task(self, task_manager):
        """Test updating nonexistent task returns None."""
        updated = task_manager.update_task_skill(999, title="New title")
        assert updated is None

    def test_update_task_with_empty_title_raises_error(self, task_manager):
        """Test updating task with empty title raises ValueError."""
        task = task_manager.add_task_skill(title="Test task")
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            task_manager.update_task_skill(task.id, title="")


class TestTaskDeletion:
    """Tests for task deletion (delete_task_skill)."""

    def test_delete_existing_task(self, task_manager):
        """Test deleting an existing task."""
        task = task_manager.add_task_skill(title="Test task")
        result = task_manager.delete_task_skill(task.id)

        assert result is True
        assert task_manager.get_task_by_id_skill(task.id) is None
        assert len(task_manager.get_all_tasks_skill()) == 0

    def test_delete_nonexistent_task(self, task_manager):
        """Test deleting nonexistent task returns False."""
        result = task_manager.delete_task_skill(999)
        assert result is False


class TestTaskCompletion:
    """Tests for task completion (complete_task_skill, uncomplete_task_skill)."""

    def test_complete_task(self, task_manager):
        """Test marking task as completed."""
        task = task_manager.add_task_skill(title="Test task")
        completed = task_manager.complete_task_skill(task.id)

        assert completed.status == Status.COMPLETED
        assert completed.completed_at is not None

    def test_uncomplete_task(self, task_manager):
        """Test marking completed task as pending."""
        task = task_manager.add_task_skill(title="Test task")
        task_manager.complete_task_skill(task.id)
        uncompleted = task_manager.uncomplete_task_skill(task.id)

        assert uncompleted.status == Status.PENDING
        assert uncompleted.completed_at is None

    def test_complete_nonexistent_task(self, task_manager):
        """Test completing nonexistent task returns None."""
        completed = task_manager.complete_task_skill(999)
        assert completed is None


class TestTaskSearch:
    """Tests for task search (search_tasks_skill)."""

    def test_search_by_title(self, task_manager):
        """Test searching tasks by title keyword."""
        task_manager.add_task_skill(title="Buy groceries")
        task_manager.add_task_skill(title="Buy books")
        task_manager.add_task_skill(title="Read documentation")

        results = task_manager.search_tasks_skill("buy")
        assert len(results) == 2
        assert all("buy" in t.title.lower() for t in results)

    def test_search_case_insensitive(self, task_manager):
        """Test search is case-insensitive."""
        task_manager.add_task_skill(title="IMPORTANT TASK")
        results = task_manager.search_tasks_skill("important")
        assert len(results) == 1

    def test_search_empty_query(self, task_manager):
        """Test search with empty query returns empty list."""
        task_manager.add_task_skill(title="Test task")
        results = task_manager.search_tasks_skill("")
        assert results == []


class TestTaskFiltering:
    """Tests for task filtering (filter_by_status_skill, filter_by_priority_skill, filter_by_tag_skill)."""

    def test_filter_by_status_pending(self, task_manager):
        """Test filtering by pending status."""
        task1 = task_manager.add_task_skill(title="Task 1")
        task2 = task_manager.add_task_skill(title="Task 2")
        task_manager.complete_task_skill(task2.id)

        results = task_manager.filter_by_status_skill(Status.PENDING)
        assert len(results) == 1
        assert results[0].id == task1.id

    def test_filter_by_priority(self, task_manager):
        """Test filtering by priority level."""
        task_manager.add_task_skill(title="Task 1", priority=Priority.HIGH)
        task_manager.add_task_skill(title="Task 2", priority=Priority.LOW)
        task_manager.add_task_skill(title="Task 3", priority=Priority.HIGH)

        results = task_manager.filter_by_priority_skill(Priority.HIGH)
        assert len(results) == 2

    def test_filter_by_tag(self, task_manager):
        """Test filtering by tag."""
        task_manager.add_task_skill(title="Task 1", tags=["work", "urgent"])
        task_manager.add_task_skill(title="Task 2", tags=["personal"])
        task_manager.add_task_skill(title="Task 3", tags=["work"])

        results = task_manager.filter_by_tag_skill("work")
        assert len(results) == 2


class TestOverdueTasks:
    """Tests for overdue task detection (get_overdue_tasks_skill)."""

    def test_get_overdue_tasks(self, task_manager):
        """Test retrieving overdue pending tasks."""
        past_date = datetime.now() - timedelta(days=1)
        future_date = datetime.now() + timedelta(days=1)

        overdue_task = task_manager.add_task_skill(title="Overdue task", due_date=past_date)
        task_manager.add_task_skill(title="Future task", due_date=future_date)

        results = task_manager.get_overdue_tasks_skill()
        assert len(results) == 1
        assert results[0].id == overdue_task.id


class TestTaskSorting:
    """Tests for task sorting (sort_tasks_skill)."""

    def test_sort_by_created_ascending(self, task_manager):
        """Test sorting by creation date (oldest first)."""
        task1 = task_manager.add_task_skill(title="Task 1")
        task2 = task_manager.add_task_skill(title="Task 2")
        task3 = task_manager.add_task_skill(title="Task 3")

        tasks = task_manager.get_all_tasks_skill()
        sorted_tasks = task_manager.sort_tasks_skill(tasks, sort_by="created", reverse=False)

        assert sorted_tasks[0].id == task1.id
        assert sorted_tasks[1].id == task2.id
        assert sorted_tasks[2].id == task3.id

    def test_sort_by_priority(self, task_manager):
        """Test sorting by priority (high first)."""
        task_manager.add_task_skill(title="Low", priority=Priority.LOW)
        task_manager.add_task_skill(title="High", priority=Priority.HIGH)
        task_manager.add_task_skill(title="Medium", priority=Priority.MEDIUM)

        tasks = task_manager.get_all_tasks_skill()
        sorted_tasks = task_manager.sort_tasks_skill(tasks, sort_by="priority", reverse=False)

        assert sorted_tasks[0].priority == Priority.HIGH
        assert sorted_tasks[1].priority == Priority.MEDIUM
        assert sorted_tasks[2].priority == Priority.LOW

    def test_sort_invalid_field_raises_error(self, task_manager):
        """Test sorting by invalid field raises ValueError."""
        tasks = task_manager.get_all_tasks_skill()
        with pytest.raises(ValueError, match="Invalid sort_by value"):
            task_manager.sort_tasks_skill(tasks, sort_by="invalid_field")
