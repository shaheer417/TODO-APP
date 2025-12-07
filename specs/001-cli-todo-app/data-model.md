# Data Model: In-Memory Python CLI Todo Application

**Date**: 2025-12-05
**Feature**: CLI Todo App (001-cli-todo-app)
**Purpose**: Define all data entities, fields, validations, and relationships

---

## Entity Diagram

```
┌─────────────────────┐
│       Task          │
│─────────────────────│
│ + id: int           │
│ + title: str        │
│ + description: str? │
│ + status: Status    │
│ + priority: Priority│
│ + tags: list[str]   │
│ + due_date: datetime?│
│ + created_at: datetime│
│ + completed_at: datetime?│
│ + recurrence: Recurrence│
└─────────────────────┘
         ▲
         │ references (via ID)
         │
┌─────────────────────┐         ┌─────────────────────┐
│   UserProfile       │         │   Configuration     │
│─────────────────────│         │─────────────────────│
│ + total_xp: int     │         │ + language: str     │
│ + daily_streak: int │         │ + color_theme: str  │
│ + last_completion_date: date?│ │ + default_priority: Priority│
│ + earned_badges: list[str]│   └─────────────────────┘
│ + completion_history: list[CompletionRecord]│
└─────────────────────┘

CompletionRecord (embedded):
  - task_id: int
  - completed_at: datetime
  - xp_earned: int
```

---

## 1. Task Entity

### Purpose
Represents a single todo item with all associated metadata.

### Fields

| Field Name | Type | Required | Default | Description |
|------------|------|----------|---------|-------------|
| `id` | int | Yes | Auto-increment | Unique identifier, starts at 1 |
| `title` | str | Yes | - | Task title, max 200 characters |
| `description` | str | No | None | Detailed description, max 1000 characters |
| `status` | Status (enum) | Yes | "Pending" | Current task state |
| `priority` | Priority (enum) | Yes | "Medium" | Importance level |
| `tags` | list[str] | No | [] | Category tags for organization |
| `due_date` | datetime | No | None | Deadline with time (timezone-aware) |
| `created_at` | datetime | Yes | Auto-generated | Timestamp when task was created |
| `completed_at` | datetime | No | None | Timestamp when task was completed |
| `recurrence` | Recurrence (enum) | Yes | "None" | Repeat pattern for recurring tasks |

### Enumerations

**Status**:
```python
class Status(Enum):
    PENDING = "Pending"
    COMPLETED = "Completed"
```

**Priority**:
```python
class Priority(Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"
```

**Recurrence**:
```python
class Recurrence(Enum):
    NONE = "None"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
```

### Validations

1. **Title**:
   - Cannot be empty or whitespace-only
   - Maximum length: 200 characters
   - Error: "Task title cannot be empty"

2. **Description**:
   - Optional field
   - Maximum length: 1000 characters
   - Error: "Description too long (max 1000 characters)"

3. **Due Date**:
   - Must be timezone-aware datetime
   - Warning (not error) if in the past
   - Stored as UTC internally, displayed in local timezone

4. **Completed At**:
   - Can only be set when status is "Completed"
   - Automatically cleared if status changes back to "Pending"
   - Must be >= created_at

5. **Tags**:
   - Each tag max 50 characters
   - Case-insensitive (stored lowercase)
   - No duplicate tags allowed
   - Special characters allowed except commas

6. **Recurrence**:
   - If recurrence != "None", due_date is recommended (warning if missing)
   - Recurring task completion creates new instance with updated due_date

### State Transitions

```
[Initial State]
      │
      ▼
  ┌─────────┐   mark_complete    ┌───────────┐
  │ Pending ├──────────────────>  │ Completed │
  └─────────┘                     └───────────┘
      ▲                                 │
      │                                 │
      └─────────── mark_incomplete ─────┘

Special case for Recurring Tasks:
  │ Completed │ ──> [Create new Pending instance with next due_date]
```

### Business Rules

1. **Overdue Detection**:
   - Task is overdue if: `status == "Pending" AND due_date < current_time`
   - Display with bright red color and warning icon

2. **Recurring Task Generation**:
   - When recurring task is completed:
     - Calculate next due_date based on recurrence pattern
     - Create new Task with same title, description, priority, tags, recurrence
     - New task gets new ID and created_at timestamp
     - Original task remains in history as completed

3. **XP Calculation** (for Gamification):
   - Base XP: 10 points for any completion
   - Bonus XP: +25 points if completed before due_date
   - Early Bird bonus: +15 points if completed before 8 AM

### Example Instance

```python
Task(
    id=42,
    title="Complete project report",
    description="Quarterly report for Q4 2025",
    status=Status.PENDING,
    priority=Priority.HIGH,
    tags=["work", "urgent", "quarterly"],
    due_date=datetime(2025, 12, 10, 17, 0, tzinfo=timezone.utc),
    created_at=datetime(2025, 12, 5, 9, 30, tzinfo=timezone.utc),
    completed_at=None,
    recurrence=Recurrence.NONE
)
```

---

## 2. UserProfile Entity

### Purpose
Stores gamification metrics and productivity analytics data for the current session.

### Fields

| Field Name | Type | Required | Default | Description |
|------------|------|----------|---------|-------------|
| `total_xp` | int | Yes | 0 | Total experience points earned |
| `daily_streak` | int | Yes | 0 | Consecutive days with at least 1 completed task |
| `last_completion_date` | date | No | None | Date of most recent task completion |
| `earned_badges` | list[str] | Yes | [] | List of badge names awarded |
| `completion_history` | list[CompletionRecord] | Yes | [] | History of all task completions |

### Nested Type: CompletionRecord

```python
@dataclass
class CompletionRecord:
    task_id: int          # ID of completed task
    completed_at: datetime # Timestamp of completion
    xp_earned: int        # XP awarded for this completion
```

### Validations

1. **total_xp**:
   - Cannot be negative
   - Error: "XP cannot be negative"

2. **daily_streak**:
   - Cannot be negative
   - Resets to 0 if `current_date - last_completion_date > 1 day`
   - Increments by 1 when task completed on new day

3. **earned_badges**:
   - Each badge name is unique (no duplicates)
   - Stored as list of strings matching predefined badge names

4. **completion_history**:
   - Append-only (no deletions or modifications)
   - Used for analytics calculations

### Badge Definitions

| Badge Name | Criteria | Icon |
|------------|----------|------|
| "Early Bird" | Complete task before 8 AM | 🌅 |
| "7-Day Streak" | Maintain 7 consecutive days of completions | 🔥 |
| "Task Master" | Complete 50 total tasks | 🏆 |
| "Speed Demon" | Complete task within 1 hour of creation | ⚡ |
| "Deadline Crusher" | Complete 10 tasks before their due date | 🎯 |

### Business Rules

1. **Streak Calculation**:
   ```python
   def update_streak(profile: UserProfile, current_date: date):
       if profile.last_completion_date is None:
           profile.daily_streak = 1
       elif (current_date - profile.last_completion_date).days == 1:
           profile.daily_streak += 1  # Continue streak
       elif (current_date - profile.last_completion_date).days > 1:
           profile.daily_streak = 1   # Reset streak
       # Same day: no change
   ```

2. **Badge Awarding**:
   - Check criteria after each task completion
   - Only award badge once (check if already in earned_badges)
   - Display notification when badge is earned

3. **Analytics Queries**:
   - Most productive day: Group completion_history by day_of_week, find max
   - Most productive time: Group completion_history by hour, find max
   - Average completion time: Average of (completed_at - created_at) for all tasks

### Example Instance

```python
UserProfile(
    total_xp=250,
    daily_streak=5,
    last_completion_date=date(2025, 12, 5),
    earned_badges=["Early Bird", "7-Day Streak"],
    completion_history=[
        CompletionRecord(
            task_id=1,
            completed_at=datetime(2025, 12, 1, 7, 45),
            xp_earned=25  # 10 base + 15 Early Bird
        ),
        CompletionRecord(
            task_id=2,
            completed_at=datetime(2025, 12, 2, 14, 30),
            xp_earned=10  # Base only
        ),
        # ... more records
    ]
)
```

---

## 3. Configuration Entity

### Purpose
Stores user preferences and application settings for the current session.

### Fields

| Field Name | Type | Required | Default | Description |
|------------|------|----------|---------|-------------|
| `language` | str | Yes | "en" | Interface language code |
| `color_theme` | str | Yes | "default" | Color scheme name |
| `default_priority` | Priority (enum) | Yes | Priority.MEDIUM | Default priority for new tasks |

### Validations

1. **language**:
   - Must be one of: ["en", "ur", "es"]
   - Falls back to "en" if invalid or translation file missing
   - Error: "Unsupported language. Using English."

2. **color_theme**:
   - Currently only "default" supported (reserved for future themes)
   - No validation error (ignored if invalid)

3. **default_priority**:
   - Must be valid Priority enum value
   - Used when user doesn't specify priority

### Example Instance

```python
Configuration(
    language="en",
    color_theme="default",
    default_priority=Priority.MEDIUM
)
```

---

## 4. Relationships

### Task ← UserProfile
- **Type**: Weak reference (one-way)
- **Cardinality**: Many Tasks to One UserProfile
- **Implementation**: UserProfile.completion_history contains task_ids
- **Integrity**: Task deletion does not cascade to UserProfile (IDs remain in history)

### Configuration ← (All Entities)
- **Type**: Application-wide singleton
- **Cardinality**: One Configuration for entire application
- **Implementation**: Injected into agents that need localization or defaults

---

## 5. Data Storage Strategy

### In-Memory Structure

```python
# TaskManager maintains all tasks
class TaskManager:
    tasks: List[Task] = []              # Main storage (preserves order)
    task_index: Dict[int, Task] = {}    # Fast O(1) lookup by ID
    next_id: int = 1                     # Auto-increment counter

# UserProfile is a single instance
user_profile: UserProfile = UserProfile()

# Configuration is a single instance
config: Configuration = Configuration()
```

### Indexing Strategy

**Primary Index** (task_index):
- Key: Task.id (int)
- Value: Task object reference
- Purpose: O(1) lookups for get/update/delete operations

**No Secondary Indexes**:
- Search/filter use list comprehensions (O(n) acceptable for 10,000 tasks)
- Sorting uses Python's Timsort (O(n log n))

### Memory Considerations

**Estimated Memory Usage** (10,000 tasks):
- Task object: ~200 bytes each
- List storage: ~2 MB
- Dict index: ~500 KB
- UserProfile: ~100 KB (depends on completion_history size)
- **Total**: ~2.6 MB (negligible)

---

## 6. Data Lifecycle

### Task Lifecycle

```
[Create] ──> [Update*] ──> [Complete] ──> [Recurring: Create Next Instance]
                                │
                                └──> [Delete] ──> [Removed from memory]
```

### Session Data

**On Application Start**:
- All data structures initialized empty
- Configuration loaded from config.json (if exists)
- Sample tasks optionally loaded for demo

**During Session**:
- All changes in-memory only
- No automatic persistence
- Data consistent within session

**On Application Exit**:
- All data discarded (constitutional requirement: no persistence)
- Configuration optionally saved to config.json (user preferences only)

---

## 7. Data Validation Summary

| Entity | Validation Points | Error Handling |
|--------|-------------------|----------------|
| **Task** | Title (required, max 200), Description (max 1000), Due date (future warning), Completed_at (only when completed) | User-friendly error messages, prevent save on validation failure |
| **UserProfile** | XP non-negative, Streak auto-reset logic, Unique badges | Internal consistency checks, no user errors |
| **Configuration** | Language in supported list, Fallback to English | Warning message, graceful degradation |

---

**Data Model Status**: ✅ Complete
**All Entities Defined**: Yes
**Ready for Implementation**: Yes
