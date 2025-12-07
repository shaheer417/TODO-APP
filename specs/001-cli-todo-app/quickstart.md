# Quickstart: In-Memory Python CLI Todo Application

**Feature**: CLI Todo App (001-cli-todo-app)
**Last Updated**: 2025-12-05

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.10 or newer** (required by constitution)
- **pip** package manager
- **Git** (for version control)
- **Microphone** (optional, for voice input feature)
- **Terminal** with ANSI color and Unicode support
  - Windows: Windows Terminal or PowerShell 7+
  - macOS: Terminal.app or iTerm2
  - Linux: GNOME Terminal, Konsole, or similar

---

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd todo-hackathon
```

### 2. Checkout Feature Branch

```bash
git checkout 001-cli-todo-app
```

### 3. Create Virtual Environment

**Windows (PowerShell)**:
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux**:
```bash
python3 -m venv venv
source venv/bin/activate
```

**Verify activation** (should show `(venv)` in prompt):
```bash
which python  # macOS/Linux
where python  # Windows
```

### 4. Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Dependencies installed**:
- `rich` - Terminal UI rendering
- `dateparser` - Natural language date parsing
- `SpeechRecognition` - Voice input
- `PyAudio` - Microphone access
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `pytest-mock` - Mocking for tests
- `requests` - HTTP for quote API

### 5. Install Platform-Specific Dependencies (PyAudio)

**Windows**:
```powershell
pip install pyaudio
```

**macOS**:
```bash
brew install portaudio
pip install pyaudio
```

**Linux (Debian/Ubuntu)**:
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Linux (Fedora/RHEL)**:
```bash
sudo dnf install portaudio-devel
pip install pyaudio
```

**Troubleshooting PyAudio**:
- If installation fails, voice input will not work, but all other features remain functional
- See [PyAudio documentation](https://people.csail.mit.edu/hubert/pyaudio/) for detailed platform guides

---

## Running the Application

### Start the Application

```bash
python todo_app/main.py
```

**Expected Output**:
```
╔══════════════════════════════════════╗
║   TODO APPLICATION                   ║
║   Your Productivity Companion        ║
╚══════════════════════════════════════╝

📊 Pending Tasks: 0
🏆 Daily Streak: 0 days

💡 Quote of the Day:
"The future depends on what you do today."
   — Mahatma Gandhi

[Main Menu will appear below]
```

### First-Time Setup

On first run, the application will:
1. Create default configuration (English language, medium priority default)
2. Offer to load sample tasks for demonstration
3. Display welcome screen

---

## Running Tests

### Run All Tests

```bash
pytest tests/ -v
```

### Run Tests with Coverage

```bash
pytest tests/ --cov=todo_app --cov-report=html
```

**View coverage report**:
```bash
open htmlcov/index.html  # macOS
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Test File

```bash
pytest tests/unit/test_task_manager.py -v
```

### Run Tests Matching Pattern

```bash
pytest tests/ -k "test_add" -v
```

---

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Implement Sub-Agent Skills

**File structure**:
```
todo_app/agents/
├── task_manager.py       # Edit this for task CRUD operations
├── ui_agent.py           # Edit this for UI changes
├── nlp_agent.py          # Edit this for NLP parsing
└── ... (other agents)
```

**Example: Adding a new skill to TaskManager**:
```python
# In todo_app/agents/task_manager.py

def get_urgent_tasks_skill(self) -> list[Task]:
    """
    Retrieve all high-priority pending tasks.

    Returns:
        List of Task objects with priority=HIGH and status=PENDING
    """
    return [
        task for task in self.tasks
        if task.priority == Priority.HIGH and task.status == Status.PENDING
    ]
```

### 3. Write Unit Tests

**File structure**:
```
tests/unit/
├── test_task_manager.py  # Tests for TaskManager skills
├── test_nlp_agent.py     # Tests for NLPAgent skills
└── ... (other test files)
```

**Example test**:
```python
# In tests/unit/test_task_manager.py

def test_get_urgent_tasks_skill(task_manager):
    """Test filtering for high-priority pending tasks."""
    # Setup
    task_manager.add_task_skill(title="Urgent task", priority=Priority.HIGH)
    task_manager.add_task_skill(title="Normal task", priority=Priority.MEDIUM)

    # Execute
    urgent = task_manager.get_urgent_tasks_skill()

    # Assert
    assert len(urgent) == 1
    assert urgent[0].title == "Urgent task"
```

### 4. Run Tests and Check Coverage

```bash
pytest tests/ --cov=todo_app --cov-report=term
```

**Target**: ≥80% coverage for all Sub-Agent skills

### 5. Format and Lint Code

**Format with Black**:
```bash
black todo_app/ tests/
```

**Lint with Pylint**:
```bash
pylint todo_app/
```

**Type Check with mypy** (optional):
```bash
mypy todo_app/
```

### 6. Commit Changes

```bash
git add .
git commit -m "feat: add get_urgent_tasks_skill to TaskManager

- Implemented skill to filter high-priority pending tasks
- Added unit tests with 100% coverage
- Updated agent_interfaces.md documentation"
```

**Commit Message Format**:
- `feat:` - New feature
- `fix:` - Bug fix
- `test:` - Adding tests
- `docs:` - Documentation updates
- `refactor:` - Code refactoring

### 7. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create PR on GitHub/GitLab with:
- Description of changes
- Link to related issue (if applicable)
- Screenshots (for UI changes)
- Test results

---

## Project Structure Overview

```
todo-hackathon/
├── todo_app/                    # Application source code
│   ├── main.py                  # Entry point, main menu loop
│   ├── models/                  # Data models
│   │   ├── task.py              # Task entity
│   │   ├── user_profile.py      # UserProfile entity
│   │   └── config.py            # Configuration entity
│   ├── agents/                  # Sub-Agent implementations
│   │   ├── task_manager.py      # Task CRUD, search, filter, sort
│   │   ├── ui_agent.py          # Rich-based UI rendering
│   │   ├── nlp_agent.py         # Natural language parsing
│   │   ├── voice_agent.py       # Speech-to-text
│   │   ├── language_agent.py    # Multi-language support
│   │   ├── gamification_agent.py # XP, streaks, badges
│   │   ├── focus_agent.py       # Pomodoro timer
│   │   └── analytics_agent.py   # Metrics and charts
│   ├── locales/                 # Translation files
│   │   ├── en.json              # English
│   │   ├── ur.json              # Urdu
│   │   └── es.json              # Spanish
│   ├── utils/                   # Helper functions
│   │   ├── validators.py        # Input validation
│   │   └── quotes.py            # Quote of the day
│   └── config.json              # Runtime configuration
│
├── tests/                       # Test suite
│   ├── unit/                    # Unit tests (isolated)
│   │   ├── test_task_manager.py
│   │   ├── test_nlp_agent.py
│   │   └── ... (other unit tests)
│   ├── integration/             # Integration tests (workflows)
│   │   ├── test_task_workflows.py
│   │   ├── test_voice_to_task.py
│   │   └── test_multi_language.py
│   └── fixtures/                # Test data and fixtures
│       ├── sample_tasks.py
│       └── test_data.py
│
├── specs/                       # Feature specifications
│   └── 001-cli-todo-app/
│       ├── spec.md              # Feature requirements
│       ├── plan.md              # Implementation plan
│       ├── research.md          # Technology decisions
│       ├── data-model.md        # Entity definitions
│       ├── quickstart.md        # This file
│       └── contracts/           # Agent interfaces
│
├── docs/                        # Documentation
│   ├── README.md                # User guide
│   └── future_improvements.md   # Enhancement ideas
│
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── .gitignore                   # Git exclusions
└── CLAUDE.md                    # Project constitution
```

---

## Key Commands Reference

### Running the Application

| Command | Description |
|---------|-------------|
| `python todo_app/main.py` | Start the application |
| `python todo_app/main.py --demo` | Load sample tasks on startup |
| `python todo_app/main.py --lang ur` | Start in Urdu language |

### Testing

| Command | Description |
|---------|-------------|
| `pytest tests/ -v` | Run all tests (verbose) |
| `pytest tests/ --cov=todo_app` | Run tests with coverage |
| `pytest tests/ --cov-report=html` | Generate HTML coverage report |
| `pytest tests/unit/` | Run only unit tests |
| `pytest tests/integration/` | Run only integration tests |
| `pytest -k "test_task"` | Run tests matching pattern |
| `pytest --lf` | Run only last failed tests |

### Code Quality

| Command | Description |
|---------|-------------|
| `black todo_app/ tests/` | Format code with Black |
| `black --check todo_app/` | Check formatting without changes |
| `pylint todo_app/` | Lint code with Pylint |
| `mypy todo_app/` | Type check with mypy |
| `flake8 todo_app/` | Check PEP 8 compliance |

### Git

| Command | Description |
|---------|-------------|
| `git status` | Check working tree status |
| `git log --oneline` | View commit history |
| `git diff` | Show unstaged changes |
| `git branch -a` | List all branches |

---

## Troubleshooting

### Issue: Voice input not working

**Symptoms**: "Microphone not found" error when selecting voice input

**Solutions**:
1. Verify microphone is connected and working (test with system voice recorder)
2. Check PyAudio installation: `python -c "import pyaudio; print(pyaudio.__version__)"`
3. On Linux, check permissions: `groups` (user should be in `audio` group)
4. Reinstall PyAudio with platform-specific instructions above

**Workaround**: Use text input instead of voice input

---

### Issue: Urdu text not rendering correctly

**Symptoms**: Urdu characters appear as boxes or incorrect glyphs

**Solutions**:
1. Verify terminal supports Unicode: `echo "اردو"` (should display Urdu text)
2. Install Urdu fonts:
   - Windows: Urdu Typesetting (built-in)
   - macOS: Geeza Pro (built-in)
   - Linux: `sudo apt-get install fonts-noto-nastaliq-urdu`
3. Use modern terminal (Windows Terminal, iTerm2, etc.)

**Workaround**: Switch to English or Spanish: Settings → Language → English

---

### Issue: Tests failing with "ModuleNotFoundError"

**Symptoms**: `ModuleNotFoundError: No module named 'todo_app'`

**Solutions**:
1. Ensure virtual environment is activated (check for `(venv)` in prompt)
2. Run tests from repository root: `cd /path/to/todo-hackathon && pytest tests/`
3. Reinstall dependencies: `pip install -r requirements.txt`

---

### Issue: Application startup slow (>5 seconds)

**Symptoms**: Long delay before main menu appears

**Solutions**:
1. Check quote API timeout (should fail gracefully after 5 seconds)
2. Disable quote fetching: Comment out quote API call in main.py (temporary)
3. Check internet connection (quote API requires network)

**Workaround**: Quote will fallback to embedded quotes if API times out

---

### Issue: Python version check failed

**Symptoms**: `SyntaxError` or "requires Python 3.10+" message

**Solutions**:
1. Check Python version: `python --version` (must be 3.10 or newer)
2. Use specific version: `python3.10 -m venv venv`
3. Install Python 3.10+: Visit [python.org/downloads](https://www.python.org/downloads/)

---

## Next Steps

After completing setup:

1. **Explore the codebase**: Read through `todo_app/agents/` to understand Sub-Agent structure
2. **Run the tests**: Execute `pytest tests/ -v` to see all tests pass
3. **Try the application**: Run `python todo_app/main.py` and experiment with features
4. **Read the docs**: Review `specs/001-cli-todo-app/plan.md` for architecture overview
5. **Start implementing**: Pick a task from `specs/001-cli-todo-app/tasks.md` (generated by `/sp.tasks`)

---

## Additional Resources

- **Constitution**: `.specify/memory/constitution.md` - Project principles and standards
- **Specification**: `specs/001-cli-todo-app/spec.md` - Feature requirements
- **Architecture Plan**: `specs/001-cli-todo-app/plan.md` - Implementation strategy
- **Agent Contracts**: `specs/001-cli-todo-app/contracts/agent_interfaces.md` - API documentation
- **Research**: `specs/001-cli-todo-app/research.md` - Technology decisions

---

## Support

For questions or issues:

1. Check this quickstart guide first
2. Review troubleshooting section above
3. Search existing issues on GitHub/GitLab
4. Create new issue with:
   - Steps to reproduce
   - Expected vs actual behavior
   - Python version and OS
   - Relevant error messages

---

**Quickstart Status**: ✅ Complete
**Ready for Development**: Yes
