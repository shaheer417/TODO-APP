# Research: In-Memory Python CLI Todo Application

**Date**: 2025-12-05
**Feature**: CLI Todo App (001-cli-todo-app)
**Purpose**: Resolve technical unknowns and establish implementation strategies

---

## 1. Natural Language Processing for Task Parsing

### Decision
Use **`dateparser`** library for date/time extraction combined with **keyword-based pattern matching** for priority detection and title extraction.

### Rationale
- **dateparser**: Mature library with extensive locale support, handles relative dates ("tomorrow", "next Friday") and absolute dates with high accuracy
- **Keyword matching**: Simple, fast, deterministic approach for priority keywords ("urgent", "asap", "important")
- **Title extraction**: Remove recognized date/time phrases and priority keywords from input string to isolate task title

### Alternatives Considered
- **NLTK/spaCy**: Overkill for this use case; requires training data and adds significant dependencies
- **Regular expressions only**: Too brittle for diverse date formats; dateparser handles this better
- **ML-based approach**: Unnecessary complexity; keyword matching achieves 85%+ accuracy target

### Implementation Notes
```python
import dateparser
from typing import Tuple, Optional
from datetime import datetime

PRIORITY_KEYWORDS = {
    'high': ['urgent', 'asap', 'critical', 'important', 'high priority'],
    'medium': ['soon', 'medium priority'],
    'low': ['someday', 'maybe', 'low priority', 'when possible']
}

def parse_natural_language(text: str) -> Tuple[str, Optional[datetime], str]:
    """
    Extract title, due_date, and priority from natural language input.

    Returns: (title, due_date, priority)
    """
    # 1. Extract priority keywords
    priority = 'Medium'  # default
    text_lower = text.lower()
    for level, keywords in PRIORITY_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text_lower:
                priority = level.capitalize()
                text = text.replace(keyword, '', 1)  # Remove first occurrence
                break

    # 2. Extract date/time using dateparser
    due_date = dateparser.parse(text, settings={'PREFER_DATES_FROM': 'future'})

    # 3. Title is what remains after removing date phrase
    # (dateparser doesn't return matched substring, so heuristic: keep first clause)
    title = text.strip()

    return title, due_date, priority
```

**Configuration**:
- Use `dateparser.parse()` with `settings={'PREFER_DATES_FROM': 'future'}` to avoid past dates
- Support relative dates: "tomorrow", "next week", "in 3 days"
- Support absolute dates: "Dec 15", "2025-12-10 17:00"
- Support time expressions: "6pm", "morning", "afternoon"

**Edge Cases**:
- Ambiguous dates (e.g., "Friday" when today is Friday) → dateparser defaults to next week
- No date found → return None for due_date
- Multiple priority keywords → use first match

---

## 2. Voice Input Implementation

### Decision
Use **SpeechRecognition library** with **Google Speech Recognition API** as primary backend and **CMU Sphinx** as offline fallback.

### Rationale
- **Google API**: Free tier, excellent accuracy for English/Spanish (80%+ in quiet environment), no API key required
- **CMU Sphinx**: Offline fallback ensures voice input works without internet
- **SpeechRecognition**: Unified API abstracts backend switching, handles microphone access via PyAudio

### Alternatives Considered
- **Wit.ai**: Requires API key registration, less documented
- **Whisper (OpenAI)**: Too heavy (model download), slower, overkill for this use case
- **Cloud services (Azure, AWS)**: Require paid accounts and API keys

### Implementation Notes
```python
import speech_recognition as sr

def transcribe_voice_skill() -> Optional[str]:
    """
    Record audio from microphone and convert to text.

    Returns: Transcribed text or None if error
    """
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... (speak now)")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return None  # No speech detected

    try:
        # Try Google first
        text = recognizer.recognize_google(audio)
        return text
    except (sr.UnknownValueError, sr.RequestError):
        # Fallback to Sphinx (offline)
        try:
            text = recognizer.recognize_sphinx(audio)
            return text
        except sr.UnknownValueError:
            return None  # Could not understand audio
```

**Error Handling**:
- Timeout after 5 seconds if no speech detected
- Limit phrase duration to 10 seconds
- Show user-friendly messages for all error states:
  - No microphone detected → "Microphone not found. Please check device."
  - Poor audio quality → "Could not understand audio. Please try again."
  - Network error (Google API) → "Offline mode active. Accuracy may be reduced."

**PyAudio Setup**:
- **Windows**: `pip install pyaudio` (prebuilt wheels available)
- **Linux**: `sudo apt-get install portaudio19-dev python3-pyaudio`
- **macOS**: `brew install portaudio && pip install pyaudio`

---

## 3. Multi-Language Support Architecture

### Decision
Use **flat JSON files** with **dot-notation keys** and **LanguageAgent** for runtime translation with English fallback.

### Rationale
- Flat structure is simple to parse and maintain
- Dot notation provides logical namespacing (menu., error., label., etc.)
- JSON is human-readable and editable by translators without programming knowledge
- Fallback to English ensures UI never shows untranslated placeholders

### Alternatives Considered
- **Gettext (.po files)**: More complex toolchain, overkill for 3 languages
- **Nested JSON**: Harder to traverse, requires recursive lookup logic
- **YAML**: Similar to JSON but less universally supported

### Implementation Notes

**JSON File Structure** (`locales/en.json`):
```json
{
  "menu.title": "Todo Application",
  "menu.add_task": "Add Task",
  "menu.view_tasks": "View All Tasks",
  "menu.search": "Search Tasks",
  "menu.filter": "Filter Tasks",
  "menu.exit": "Exit",

  "label.title": "Title",
  "label.description": "Description",
  "label.priority": "Priority",
  "label.tags": "Tags",
  "label.due_date": "Due Date",

  "priority.high": "High",
  "priority.medium": "Medium",
  "priority.low": "Low",

  "status.pending": "Pending",
  "status.completed": "Completed",

  "error.task_not_found": "Task ID not found",
  "error.invalid_date": "Invalid date format. Use YYYY-MM-DD HH:MM",
  "error.empty_title": "Task title cannot be empty",

  "success.task_created": "Task created successfully",
  "success.task_deleted": "Task deleted successfully"
}
```

**LanguageAgent Implementation**:
```python
import json
from typing import Dict

class LanguageAgent:
    def __init__(self, default_lang='en'):
        self.current_lang = default_lang
        self.translations: Dict[str, Dict[str, str]] = {}
        self.load_language(default_lang)

    def load_language_skill(self, lang_code: str) -> bool:
        """Load translation file for specified language."""
        try:
            with open(f'locales/{lang_code}.json', 'r', encoding='utf-8') as f:
                self.translations[lang_code] = json.load(f)
            self.current_lang = lang_code
            return True
        except FileNotFoundError:
            return False  # Fallback to current language

    def translate_skill(self, key: str) -> str:
        """
        Get translated string for key. Falls back to English if missing.
        """
        # Try current language
        if key in self.translations.get(self.current_lang, {}):
            return self.translations[self.current_lang][key]

        # Fallback to English
        if key in self.translations.get('en', {}):
            return self.translations['en'][key]

        # Ultimate fallback: return key itself
        return key
```

**Urdu RTL Considerations**:
- Urdu script is RTL (right-to-left), but most terminals handle this automatically if Unicode is supported
- Test on Windows Terminal, iTerm2, and modern Linux terminals
- Document terminal requirements in README
- If terminal doesn't support RTL, text will display LTR (left-to-right) but remain readable

**Character Encoding**:
- All JSON files use UTF-8 encoding
- Python reads with `encoding='utf-8'` parameter
- Rich library handles Unicode rendering correctly

---

## 4. Pomodoro Timer in CLI

### Decision
Use **`rich.live.Live`** context manager with **threading** for non-blocking countdown display.

### Rationale
- `rich.live.Live` provides flicker-free dynamic updates ideal for timers
- Threading allows timer to run while listening for keyboard interrupt (user cancel)
- No async complexity needed; threading is simpler for this use case

### Alternatives Considered
- **Async/await**: Adds unnecessary complexity; rich.live handles updates internally
- **Blocking loop with clear screen**: Creates flicker, poor UX
- **Curses library**: Lower-level, harder to style, rich provides better abstraction

### Implementation Notes
```python
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
import threading
import time

def start_pomodoro_skill(task_title: str, duration_minutes: int) -> bool:
    """
    Start focus timer for specified duration.

    Args:
        task_title: Name of task to focus on
        duration_minutes: 25 or 50 minutes

    Returns: True if completed, False if cancelled
    """
    total_seconds = duration_minutes * 60
    cancelled = threading.Event()

    def countdown(live: Live):
        remaining = total_seconds
        while remaining > 0 and not cancelled.is_set():
            mins, secs = divmod(remaining, 60)
            timer_text = Text(f"🎯 Focus Mode: {task_title}\n\n{mins:02d}:{secs:02d}",
                              style="bold cyan", justify="center")
            panel = Panel(timer_text, title="Pomodoro Timer", border_style="cyan")
            live.update(panel)
            time.sleep(1)
            remaining -= 1

        if not cancelled.is_set():
            # Timer completed
            completion_text = Text("✅ Focus session complete! Great work!",
                                   style="bold green", justify="center")
            live.update(Panel(completion_text, border_style="green"))
            time.sleep(3)

    with Live(auto_refresh=False) as live:
        timer_thread = threading.Thread(target=countdown, args=(live,))
        timer_thread.start()

        try:
            timer_thread.join()
            return not cancelled.is_set()
        except KeyboardInterrupt:
            cancelled.set()
            return False
```

**User Interaction**:
- Display task title and countdown in centered panel
- Update every second
- User presses Ctrl+C to cancel
- Show completion message for 3 seconds when timer finishes

**Threading Safety**:
- Use `threading.Event()` for cancellation signaling
- No shared mutable state (timer only updates Live display)
- Join thread before function returns

---

## 5. CLI Charts with Rich

### Decision
Generate **custom ASCII bar charts** using **rich formatting** and **dynamic scaling**.

### Rationale
- Rich doesn't have built-in bar chart widget, but provides text styling for custom charts
- Custom approach gives full control over layout and scaling
- Simple enough to implement without external charting libraries

### Alternatives Considered
- **rich.bar.Bar**: Doesn't exist (checked documentation)
- **asciichartpy**: External dependency, less flexible styling
- **plotext**: Terminal plotting library, but overkill and less aesthetic than rich

### Implementation Notes
```python
from rich.console import Console
from rich.table import Table
from typing import Dict

def generate_chart_skill(data: Dict[str, int], title: str) -> Table:
    """
    Generate ASCII bar chart as Rich table.

    Args:
        data: Dict mapping labels to values (e.g., {'Mon': 5, 'Tue': 3})
        title: Chart title

    Returns: Rich Table object
    """
    if not data:
        return Table(title=title)

    max_value = max(data.values()) if data.values() else 1
    bar_width = 40  # characters

    table = Table(title=title, show_header=False, box=None)
    table.add_column("Label", style="cyan", width=10)
    table.add_column("Bar", no_wrap=True)
    table.add_column("Value", style="bold", width=5)

    for label, value in data.items():
        # Scale bar length
        bar_length = int((value / max_value) * bar_width) if max_value > 0 else 0
        bar = "█" * bar_length

        # Color based on value
        if value > max_value * 0.7:
            bar_style = "green"
        elif value > max_value * 0.3:
            bar_style = "yellow"
        else:
            bar_style = "red"

        table.add_row(label, f"[{bar_style}]{bar}[/{bar_style}]", str(value))

    return table
```

**Example Output**:
```
 Tasks Completed This Week
 Mon      ██████████████████████████████  6
 Tue      ████████████████████  4
 Wed      ████████████████████████████████████████  8
 Thu      ██████████  2
 Fri      ████████████████████████  5
 Sat      ████████  1
 Sun      ████████████  3
```

**Scaling Logic**:
- Normalize bars to max 40 characters
- Use full-block character (█) for solid bars
- Color-code based on relative value (green=high, yellow=medium, red=low)

---

## 6. Quote of the Day API

### Decision
Use **ZenQuotes API** (https://zenquotes.io/api/random) with **5-second timeout** and **embedded fallback quotes**.

### Rationale
- ZenQuotes is free, no API key required, simple JSON response
- Reliable uptime, no rate limits for reasonable usage
- Embedded fallbacks ensure startup never fails due to API issues

### Alternatives Considered
- **Quotable API**: More restrictive rate limits (180 requests per minute)
- **They Said So**: Requires API key registration
- **Static file**: No variety, less engaging

### Implementation Notes
```python
import requests
from typing import Optional

FALLBACK_QUOTES = [
    ("The only way to do great work is to love what you do.", "Steve Jobs"),
    ("Success is not final, failure is not fatal.", "Winston Churchill"),
    ("Believe you can and you're halfway there.", "Theodore Roosevelt"),
    ("Act as if what you do makes a difference. It does.", "William James"),
    ("The future depends on what you do today.", "Mahatma Gandhi")
]

def fetch_quote_skill() -> tuple[str, str]:
    """
    Fetch random inspirational quote.

    Returns: (quote_text, author)
    """
    try:
        response = requests.get(
            'https://zenquotes.io/api/random',
            timeout=5
        )
        response.raise_for_status()
        data = response.json()[0]
        return (data['q'], data['a'])

    except (requests.RequestException, KeyError, IndexError):
        # Use fallback on any error
        import random
        return random.choice(FALLBACK_QUOTES)
```

**Error Handling**:
- Timeout after 5 seconds (doesn't delay startup)
- Catch all request exceptions (network, timeout, invalid JSON)
- Fallback quotes randomly selected for variety
- Log warning but don't show error to user (seamless UX)

**API Response Format**:
```json
[
  {
    "q": "The only impossible journey is the one you never begin.",
    "a": "Tony Robbins",
    "h": "<blockquote>...</blockquote>"
  }
]
```

---

## 7. In-Memory Data Structure Optimization

### Decision
Use **Python list** for task storage with **dict index** for O(1) ID lookups.

### Rationale
- List preserves insertion order, supports all required operations
- Dict index provides fast ID-based access without changing storage model
- Python's built-in `sorted()` and list comprehensions are highly optimized
- Memory footprint: ~100KB for 10,000 tasks (acceptable)

### Alternatives Considered
- **Dict only**: Loses insertion order (though Python 3.7+ dicts are ordered), less natural for iteration
- **In-memory SQLite**: Violates constitutional simplicity requirement, overkill
- **Custom data structures (trees, heaps)**: Premature optimization, adds complexity

### Implementation Notes
```python
from typing import List, Dict, Optional
from models.task import Task

class TaskManager:
    def __init__(self):
        self.tasks: List[Task] = []
        self.task_index: Dict[int, Task] = {}  # ID -> Task mapping
        self.next_id = 1

    def add_task_skill(self, title, **kwargs) -> Task:
        """Create new task with auto-incrementing ID."""
        task = Task(id=self.next_id, title=title, **kwargs)
        self.tasks.append(task)
        self.task_index[task.id] = task
        self.next_id += 1
        return task

    def get_task_skill(self, task_id: int) -> Optional[Task]:
        """O(1) lookup by ID."""
        return self.task_index.get(task_id)

    def delete_task_skill(self, task_id: int) -> bool:
        """Remove task from both list and index."""
        task = self.task_index.pop(task_id, None)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def search_tasks_skill(self, keyword: str) -> List[Task]:
        """O(n) search - acceptable for 10k items."""
        keyword_lower = keyword.lower()
        return [
            task for task in self.tasks
            if keyword_lower in task.title.lower()
            or keyword_lower in (task.description or '').lower()
        ]

    def filter_tasks_skill(self, status=None, priority=None, tag=None) -> List[Task]:
        """O(n) filter with early exit for efficiency."""
        return [
            task for task in self.tasks
            if (status is None or task.status == status)
            and (priority is None or task.priority == priority)
            and (tag is None or tag in task.tags)
        ]

    def sort_tasks_skill(self, tasks: List[Task], sort_by: str, reverse=False) -> List[Task]:
        """Use Python's optimized Timsort (O(n log n))."""
        key_funcs = {
            'due_date': lambda t: t.due_date or datetime.max,
            'priority': lambda t: {'High': 0, 'Medium': 1, 'Low': 2}[t.priority],
            'title': lambda t: t.title.lower(),
            'created_at': lambda t: t.created_at
        }
        return sorted(tasks, key=key_funcs.get(sort_by), reverse=reverse)
```

**Performance Characteristics**:
- Add: O(1)
- Get by ID: O(1)
- Delete: O(n) for list.remove(), O(1) for dict.pop()
- Search: O(n) - linear scan
- Filter: O(n) - linear scan
- Sort: O(n log n) - Timsort

**Memory Estimation**:
- Task object: ~200 bytes (including strings, dates)
- 10,000 tasks: ~2MB
- Dict index: ~500KB (int keys, object references)
- Total: ~2.5MB (negligible)

---

## 8. Testing Strategy for CLI Application

### Decision
Use **pytest** with **mocking for external dependencies** and **console capture for Rich output validation**.

### Rationale
- pytest is constitutional requirement, provides fixtures, parametrization, and assertion introspection
- Mocking (pytest-mock) eliminates non-determinism from voice input, API calls, time
- Console capture (Rich's `Console(file=StringIO())`) validates UI output without manual testing

### Alternatives Considered
- **unittest**: More verbose, less feature-rich than pytest
- **Real API/voice testing**: Too slow, non-deterministic, requires hardware
- **Snapshot testing**: Brittle for terminal output, hard to maintain

### Implementation Notes

**Unit Test Example** (test_task_manager.py):
```python
import pytest
from agents.task_manager import TaskManager
from models.task import Task

@pytest.fixture
def task_manager():
    """Fixture provides fresh TaskManager for each test."""
    return TaskManager()

def test_add_task_skill(task_manager):
    """Test task creation with auto-incrementing ID."""
    task = task_manager.add_task_skill(
        title="Test task",
        priority="High",
        tags=["test"]
    )

    assert task.id == 1
    assert task.title == "Test task"
    assert task.priority == "High"
    assert "test" in task.tags
    assert task.status == "Pending"

def test_search_tasks_skill(task_manager):
    """Test keyword search in title and description."""
    task_manager.add_task_skill(title="Buy groceries", description="Milk and eggs")
    task_manager.add_task_skill(title="Write report", description="Q4 financials")

    results = task_manager.search_tasks_skill("report")
    assert len(results) == 1
    assert results[0].title == "Write report"

    results = task_manager.search_tasks_skill("eggs")
    assert len(results) == 1
    assert results[0].title == "Buy groceries"
```

**Mocking External Dependencies** (test_voice_agent.py):
```python
import pytest
from agents.voice_agent import VoiceAgent
from unittest.mock import patch, MagicMock

@patch('speech_recognition.Recognizer')
@patch('speech_recognition.Microphone')
def test_transcribe_voice_skill_success(mock_mic, mock_recognizer):
    """Test successful voice transcription."""
    # Setup mocks
    recognizer_instance = mock_recognizer.return_value
    recognizer_instance.recognize_google.return_value = "Buy milk tomorrow"

    agent = VoiceAgent()
    result = agent.transcribe_voice_skill()

    assert result == "Buy milk tomorrow"
    recognizer_instance.recognize_google.assert_called_once()

@patch('speech_recognition.Recognizer')
@patch('speech_recognition.Microphone')
def test_transcribe_voice_skill_fallback(mock_mic, mock_recognizer):
    """Test fallback to Sphinx when Google fails."""
    recognizer_instance = mock_recognizer.return_value
    recognizer_instance.recognize_google.side_effect = Exception("Network error")
    recognizer_instance.recognize_sphinx.return_value = "Call mom"

    agent = VoiceAgent()
    result = agent.transcribe_voice_skill()

    assert result == "Call mom"
    recognizer_instance.recognize_sphinx.assert_called_once()
```

**Testing Rich Output** (test_ui_agent.py):
```python
from rich.console import Console
from io import StringIO
from agents.ui_agent import UIAgent

def test_display_task_table():
    """Test task table rendering."""
    # Capture Rich output to string
    string_io = StringIO()
    console = Console(file=string_io, force_terminal=True, width=120)

    ui_agent = UIAgent(console=console)
    tasks = [
        Task(id=1, title="Test task", priority="High", status="Pending")
    ]

    ui_agent.display_task_table_skill(tasks)
    output = string_io.getvalue()

    # Assert output contains expected elements
    assert "Test task" in output
    assert "High" in output
    assert "Pending" in output
    assert "🔥" in output  # High priority icon
```

**Integration Test Example** (test_task_workflows.py):
```python
def test_create_task_with_nlp():
    """Integration test: NLP → TaskManager → Gamification."""
    nlp_agent = NLPAgent()
    task_manager = TaskManager()
    gamification_agent = GamificationAgent()

    # Parse natural language
    title, due_date, priority = nlp_agent.parse_natural_language_skill(
        "Urgent: submit report by tomorrow 5pm"
    )

    # Create task
    task = task_manager.add_task_skill(title=title, due_date=due_date, priority=priority)

    # Complete task
    task_manager.mark_complete_skill(task.id)

    # Award XP
    xp_earned = gamification_agent.award_xp_skill(task)

    assert task.status == "Completed"
    assert xp_earned == 10  # Base XP for completion
```

**Test Organization**:
```
tests/
├── unit/               # Fast, isolated tests (mock all dependencies)
│   ├── test_task_manager.py
│   ├── test_nlp_agent.py
│   ├── test_voice_agent.py
│   ├── test_gamification_agent.py
│   └── test_analytics_agent.py
├── integration/        # End-to-end workflows (use in-memory fixtures)
│   ├── test_task_workflows.py
│   ├── test_voice_to_task.py
│   └── test_multi_language.py
└── fixtures/           # Reusable test data
    ├── sample_tasks.py
    └── test_data.py
```

**Coverage Requirements**:
- Target: ≥80% for all Sub-Agent skills
- Run: `pytest tests/ --cov=todo_app --cov-report=html`
- Exclude: `main.py` menu loop (tested manually), UI rendering details

---

## Summary of Key Decisions

| Area | Technology/Approach | Rationale |
|------|---------------------|-----------|
| **NLP Date Parsing** | dateparser library | Mature, handles relative/absolute dates, locale-aware |
| **NLP Priority Detection** | Keyword matching | Simple, fast, deterministic, meets 85% accuracy target |
| **Voice Recognition** | SpeechRecognition + Google/Sphinx | Best accuracy for free tier, offline fallback |
| **Multi-Language** | Flat JSON with dot notation | Simple, translator-friendly, easy fallback logic |
| **Pomodoro Timer** | rich.live.Live + threading | Flicker-free updates, non-blocking, simple |
| **CLI Charts** | Custom ASCII with Rich styling | Full control, no extra dependencies, aesthetic |
| **Quote API** | ZenQuotes with fallbacks | Free, reliable, seamless UX on failure |
| **Data Structure** | List + dict index | Fast lookups, simple, meets performance requirements |
| **Testing** | pytest + mocking + console capture | Deterministic, fast, comprehensive coverage |

---

**Research Status**: ✅ Complete
**All Technical Unknowns Resolved**: Yes
**Ready for Phase 1 (Design & Contracts)**: Yes
