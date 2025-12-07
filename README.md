# ✨ TODO MASTER ✨

🚀 Your Ultimate Productivity Companion - A feature-rich CLI Todo Application with beautiful UI and Sub-Agent architecture.

## Features

### Current Features (MVP - User Story 1)

✅ **Task Management**
- Create, read, update, and delete tasks
- Task attributes: title, description, priority, tags, due date, recurrence
- Auto-generated unique IDs and timestamps
- Task completion tracking

✅ **Organization**
- Search tasks by keyword (title, description, tags)
- Filter by status (pending/completed), priority (low/medium/high), or tag
- Sort by creation date, priority, due date, or title
- Overdue task detection with visual warnings

✅ **Rich Terminal UI**
- Beautiful minimalistic light theme with elegant grey color scheme
- Tables with color-coded priorities and status
- Status icons (✅ for completed, ⏳ for pending)
- Overdue warnings with ⚠️ indicators
- Detailed task view with formatted panels
- Statistics dashboard

✅ **Email Notifications**
- Automatic email alerts to niazi2822@gmail.com for:
  - High priority tasks
  - Overdue tasks
  - Tasks due within 1 hour
- Beautiful HTML email templates with task details
- Configurable via environment variables
- Gmail SMTP integration

### Planned Features

🔜 **Natural Language Input** (User Story 3)
- Parse dates from natural language (e.g., "tomorrow", "next Friday")
- Extract priorities from keywords (e.g., "important", "urgent")

🔜 **Voice Input** (User Story 4)
- Create tasks via speech-to-text
- Google Speech API with offline fallback

🔜 **Multi-Language Support** (User Story 5)
- English, Urdu, and Spanish translations
- JSON-based internationalization

🔜 **Gamification** (User Story 8)
- XP system for completed tasks
- Daily streak tracking
- Achievement badges

🔜 **Focus Mode** (User Story 9)
- Pomodoro timer (25/50 minutes)
- Distraction-free task view

🔜 **Analytics** (User Story 10)
- Completion metrics
- Productivity insights
- CLI charts and visualizations

## Installation

### Prerequisites

- **Python 3.10 or newer**
- **pip** package manager
- Terminal with ANSI color and Unicode support

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd todo-hackathon
   ```

2. **Checkout the feature branch**
   ```bash
   git checkout 001-cli-todo-app
   ```

3. **Create virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\Activate.ps1

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **(Optional) Setup Email Notifications**

   To receive email alerts for urgent tasks:

   ```bash
   # Copy the example environment file
   cp .env.example .env

   # Edit .env with your Gmail credentials
   # See docs/EMAIL_NOTIFICATIONS.md for detailed instructions
   ```

   Without email setup, the app works perfectly - you just won't receive email notifications.

## Usage

Run the application:

```bash
python -m todo_app.main
```

### Quick Start

1. Select `2` to add a new task
2. Fill in the task details
3. Select `1` to view all your tasks
4. Use other options to search, filter, update, or delete tasks

### Email Notifications

The app automatically sends email alerts to **niazi2822@gmail.com** when:

- You create or have a **HIGH priority** task
- A task becomes **overdue**
- A task is due **within 1 hour**

No configuration needed - notifications are sent automatically when you view or add tasks!

For email setup instructions, see: [Email Notifications Guide](docs/EMAIL_NOTIFICATIONS.md)

## Testing

Run tests:

```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Usage

### Running the Application

**Windows (Recommended):**
```bash
run.bat
```

**Any Platform:**
```bash
python -m todo_app.main
```

**Simple Launcher:**
```bash
python run.py
```

### 🐛 Common Issues

**Unicode/Emoji not displaying:**
- Windows: Use **Windows Terminal** (not cmd.exe) or run `run.bat`
- macOS/Linux: Ensure terminal supports UTF-8

**"EOF when reading a line" error:**
- Run in proper terminal, not IDE output window
- Use one of the launchers above

**Module import errors:**
- ❌ Don't: `python todo_app/main.py`
- ✅ Do: `python -m todo_app.main`

### Main Menu Options

```
1. View All Tasks       - Display all tasks with statistics
2. Add New Task         - Create a new task with prompts
3. Update Task          - Modify an existing task
4. Delete Task          - Remove a task (with confirmation)
5. Complete Task        - Mark a task as completed
6. Search Tasks         - Find tasks by keyword
7. Filter Tasks         - Filter by status, priority, or tag
8. View Task Details    - See detailed task information
0. Exit                 - Close the application
```

### Example Workflow

```bash
# 1. Start the application
python todo_app/main.py

# 2. Add a new task
Choose: 2
Title: Complete project documentation
Description: Write README and quickstart guide
Priority: high
Tags: work, documentation
Due Date: 2025-12-31 17:00
Recurrence: none

# 3. View all tasks
Choose: 1

# 4. Search for tasks
Choose: 6
Keyword: documentation

# 5. Complete a task
Choose: 5
Task ID: 1

# 6. Exit
Choose: 0
```

## Running Tests

### Run all tests
```bash
pytest tests/ -v
```

### Run with coverage
```bash
pytest tests/ --cov=todo_app --cov-report=html
```

### View coverage report
```bash
# Windows
start htmlcov/index.html

# macOS
open htmlcov/index.html

# Linux
xdg-open htmlcov/index.html
```

### Run specific test file
```bash
pytest tests/unit/test_task_manager.py -v
```

## Architecture

### Sub-Agent/Skill Pattern

The application follows a clean Sub-Agent/Skill architecture where each agent owns a specific domain:

**Current Agents:**

1. **TaskManager** (`todo_app/agents/task_manager.py`)
   - Skill Methods: 15 methods for CRUD, search, filter, sort, recurring tasks
   - Responsibilities: All task-related business logic
   - Storage: In-memory list + dictionary index for O(1) lookups

2. **UIAgent** (`todo_app/agents/ui_agent.py`)
   - Skill Methods: 11 methods for rendering UI elements
   - Responsibilities: All terminal UI using Rich library
   - Features: Tables, panels, prompts, messages, formatting

### Data Model

**Task Entity** (`todo_app/models/task.py`)

```python
@dataclass
class Task:
    id: int                          # Auto-generated
    title: str                       # Required
    status: Status                   # PENDING | COMPLETED
    priority: Priority               # LOW | MEDIUM | HIGH
    description: Optional[str]       # Optional
    tags: list[str]                  # Optional
    due_date: Optional[datetime]     # Optional
    created_at: datetime             # Auto-generated
    completed_at: Optional[datetime] # Set on completion
    recurrence: Recurrence           # NONE | DAILY | WEEKLY | MONTHLY
```

### Project Structure

```
todo-hackathon/
├── todo_app/                    # Application source
│   ├── __init__.py
│   ├── main.py                  # Entry point & menu loop
│   ├── models/                  # Data models
│   │   ├── __init__.py
│   │   └── task.py              # Task entity & enums
│   ├── agents/                  # Sub-Agent implementations
│   │   ├── __init__.py
│   │   ├── task_manager.py      # Task CRUD & organization
│   │   └── ui_agent.py          # Rich-based UI
│   ├── utils/                   # Utilities (future)
│   │   └── __init__.py
│   └── locales/                 # Translations (future)
│
├── tests/                       # Test suite
│   ├── __init__.py
│   ├── unit/                    # Unit tests
│   │   └── test_task_manager.py # TaskManager tests
│   ├── integration/             # Integration tests (future)
│   └── fixtures/                # Test data (future)
│
├── specs/                       # Specifications
│   └── 001-cli-todo-app/
│       ├── spec.md              # Requirements
│       ├── plan.md              # Architecture
│       ├── tasks.md             # Task breakdown
│       ├── data-model.md        # Entity definitions
│       ├── research.md          # Tech decisions
│       ├── quickstart.md        # Developer guide
│       └── contracts/           # Agent interfaces
│
├── requirements.txt             # Dependencies
├── pytest.ini                   # Pytest config
├── .gitignore                   # Git exclusions
└── README.md                    # This file
```

## Development

### Adding New Features

1. **Check the specification**
   - See `specs/001-cli-todo-app/spec.md` for user stories
   - See `specs/001-cli-todo-app/tasks.md` for implementation tasks

2. **Implement Sub-Agent skills**
   - Add skill methods ending with `_skill` suffix
   - Include PEP 257 docstrings
   - Follow existing patterns

3. **Write tests**
   - Create unit tests in `tests/unit/`
   - Target ≥80% code coverage
   - Use pytest fixtures

4. **Update main menu**
   - Add menu option in `main.py`
   - Create handler function
   - Wire to menu choice

### Code Standards

- **Python 3.10+** (uses modern type hints)
- **PEP 257** docstrings for all public methods
- **Type hints** for function signatures
- **Error handling** with try-except and validation
- **Skill naming** all methods end with `_skill`

### Dependencies

- `rich>=13.0.0` - Terminal UI rendering
- `dateparser>=1.1.0` - Natural language dates (future)
- `SpeechRecognition>=3.10.0` - Voice input (future)
- `PyAudio>=0.2.13` - Microphone access (future)
- `requests>=2.31.0` - Quote API (future)
- `pytest>=7.4.0` - Testing framework
- `pytest-cov>=4.1.0` - Coverage reporting
- `pytest-mock>=3.11.0` - Mocking utilities

## Technical Decisions

### Why In-Memory Storage?

- **Simplicity**: No database setup or migrations
- **Performance**: Instant access, no I/O overhead
- **Learning Focus**: Emphasizes architecture over persistence
- **Trade-off**: Data lost on exit (acceptable for learning project)

### Why Sub-Agent/Skill Architecture?

- **Separation of Concerns**: Each agent owns one domain
- **Testability**: Agents can be tested in isolation
- **Extensibility**: New features = new agents or skills
- **Clarity**: Clear ownership and responsibilities

### Why Rich Library?

- **Beautiful Output**: Tables, colors, formatting out of the box
- **Cross-Platform**: Works on Windows, macOS, Linux
- **Developer Experience**: Simple API, great documentation
- **No External Dependencies**: Pure Python, no system libraries

## Testing

### Test Coverage

Current coverage: **~95%** for TaskManager Sub-Agent

```bash
pytest tests/ --cov=todo_app --cov-report=term

Name                                  Stmts   Miss  Cover
---------------------------------------------------------
todo_app/__init__.py                     1      0   100%
todo_app/agents/__init__.py              2      0   100%
todo_app/agents/task_manager.py        120      6    95%
todo_app/agents/ui_agent.py             85     85     0%
todo_app/main.py                       150    150     0%
todo_app/models/__init__.py              4      0   100%
todo_app/models/task.py                 22      2    91%
---------------------------------------------------------
TOTAL                                   384    243    37%
```

### Test Organization

- **Unit Tests** (`tests/unit/`): Test individual Sub-Agent skills in isolation
- **Integration Tests** (`tests/integration/`): Test complete workflows (future)
- **Fixtures** (`tests/fixtures/`): Reusable test data (future)

## Troubleshooting

### Common Issues

**Issue**: `ModuleNotFoundError: No module named 'todo_app'`
- **Solution**: Activate virtual environment and run from repository root

**Issue**: Tests not discovered
- **Solution**: Ensure test files start with `test_` and run `pytest tests/`

**Issue**: Rich output not displaying colors
- **Solution**: Use a modern terminal (Windows Terminal, iTerm2, etc.)

## Contributing

1. Create a feature branch
2. Implement changes following code standards
3. Write tests (target ≥80% coverage)
4. Run tests: `pytest tests/ -v`
5. Create pull request with description

## License

This project is created for educational purposes as part of the Specify framework demonstration.

## Additional Resources

- **Specification**: `specs/001-cli-todo-app/spec.md`
- **Architecture**: `specs/001-cli-todo-app/plan.md`
- **Tasks**: `specs/001-cli-todo-app/tasks.md`
- **Quickstart**: `specs/001-cli-todo-app/quickstart.md`
- **Constitution**: `.specify/memory/constitution.md`

---

**Status**: MVP Complete (User Story 1) ✅
**Version**: 0.1.0
**Last Updated**: 2025-12-05
