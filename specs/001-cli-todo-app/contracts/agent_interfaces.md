# Agent Interfaces: In-Memory Python CLI Todo Application

**Date**: 2025-12-05
**Feature**: CLI Todo App (001-cli-todo-app)
**Purpose**: Define public skill methods (API contracts) for all Sub-Agents

---

## Overview

Each Sub-Agent exposes **Skills** - focused, testable methods that implement a single responsibility. This document serves as the contract between agents and defines the expected behavior of each skill.

**Conventions**:
- All skill methods end with `_skill` suffix
- Return types are explicit (no implicit None returns)
- Errors raise exceptions rather than returning error codes
- All agents are stateless service classes (dependencies injected)

---

## 1. TaskManager Sub-Agent

**File**: `todo_app/agents/task_manager.py`

**Responsibility**: Core task CRUD operations, search, filter, sort, and recurring task management.

### Methods

#### `add_task_skill(title: str, description: str = None, priority: Priority = Priority.MEDIUM, tags: list[str] = None, due_date: datetime = None, recurrence: Recurrence = Recurrence.NONE) -> Task`

Create new task with auto-generated ID and timestamps.

**Parameters**:
- `title`: Task title (required, max 200 chars)
- `description`: Optional description (max 1000 chars)
- `priority`: Task priority (default: Medium)
- `tags`: List of category tags (default: empty list)
- `due_date`: Optional deadline (timezone-aware datetime)
- `recurrence`: Repeat pattern (default: None)

**Returns**: Created Task object with assigned ID

**Raises**:
- `ValueError`: If title is empty or exceeds 200 characters
- `ValueError`: If description exceeds 1000 characters

**Example**:
```python
task = task_manager.add_task_skill(
    title="Complete project report",
    priority=Priority.HIGH,
    tags=["work", "urgent"],
    due_date=datetime(2025, 12, 10, 17, 0, tzinfo=timezone.utc)
)
```

---

#### `get_task_skill(task_id: int) -> Optional[Task]`

Retrieve task by ID (O(1) lookup).

**Parameters**:
- `task_id`: Unique task identifier

**Returns**: Task object if found, None otherwise

**Raises**: None

---

#### `update_task_skill(task_id: int, **kwargs) -> Task`

Update one or more fields of existing task.

**Parameters**:
- `task_id`: ID of task to update
- `**kwargs`: Field names and new values (title, description, priority, tags, due_date, recurrence)

**Returns**: Updated Task object

**Raises**:
- `KeyError`: If task_id not found
- `ValueError`: If field validation fails

**Example**:
```python
task = task_manager.update_task_skill(5, priority=Priority.LOW, tags=["deferred"])
```

---

#### `delete_task_skill(task_id: int) -> bool`

Remove task from storage.

**Parameters**:
- `task_id`: ID of task to delete

**Returns**: True if deleted, False if task_id not found

**Raises**: None

---

#### `mark_complete_skill(task_id: int) -> Task`

Toggle task status to Completed and set completed_at timestamp. If task is recurring, creates next instance.

**Parameters**:
- `task_id`: ID of task to complete

**Returns**: Completed Task object

**Raises**:
- `KeyError`: If task_id not found

**Side Effects**:
- Sets status = Status.COMPLETED
- Sets completed_at = current datetime
- If recurring: creates new Task with next due_date

---

#### `mark_incomplete_skill(task_id: int) -> Task`

Toggle task status back to Pending and clear completed_at.

**Parameters**:
- `task_id`: ID of task to mark incomplete

**Returns**: Updated Task object

**Raises**:
- `KeyError`: If task_id not found

**Side Effects**:
- Sets status = Status.PENDING
- Clears completed_at (sets to None)

---

#### `view_all_tasks_skill() -> list[Task]`

Retrieve all tasks in insertion order.

**Parameters**: None

**Returns**: List of all Task objects

**Raises**: None

---

#### `search_tasks_skill(keyword: str) -> list[Task]`

Find tasks matching keyword in title or description (case-insensitive).

**Parameters**:
- `keyword`: Search term

**Returns**: List of matching Task objects

**Raises**: None

**Performance**: O(n) linear search

---

#### `filter_tasks_skill(status: Status = None, priority: Priority = None, tag: str = None) -> list[Task]`

Filter tasks by one or more criteria (AND logic).

**Parameters**:
- `status`: Filter by status (optional)
- `priority`: Filter by priority (optional)
- `tag`: Filter by specific tag (optional)

**Returns**: List of matching Task objects

**Raises**: None

**Example**:
```python
# Get all high-priority pending tasks tagged "work"
tasks = task_manager.filter_tasks_skill(
    status=Status.PENDING,
    priority=Priority.HIGH,
    tag="work"
)
```

---

#### `sort_tasks_skill(tasks: list[Task], sort_by: str, reverse: bool = False) -> list[Task]`

Sort task list by specified field.

**Parameters**:
- `tasks`: List of tasks to sort
- `sort_by`: Field name ("due_date", "priority", "title", "created_at")
- `reverse`: If True, sort descending (default: ascending)

**Returns**: New sorted list (does not modify input)

**Raises**:
- `ValueError`: If sort_by field is invalid

**Example**:
```python
# Sort by due date, soonest first
sorted_tasks = task_manager.sort_tasks_skill(tasks, "due_date", reverse=False)
```

---

#### `get_overdue_tasks_skill() -> list[Task]`

Find all pending tasks past their due date.

**Parameters**: None

**Returns**: List of overdue Task objects

**Raises**: None

---

#### `process_recurring_tasks_skill(completed_task: Task) -> Optional[Task]`

Create next instance of recurring task. Called internally by mark_complete_skill.

**Parameters**:
- `completed_task`: Task that was just completed

**Returns**: New Task object if recurring, None otherwise

**Raises**: None

**Logic**:
- If recurrence == DAILY: due_date + 1 day
- If recurrence == WEEKLY: due_date + 7 days
- If recurrence == MONTHLY: due_date + 1 month (same day, or last day if month shorter)

---

## 2. UIAgent Sub-Agent

**File**: `todo_app/agents/ui_agent.py`

**Responsibility**: All terminal output using Rich library (tables, menus, prompts, styling).

### Methods

#### `display_task_table_skill(tasks: list[Task], title: str = "Tasks") -> None`

Render tasks in formatted Rich table with colors and icons.

**Parameters**:
- `tasks`: List of tasks to display
- `title`: Table title (default: "Tasks")

**Returns**: None (prints to console)

**Raises**: None

**Table Columns**:
- ID
- Icon + Title
- Priority (with icon and color)
- Status (with icon)
- Due Date
- Tags

**Color Scheme**:
- Completed: green
- High priority: red
- Medium priority: yellow
- Low priority: blue
- Overdue: bright red

---

#### `display_main_menu_skill() -> None`

Show main application menu with numbered options.

**Parameters**: None

**Returns**: None (prints to console)

**Raises**: None

---

#### `display_startup_screen_skill(pending_count: int, streak: int, quote: tuple[str, str]) -> None`

Render welcome screen with ASCII art, stats, and quote.

**Parameters**:
- `pending_count`: Number of pending tasks
- `streak`: Current daily streak
- `quote`: Tuple of (quote_text, author)

**Returns**: None (prints to console)

**Raises**: None

---

#### `prompt_text_input_skill(prompt_message: str, default: str = None) -> str`

Get text input from user with optional default value.

**Parameters**:
- `prompt_message`: Prompt to display
- `default`: Default value if user presses Enter (optional)

**Returns**: User input string

**Raises**: None

---

#### `prompt_choice_skill(prompt_message: str, choices: list[str]) -> str`

Display multiple-choice menu and get user selection.

**Parameters**:
- `prompt_message`: Prompt to display
- `choices`: List of choice options

**Returns**: Selected choice (user input)

**Raises**: None

---

#### `display_success_message_skill(message: str) -> None`

Show success message in green with checkmark icon.

**Parameters**:
- `message`: Message to display

**Returns**: None (prints to console)

**Raises**: None

---

#### `display_error_message_skill(message: str) -> None`

Show error message in red with X icon.

**Parameters**:
- `message`: Error message to display

**Returns**: None (prints to console)

**Raises**: None

---

#### `display_analytics_dashboard_skill(metrics: dict) -> None`

Render productivity analytics in formatted panels.

**Parameters**:
- `metrics`: Dict containing analytics data

**Returns**: None (prints to console)

**Raises**: None

---

## 3. NLPAgent Sub-Agent

**File**: `todo_app/agents/nlp_agent.py`

**Responsibility**: Natural language parsing for task input.

### Methods

#### `parse_natural_language_skill(text: str) -> tuple[str, Optional[datetime], Priority]`

Extract task title, due date, and priority from natural language input.

**Parameters**:
- `text`: User's natural language input

**Returns**: Tuple of (title, due_date, priority)

**Raises**: None (gracefully handles unparseable input)

**Example**:
```python
title, due_date, priority = nlp_agent.parse_natural_language_skill(
    "Urgent: submit report by tomorrow 5pm"
)
# Returns: ("submit report", datetime(...), Priority.HIGH)
```

---

## 4. VoiceAgent Sub-Agent

**File**: `todo_app/agents/voice_agent.py`

**Responsibility**: Speech-to-text conversion for hands-free task entry.

### Methods

#### `transcribe_voice_skill(timeout: int = 5, phrase_limit: int = 10) -> Optional[str]`

Record audio from microphone and convert to text.

**Parameters**:
- `timeout`: Seconds to wait for speech (default: 5)
- `phrase_limit`: Maximum phrase duration in seconds (default: 10)

**Returns**: Transcribed text or None if error/timeout

**Raises**: None (errors handled internally with user messages)

**Backends**:
- Primary: Google Speech Recognition
- Fallback: CMU Sphinx (offline)

---

## 5. LanguageAgent Sub-Agent

**File**: `todo_app/agents/language_agent.py`

**Responsibility**: Multi-language support via JSON translation files.

### Methods

#### `load_language_skill(lang_code: str) -> bool`

Load translation file for specified language.

**Parameters**:
- `lang_code`: Language code ("en", "ur", "es")

**Returns**: True if loaded successfully, False otherwise

**Raises**: None

**Side Effects**: Updates current_lang and translations dict

---

#### `translate_skill(key: str) -> str`

Get translated string for key, falling back to English if missing.

**Parameters**:
- `key`: Translation key (e.g., "menu.add_task")

**Returns**: Translated string or key itself if not found

**Raises**: None

---

#### `get_current_language_skill() -> str`

Get currently active language code.

**Parameters**: None

**Returns**: Language code (e.g., "en")

**Raises**: None

---

## 6. GamificationAgent Sub-Agent

**File**: `todo_app/agents/gamification_agent.py`

**Responsibility**: XP, streaks, badges, and motivation mechanics.

### Methods

#### `award_xp_skill(task: Task) -> int`

Calculate and award XP for task completion.

**Parameters**:
- `task`: Completed task

**Returns**: XP amount awarded

**Raises**: None

**Logic**:
- Base XP: 10
- Bonus if completed before due_date: +25
- Bonus if completed before 8 AM: +15

**Side Effects**: Updates UserProfile.total_xp

---

#### `update_streak_skill(completion_date: date) -> int`

Update daily streak based on completion date.

**Parameters**:
- `completion_date`: Date task was completed

**Returns**: New streak value

**Raises**: None

**Logic**:
- If same day as last: no change
- If next day: increment
- If gap > 1 day: reset to 1

**Side Effects**: Updates UserProfile.daily_streak and last_completion_date

---

#### `check_badge_eligibility_skill(task: Task) -> list[str]`

Check if task completion earns any new badges.

**Parameters**:
- `task`: Completed task

**Returns**: List of badge names earned (empty if none)

**Raises**: None

**Checks**:
- Early Bird: Completed before 8 AM
- 7-Day Streak: daily_streak == 7
- Task Master: 50 total completions

**Side Effects**: Adds badges to UserProfile.earned_badges

---

## 7. FocusAgent Sub-Agent

**File**: `todo_app/agents/focus_agent.py`

**Responsibility**: Pomodoro timer for focus sessions.

### Methods

#### `start_pomodoro_skill(task_title: str, duration_minutes: int) -> bool`

Start focus timer with live countdown display.

**Parameters**:
- `task_title`: Name of task being focused on
- `duration_minutes`: Timer duration (25 or 50)

**Returns**: True if completed, False if cancelled

**Raises**: None

**User Interaction**:
- Displays live countdown using rich.live
- User can press Ctrl+C to cancel
- Shows completion message when finished

---

## 8. AnalyticsAgent Sub-Agent

**File**: `todo_app/agents/analytics_agent.py`

**Responsibility**: Productivity metrics calculation and visualization.

### Methods

#### `calculate_metrics_skill() -> dict`

Calculate all productivity metrics from completion history.

**Parameters**: None

**Returns**: Dict containing:
- `tasks_completed_today`: int
- `tasks_completed_this_week`: int
- `total_overdue`: int
- `most_productive_day`: str (e.g., "Monday")
- `most_productive_hour`: int (0-23)
- `average_completion_time`: timedelta

**Raises**: None

---

#### `generate_weekly_chart_skill() -> Table`

Generate text-based bar chart of tasks completed per day (last 7 days).

**Parameters**: None

**Returns**: Rich Table object with chart

**Raises**: None

---

## Agent Dependencies

```
main.py
  ├── TaskManager (core data operations)
  ├── UIAgent (all console output)
  ├── NLPAgent (used by TaskManager for natural language task creation)
  ├── VoiceAgent (used by UIAgent for voice input mode)
  ├── LanguageAgent (used by UIAgent for translated strings)
  ├── GamificationAgent (called after TaskManager.mark_complete)
  ├── FocusAgent (standalone, triggered from main menu)
  └── AnalyticsAgent (standalone, triggered from main menu)
```

**Dependency Injection**: All agents instantiated in main.py and passed to handlers/workflows as needed.

---

**Contract Status**: ✅ Complete
**All Agent Interfaces Defined**: Yes
**Ready for Implementation**: Yes
