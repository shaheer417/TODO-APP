# Focus Agent Skill

Provide Pomodoro timer functionality for focused work sessions.

## Purpose
This skill provides access to the FocusAgent sub-agent which manages focus mode with Pomodoro-style timers using Rich's Live display for smooth, flicker-free countdown updates.

## Usage

When you need to start a focus session or manage Pomodoro timers, invoke the FocusAgent's methods.

### Available Skills

#### Start Focus Session
```python
from todo_app.agents.focus_agent import FocusAgent

focus = FocusAgent()
completed = focus.start_focus_session_skill(
    task_title="Write documentation",
    duration_minutes=25,
    on_complete=None  # Optional callback function
)
# Returns: True if session completed, False if interrupted
```

#### Start Break Timer
```python
completed = focus.start_break_skill(duration_minutes=5)
# Returns: True if break completed, False if interrupted
```

#### Stop Running Timer
```python
focus.stop_timer_skill()
# Stops the currently running timer
```

#### Check if Timer Running
```python
is_running = focus.is_timer_running_skill()
# Returns: True if timer active, False otherwise
```

#### Get Preset Durations
```python
presets = focus.get_preset_durations_skill()
# Returns: {
#     "pomodoro_25": 25,
#     "pomodoro_50": 50,
#     "break_5": 5,
#     "break_15": 15
# }
```

## Timer Presets

### Work Sessions
- **25 minutes**: Standard Pomodoro session
- **50 minutes**: Extended focus session

### Break Sessions
- **5 minutes**: Short break
- **15 minutes**: Long break

## Timer Display Features

The focus mode displays:
- 🎯 Focus mode indicator
- Task title
- Live countdown timer (MM:SS format)
- Progress bar (visual representation)
- Progress percentage
- Color-coded time remaining:
  - **Green**: More than 50% time remaining
  - **Yellow**: 25-50% time remaining
  - **Red**: Less than 25% time remaining

## User Interaction

- Timer updates every second
- User can press **Ctrl+C** to stop timer early
- Completion shows success message
- Interruption shows friendly message

## When to Use

- When user wants to focus on a specific task
- When implementing Pomodoro technique workflow
- When tracking time spent on tasks
- When encouraging focused, distraction-free work

## Callback Support

You can provide an optional callback function that executes when the timer completes:

```python
def on_session_complete():
    print("Great work! Time for a break.")
    # Award bonus XP, update stats, etc.

focus.start_focus_session_skill(
    task_title="Complete report",
    duration_minutes=25,
    on_complete=on_session_complete
)
```

## Error Handling

- Raises RuntimeError if Rich library not installed
- Returns False if timer already running when trying to start new session
- Gracefully handles user interruption (Ctrl+C)

## Dependencies

- Rich library (required for Live display and formatting)

## Notes

- Only one timer can run at a time
- Timer runs in the main thread with live display updates
- Progress bar uses block characters (█ and ░)
- Timer is accurate to within 1 second
- Interrupting a session does not trigger the on_complete callback
- Break timer uses same UI as focus timer with "☕ Break Time" title
