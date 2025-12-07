# UI Agent Skill

Display rich terminal UI elements for the Todo application using the Rich library.

## Purpose
This skill provides access to the UIAgent sub-agent which handles all terminal-based user interface rendering including tables, menus, prompts, panels, and formatted output.

## Usage

When you need to display or interact with the UI, invoke the UIAgent's methods.

### Available Skills

#### Display Task Table
```python
from todo_app.agents.ui_agent import UIAgent

ui = UIAgent()
ui.display_task_table_skill(tasks, title="Tasks")
```

#### Display Task Details
```python
ui.display_task_details_skill(task)
```

#### Display Main Menu
```python
ui.display_main_menu_skill()
```

#### Prompt for Input
```python
user_input = ui.prompt_input_skill("Enter task title", default="")
```

#### Prompt for Confirmation
```python
confirmed = ui.prompt_confirm_skill("Are you sure?", default=False)
```

#### Display Messages
```python
ui.display_message_skill("Operation completed", style="green")
ui.display_error_skill("Invalid input")
ui.display_success_skill("Task created successfully")
```

#### Display Header
```python
ui.display_header_skill("Todo Application")
```

#### Display Statistics
```python
stats = {
    'total': 10,
    'pending': 5,
    'completed': 5,
    'overdue': 2
}
ui.display_statistics_skill(stats)
```

#### Clear Screen
```python
ui.clear_screen_skill()
```

## When to Use

- When displaying tasks in a formatted table
- When showing detailed information about a single task
- When rendering menus and navigation
- When prompting users for input or confirmation
- When displaying success, error, or informational messages
- When showing statistics or dashboard views
- When clearing the terminal screen

## Dependencies

- Rich library (for beautiful CLI formatting)
- todo_app.models.task module (for Task, Status, Priority models)
