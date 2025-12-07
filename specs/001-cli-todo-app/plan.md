# Implementation Plan: In-Memory Python CLI Todo Application

**Branch**: `001-cli-todo-app` | **Date**: 2025-12-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-cli-todo-app/spec.md`

## Summary

Develop a comprehensive, feature-rich in-memory Python CLI todo application with advanced capabilities including natural language processing, voice input, multi-language support, gamification mechanics, focus mode (Pomodoro timer), and productivity analytics. The application follows a modular Sub-Agent/Skill architecture where each functional domain (task management, UI, analytics, gamification, etc.) is encapsulated in dedicated agent classes with independently testable skill methods.

**Technical Approach**: Build a menu-driven CLI using the `rich` library for professional terminal UI. Implement core task CRUD operations first (P1), followed by organization features (P2), then layer advanced features (P3-P12) incrementally. Use `dateparser` for natural language date parsing, `SpeechRecognition` for voice input, and JSON files for multi-language support. All data stored in-memory with no persistence between sessions.

## Technical Context

**Language/Version**: Python 3.10 or newer (required by constitution)
**Primary Dependencies**:
  - `rich` (CLI UI rendering - tables, colors, styling)
  - `dateparser` (natural language date/time parsing)
  - `SpeechRecognition` (voice-to-text conversion)
  - `PyAudio` (microphone input for voice features)
  - `pytest` (unit testing framework)
  - `requests` (quote of the day API calls)

**Storage**: In-memory only (no databases, files, or persistence - constitutional requirement)
**Testing**: pytest with minimum 80% coverage for Sub-Agent skills
**Target Platform**: Cross-platform CLI (Windows, Linux, macOS) with ANSI color and Unicode support
**Project Type**: Single Python application with modular Sub-Agent architecture
**Performance Goals**:
  - CLI response time <500ms for typical operations (constitutional requirement)
  - NLP parsing <200ms per input (constitutional requirement)
  - Support 10,000+ tasks without degradation (constitutional requirement)
  - Startup screen display <2 seconds (from spec SC-005)
  - Search/filter/sort <1 second for 1000 tasks (from spec SC-007)

**Constraints**:
  - No external databases or file-based persistence
  - Must use `rich` exclusively for UI (no other libraries)
  - All Sub-Agents must reside in separate files
  - All skills must be independently testable
  - Terminal must support ANSI colors and Unicode
  - Voice input requires microphone hardware

**Scale/Scope**:
  - 12 prioritized user stories (P1-P12)
  - 64 functional requirements
  - 8 Sub-Agent domains (Task Management, UI, NLP, Voice, Language, Gamification, Focus, Analytics)
  - 3 required languages (English, Urdu, Spanish)
  - Single-user application (no multi-user support)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Language & Environment ✅ PASS

- **Requirement**: Python 3.10 or newer exclusively
- **Plan Compliance**: Specification and plan both mandate Python 3.10+
- **Dependency Management**: `requirements.txt` will be created with all external packages

### Architecture & Design ✅ PASS

- **Requirement**: Strict OOP with Sub-Agent/Skill architecture
- **Plan Compliance**: Application designed with 8 Sub-Agents, each in dedicated file:
  - `TaskManager` (task_manager.py) - Task CRUD, search, filter, sort, recurring tasks
  - `UIAgent` (ui_agent.py) - Rich-based rendering, menus, tables, startup screen
  - `NLPAgent` (nlp_agent.py) - Natural language parsing for dates and priorities
  - `VoiceAgent` (voice_agent.py) - Speech-to-text conversion
  - `LanguageAgent` (language_agent.py) - Multi-language JSON loading and translation
  - `GamificationAgent` (gamification_agent.py) - Streaks, XP, badges
  - `FocusAgent` (focus_agent.py) - Pomodoro timer
  - `AnalyticsAgent` (analytics_agent.py) - Metrics calculation, charts

- **Requirement**: Each Sub-Agent's functionality broken into Skills (focused, reusable, testable methods)
- **Plan Compliance**: Each agent will expose skill methods (e.g., `add_task_skill()`, `parse_natural_language_skill()`, `award_xp_skill()`)

- **Requirement**: Fully in-memory, no persistence
- **Plan Compliance**: All task data stored in Python data structures (lists/dicts), reset on application exit

### Technology Stack ✅ PASS

- **Requirement**: CLI with `rich` library exclusively
- **Plan Compliance**: All UI rendering (tables, colors, icons, styling) uses `rich.table.Table`, `rich.console.Console`, `rich.panel.Panel`

- **Requirement**: `dateparser` for NLP date parsing
- **Plan Compliance**: Natural language date extraction uses `dateparser.parse()`

- **Requirement**: JSON files for i18n
- **Plan Compliance**: Language strings stored in `locales/en.json`, `locales/ur.json`, `locales/es.json`

- **Requirement**: `SpeechRecognition` with `PyAudio` for voice input
- **Plan Compliance**: Voice transcription uses `speech_recognition.Recognizer()` with PyAudio microphone input

### Quality & Reliability ✅ PASS

- **Requirement**: PEP 257 docstrings for all modules, classes, public methods
- **Plan Compliance**: All Sub-Agents and Skills will include comprehensive docstrings

- **Requirement**: pytest with ≥80% coverage for core logic
- **Plan Compliance**: Unit tests for all Skills in `tests/unit/`, integration tests in `tests/integration/`

- **Requirement**: Graceful error handling with user-friendly messages
- **Plan Compliance**: Try-except blocks for all user input, invalid operations, API failures (quote service, voice recognition)

### Performance Standards ✅ PASS

- **Requirement**: CLI commands respond within 500ms
- **Plan Compliance**: In-memory operations ensure sub-millisecond data access; only potential delays are NLP parsing (<200ms target) and voice recognition (handled asynchronously)

- **Requirement**: Support 10,000 tasks without degradation
- **Plan Compliance**: Python lists/dicts handle this scale efficiently; search/filter use list comprehensions (O(n) acceptable for 10k items)

- **Requirement**: NLP parsing <200ms per input
- **Plan Compliance**: `dateparser` is optimized for speed; keyword matching for priority uses simple string operations

**Constitution Compliance**: ✅ ALL GATES PASS - No violations, proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-cli-todo-app/
├── spec.md              # Feature specification (created by /sp.specify)
├── plan.md              # This file (created by /sp.plan)
├── research.md          # Phase 0: Technology research and decisions
├── data-model.md        # Phase 1: Entity definitions and relationships
├── quickstart.md        # Phase 1: Developer setup and usage guide
├── contracts/           # Phase 1: Internal agent contracts (if needed)
│   └── agent_interfaces.md
├── checklists/          # Quality validation checklists
│   └── requirements.md  # Specification quality checklist (already created)
└── tasks.md             # Phase 2: Implementation tasks (created by /sp.tasks - NOT by /sp.plan)
```

### Source Code (repository root)

```text
todo_app/
├── main.py                    # Application entry point, main menu loop
├── models/
│   ├── __init__.py
│   ├── task.py                # Task data class
│   ├── user_profile.py        # Gamification/analytics data class
│   └── config.py              # Configuration data class
├── agents/
│   ├── __init__.py
│   ├── task_manager.py        # TaskManager Sub-Agent
│   ├── ui_agent.py            # UIAgent Sub-Agent
│   ├── nlp_agent.py           # NLPAgent Sub-Agent
│   ├── voice_agent.py         # VoiceAgent Sub-Agent
│   ├── language_agent.py      # LanguageAgent Sub-Agent
│   ├── gamification_agent.py  # GamificationAgent Sub-Agent
│   ├── focus_agent.py         # FocusAgent Sub-Agent
│   └── analytics_agent.py     # AnalyticsAgent Sub-Agent
├── locales/
│   ├── en.json                # English translations
│   ├── ur.json                # Urdu translations
│   └── es.json                # Spanish translations
├── utils/
│   ├── __init__.py
│   ├── validators.py          # Input validation helpers
│   └── quotes.py              # Quote of the day functionality
└── config.json                # Runtime configuration (default language, theme)

tests/
├── unit/
│   ├── test_task_manager.py
│   ├── test_nlp_agent.py
│   ├── test_gamification_agent.py
│   ├── test_analytics_agent.py
│   └── test_validators.py
├── integration/
│   ├── test_task_workflows.py
│   ├── test_voice_to_task.py
│   └── test_multi_language.py
└── fixtures/
    ├── sample_tasks.py
    └── test_data.py

docs/
├── README.md                  # Setup and usage instructions
└── future_improvements.md     # Potential enhancements

requirements.txt               # Python dependencies
.gitignore                     # Git exclusions
pytest.ini                     # Pytest configuration
```

**Structure Decision**: Single Python application structure selected because this is a self-contained CLI tool (not web/mobile). The `agents/` directory houses all Sub-Agents following the constitutional requirement for separate files. The `models/` directory contains data classes (Task, UserProfile, Config). The `locales/` directory manages i18n JSON files. The `tests/` directory mirrors the source structure for unit and integration tests.

## Complexity Tracking

**No constitutional violations detected** - Complexity tracking table not required.

All design decisions align with constitution:
- Single Python project (within scope)
- Sub-Agent/Skill architecture followed
- In-memory storage only
- Approved libraries only (`rich`, `dateparser`, `SpeechRecognition`, `PyAudio`, `pytest`)
- No unnecessary abstractions or patterns introduced

## Phase 0: Research & Decisions

**Objective**: Resolve all technical unknowns and establish best practices for each technology choice.

### Research Tasks

1. **Natural Language Processing for Task Parsing**
   - **Question**: How to extract task title, due date, and priority from free-text input?
   - **Research Focus**:
     - `dateparser` library capabilities and configuration
     - Keyword-based priority detection strategies
     - Separating task title from date/priority indicators
   - **Output**: NLP parsing strategy documented in `research.md`

2. **Voice Input Implementation**
   - **Question**: Which speech recognition backend to use and how to handle errors?
   - **Research Focus**:
     - `SpeechRecognition` library supported backends (Google, Sphinx, Wit.ai)
     - Offline vs. online recognition trade-offs
     - Error handling for poor audio quality, network failures
     - Microphone access and PyAudio setup
   - **Output**: Voice input architecture documented in `research.md`

3. **Multi-Language Support Architecture**
   - **Question**: How to structure JSON files and implement fallback logic?
   - **Research Focus**:
     - JSON schema for translation files
     - Dynamic string lookup mechanism
     - Fallback to English when translations missing
     - Urdu script rendering in terminal (RTL considerations)
   - **Output**: i18n implementation strategy documented in `research.md`

4. **Pomodoro Timer in CLI**
   - **Question**: How to display live countdown timer without blocking main thread?
   - **Research Focus**:
     - `rich.live.Live` for dynamic updates
     - Threading vs. async approaches
     - User interrupt handling (cancel timer)
   - **Output**: Focus mode timer design documented in `research.md`

5. **CLI Charts with Rich**
   - **Question**: How to generate text-based bar charts?
   - **Research Focus**:
     - `rich.bar.Bar` or custom ASCII art generation
     - Scaling bars to terminal width
     - Data normalization for visualization
   - **Output**: Chart generation approach documented in `research.md`

6. **Quote of the Day API**
   - **Question**: Which free API to use and how to handle unavailability?
   - **Research Focus**:
     - Free quote APIs (ZenQuotes, Quotable, They Said So)
     - Rate limits and reliability
     - Fallback to embedded quote list
     - Timeout handling
   - **Output**: Quote fetching strategy documented in `research.md`

7. **In-Memory Data Structure Optimization**
   - **Question**: Best Python data structures for 10,000+ tasks with fast search/filter/sort?
   - **Research Focus**:
     - List vs. dict vs. custom index structures
     - Trade-offs for search (O(n) acceptable at this scale)
     - Sorting performance with Python's `sorted()`
     - Memory footprint estimation
   - **Output**: Data structure decisions documented in `research.md`

8. **Testing Strategy for CLI Application**
   - **Question**: How to test CLI interactions and Rich output?
   - **Research Focus**:
     - Mocking user input in pytest
     - Capturing Rich console output for assertions
     - Integration test patterns for menu flows
     - Voice/API mocking strategies
   - **Output**: Testing approach documented in `research.md`

### Research Deliverable

**File**: `specs/001-cli-todo-app/research.md`

**Structure**:
```markdown
# Research: In-Memory Python CLI Todo Application

## 1. Natural Language Processing
- **Decision**: [chosen approach]
- **Rationale**: [why chosen]
- **Alternatives Considered**: [what else evaluated]
- **Implementation Notes**: [key details]

## 2. Voice Input
[same structure]

## 3. Multi-Language Support
[same structure]

... [for each research task]

## Summary of Key Decisions
[consolidated decision log]
```

## Phase 1: Design & Contracts

**Prerequisites**: `research.md` complete, all technical unknowns resolved

### 1. Data Model Design

**Objective**: Define all entities with fields, validations, and relationships.

**File**: `specs/001-cli-todo-app/data-model.md`

**Entities** (extracted from spec.md Key Entities section):

#### Task
- **Purpose**: Represents a single todo item
- **Fields**:
  - `id`: int (unique, auto-incremented) or UUID
  - `title`: str (required, max 200 chars)
  - `description`: str (optional, max 1000 chars)
  - `status`: Enum("Pending", "Completed")
  - `priority`: Enum("High", "Medium", "Low")
  - `tags`: list[str] (optional)
  - `due_date`: datetime (optional, timezone-aware)
  - `created_at`: datetime (auto-generated on creation)
  - `completed_at`: datetime (optional, set when status changes to Completed)
  - `recurrence`: Enum("None", "Daily", "Weekly", "Monthly") (optional)
- **Validations**:
  - Title cannot be empty
  - Due date must be in the future (warning, not error)
  - Completed_at only set when status is Completed
- **Relationships**: None (standalone entity)

#### UserProfile
- **Purpose**: Stores gamification and analytics data for the session
- **Fields**:
  - `total_xp`: int (default 0)
  - `daily_streak`: int (default 0)
  - `last_completion_date`: date (optional)
  - `earned_badges`: list[str] (default empty)
  - `completion_history`: list[dict] with {task_id, completed_at, xp_earned}
- **Validations**:
  - XP cannot be negative
  - Streak resets if last_completion_date is more than 1 day old
- **Relationships**: References Task IDs in completion_history

#### Configuration
- **Purpose**: Runtime settings for the application
- **Fields**:
  - `language`: str (default "en", choices: ["en", "ur", "es"])
  - `color_theme`: str (default "default")
  - `default_priority`: Enum("High", "Medium", "Low") (default "Medium")
- **Validations**:
  - Language must be supported (en/ur/es)
- **Relationships**: None

**State Transitions**:
- Task status: Pending → Completed (via mark_complete action)
- Task status: Completed → Pending (via mark_incomplete action)
- Recurring tasks: Completed → create new Pending instance with future due_date

### 2. Agent Contracts (Internal Interfaces)

**Objective**: Define the interface (skill methods) each Sub-Agent must expose.

**File**: `specs/001-cli-todo-app/contracts/agent_interfaces.md`

**Structure**: For each Sub-Agent, list public skill methods with signatures.

Example:
```markdown
## TaskManager Sub-Agent

### add_task_skill(title, description, priority, tags, due_date, recurrence) -> Task
Create new task and return Task object.

### delete_task_skill(task_id) -> bool
Delete task by ID, return True if successful.

### update_task_skill(task_id, **kwargs) -> Task
Update task fields, return updated Task object.

### mark_complete_skill(task_id) -> Task
Toggle task status to Completed, set completed_at, return Task.

### search_tasks_skill(keyword) -> list[Task]
Return tasks matching keyword in title or description.

### filter_tasks_skill(status, priority, tag) -> list[Task]
Return tasks matching filter criteria.

### sort_tasks_skill(tasks, sort_by, order) -> list[Task]
Return sorted task list.

... [for all 8 Sub-Agents]
```

### 3. Developer Quickstart Guide

**Objective**: Document setup, running, and basic development workflow.

**File**: `specs/001-cli-todo-app/quickstart.md`

**Content**:
```markdown
# Quickstart: In-Memory Python CLI Todo Application

## Prerequisites
- Python 3.10 or newer
- pip package manager
- Microphone (for voice input feature)
- Terminal with ANSI color and Unicode support

## Setup

1. Clone the repository:
   ```bash
   git clone <repo-url>
   cd todo-hackathon
   git checkout 001-cli-todo-app
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

```bash
python todo_app/main.py
```

## Running Tests

```bash
pytest tests/ -v --cov=todo_app --cov-report=html
```

## Development Workflow

1. Create new feature branch from 001-cli-todo-app
2. Implement Sub-Agent skills in `todo_app/agents/`
3. Add unit tests in `tests/unit/`
4. Run tests and ensure ≥80% coverage
5. Commit with descriptive message
6. Create pull request

## Project Structure Overview

- `todo_app/main.py`: Entry point
- `todo_app/agents/`: Sub-Agent implementations
- `todo_app/models/`: Data classes
- `todo_app/locales/`: Translation JSON files
- `tests/`: Test suite

## Key Commands

- Run app: `python todo_app/main.py`
- Run tests: `pytest tests/ -v`
- Check coverage: `pytest tests/ --cov=todo_app --cov-report=term`
- Format code: `black todo_app/ tests/`
- Lint: `pylint todo_app/`

## Troubleshooting

**Voice input not working**: Install PyAudio dependencies (see platform-specific guides)
**Urdu text not rendering**: Ensure terminal supports Unicode and has Urdu fonts
**Tests failing**: Check Python version (must be ≥3.10)
```

### 4. Update Agent Context

**Objective**: Update AI agent context with technology decisions from this plan.

**Action**: Run `.specify/scripts/powershell/update-agent-context.ps1 -AgentType claude` after Phase 1 completes.

**Expected Updates**: Add references to `rich`, `dateparser`, `SpeechRecognition`, Sub-Agent architecture patterns to agent context file.

## Phase 2: Task Generation (Out of Scope)

Phase 2 (generating `tasks.md`) is handled by the `/sp.tasks` command, NOT by `/sp.plan`.

The `/sp.tasks` command will:
1. Read this plan.md and spec.md
2. Break down each user story into concrete implementation tasks
3. Create dependency-ordered tasks in tasks.md
4. Include acceptance criteria and test requirements for each task

## Post-Phase 1 Constitution Re-Check

*Re-evaluate constitution compliance after design artifacts are complete.*

### Architecture & Design ✅ PASS (Re-validated)

**Sub-Agent/Skill Architecture Confirmed**:
- 8 Sub-Agents defined with clear domain boundaries
- Each Sub-Agent in separate file (agents/ directory)
- Skill methods defined in agent_interfaces.md with focused responsibilities
- No cross-agent dependencies requiring complex abstractions

**In-Memory Storage Confirmed**:
- Task, UserProfile, Configuration data classes use Python native types
- No database connections or file I/O for application data
- Session-scoped data structures (reset on exit)

### Technology Stack ✅ PASS (Re-validated)

**Approved Libraries Confirmed**:
- `rich` for all UI rendering (no alternatives used)
- `dateparser` for NLP date extraction
- `SpeechRecognition` + `PyAudio` for voice input
- `pytest` for testing
- `requests` for quote API (HTTP library, acceptable)

**JSON-based i18n Confirmed**:
- Translation files in locales/en.json, locales/ur.json, locales/es.json
- LanguageAgent handles loading and fallback logic

### Quality & Reliability ✅ PASS (Re-validated)

**Testing Strategy Confirmed**:
- Unit tests for all Sub-Agent skills
- Integration tests for workflows (task creation → gamification updates)
- Mocking for voice input and API calls
- Coverage target ≥80%

**Error Handling Confirmed**:
- User input validation in validators.py
- Try-except blocks in all agent skills
- Graceful degradation for optional features (voice, quote API)
- Clear error messages displayed via UIAgent

**Final Constitution Compliance**: ✅ ALL GATES PASS - Design adheres to all constitutional requirements

## Implementation Phases (High-Level)

*These phases are informational only; actual task breakdown happens in /sp.tasks.*

### Phase 1: Core Foundation (P1 User Story)
- Setup project structure
- Implement Task data model
- Implement TaskManager Sub-Agent (CRUD skills)
- Implement UIAgent (basic menu, task table rendering)
- Implement main.py menu loop
- Unit tests for TaskManager skills

### Phase 2: Organization Features (P2 User Story)
- Implement search_tasks_skill
- Implement filter_tasks_skill
- Implement sort_tasks_skill
- Enhance UIAgent for search/filter/sort UX
- Unit tests for organization skills

### Phase 3: Natural Language Input (P3 User Story)
- Implement NLPAgent (date parsing, priority detection)
- Integrate NLPAgent with TaskManager
- Update UIAgent for NLP input mode
- Unit tests for NLP parsing

### Phase 4: Voice Input (P4 User Story)
- Implement VoiceAgent (speech-to-text)
- Integrate VoiceAgent with NLPAgent pipeline
- Error handling for voice recognition failures
- Unit tests with mocked audio input

### Phase 5: Multi-Language Support (P5 User Story)
- Create en.json, ur.json, es.json translation files
- Implement LanguageAgent (load/translate skills)
- Refactor UIAgent to use LanguageAgent for all text
- Integration tests for language switching

### Phase 6: Advanced Features (P6-P9 User Stories)
- Implement mood-based suggestion (TaskManager skill)
- Implement recurring tasks (TaskManager skill)
- Implement GamificationAgent (XP, streaks, badges)
- Implement FocusAgent (Pomodoro timer with rich.live)
- Unit tests for all new skills

### Phase 7: Analytics & Visualization (P10-P11 User Stories)
- Implement AnalyticsAgent (metrics calculation)
- Implement chart generation skill
- Update UIAgent to display analytics dashboard
- Unit tests for analytics calculations

### Phase 8: Polish & Documentation (P12 User Story)
- Implement startup screen with ASCII art
- Integrate quote API (utils/quotes.py)
- Comprehensive error handling review
- Create README.md and future_improvements.md
- End-to-end integration tests

## Key Architectural Decisions

### 1. Sub-Agent Separation Strategy

**Decision**: Each Sub-Agent is a stateless service class, instantiated once in main.py and passed to UI/menu handlers.

**Rationale**:
- Stateless agents are easier to test (no side effects between calls)
- Single instance per agent reduces memory overhead
- Clear dependency injection pattern (agents passed explicitly)

**Alternative Rejected**: Singleton pattern (adds unnecessary complexity, harder to test)

### 2. Task Storage Structure

**Decision**: Store tasks in a Python list, with ID-based lookup using list comprehension or dict mapping.

**Rationale**:
- List comprehensions are fast enough for 10,000 items (millisecond range)
- Simple to implement, no external dependencies
- Supports all required operations (search, filter, sort)

**Alternative Rejected**: In-memory SQLite database (violates constitutional in-memory simplicity requirement)

### 3. Voice Recognition Backend

**Decision**: Use Google Speech Recognition API (via SpeechRecognition library) with offline CMU Sphinx as fallback.

**Rationale**:
- Google API has best accuracy for free tier
- Graceful degradation to Sphinx when offline
- SpeechRecognition library abstracts backend switching

**Alternative Rejected**: Wit.ai (requires API key, less documentation)

### 4. NLP Priority Detection

**Decision**: Keyword-based matching using predefined lists (e.g., ["urgent", "asap", "important"] → High priority).

**Rationale**:
- Simple, fast, deterministic
- No need for ML models or training
- Easy to extend keyword lists

**Alternative Rejected**: NLTK sentiment analysis (overkill, slower, less accurate for this use case)

### 5. Pomodoro Timer Implementation

**Decision**: Use `rich.live.Live` context manager with threading for countdown updates.

**Rationale**:
- rich.live provides flicker-free dynamic updates
- Threading allows user to cancel timer with keyboard interrupt
- No blocking of main event loop

**Alternative Rejected**: Async/await (adds complexity, rich.live already handles updates)

### 6. Quote of the Day API

**Decision**: Use ZenQuotes API (https://zenquotes.io) with 5-second timeout and embedded fallback quotes.

**Rationale**:
- ZenQuotes is free, no API key required
- Simple JSON response format
- Embedded fallbacks ensure startup never fails

**Alternative Rejected**: Quotable API (rate limits more restrictive)

### 7. Multi-Language File Structure

**Decision**: JSON files with flat key-value structure (e.g., `{"menu.add_task": "Add Task"}`).

**Rationale**:
- Simple to parse with json.load()
- Keys use dot notation for namespacing (menu., error., etc.)
- Easy for translators to edit without code knowledge

**Alternative Rejected**: Nested JSON objects (harder to lookup, more complex traversal)

### 8. Testing Approach

**Decision**:
- Unit tests mock all external dependencies (voice, API, time)
- Integration tests use in-memory fixtures, no external calls
- Rich output tested by capturing console output to StringIO

**Rationale**:
- Fast, deterministic tests (no network/hardware dependencies)
- pytest-mock makes mocking straightforward
- Console capture validates UI without manual inspection

**Alternative Rejected**: End-to-end tests with real voice/API (too slow, non-deterministic)

## Risk Assessment

### High Risk

1. **Voice Recognition Accuracy**
   - **Risk**: Poor audio quality or accents may result in incorrect transcriptions
   - **Mitigation**: Show transcribed text to user for confirmation before creating task
   - **Contingency**: Users can disable voice input and use text-only mode

2. **Urdu Script Rendering**
   - **Risk**: Not all terminals support RTL (right-to-left) rendering correctly
   - **Mitigation**: Document terminal requirements (Windows Terminal, iTerm2, etc.)
   - **Contingency**: Warn users if terminal doesn't support Unicode; default to English

### Medium Risk

3. **Quote API Reliability**
   - **Risk**: External API may be down or rate-limited
   - **Mitigation**: 5-second timeout, embedded fallback quotes
   - **Impact**: Startup screen shows fallback quote (minimal UX degradation)

4. **Performance with 10,000+ Tasks**
   - **Risk**: List operations may slow down with very large datasets
   - **Mitigation**: Use Python's built-in optimizations (sorted(), filter())
   - **Impact**: Search/filter may take 1-2 seconds (acceptable per spec SC-007)

### Low Risk

5. **PyAudio Installation Issues**
   - **Risk**: PyAudio has platform-specific dependencies (PortAudio)
   - **Mitigation**: Document platform-specific installation steps in README
   - **Impact**: Users without microphone skip voice input feature (optional)

6. **Date Parsing Ambiguity**
   - **Risk**: "next Friday" may be ambiguous if current day is Friday
   - **Mitigation**: dateparser has built-in disambiguation logic
   - **Impact**: Rare edge cases; users can manually edit due date if incorrect

## Success Metrics (How to Validate)

**From Specification Success Criteria**:

1. **SC-001**: Users create basic task in <10 seconds
   - **Validation**: Manual timing test with sample users
   - **Target**: 5 keystrokes average (menu select → title → priority → enter)

2. **SC-005**: Startup <2 seconds
   - **Validation**: `time python todo_app/main.py` (measure cold start)
   - **Target**: ≤2s on standard laptop

3. **SC-007**: Search/filter <1 second for 1000 tasks
   - **Validation**: Performance test with 1000 fixture tasks
   - **Target**: Use pytest-benchmark to measure search_tasks_skill()

4. **SC-009**: NLP date extraction 90% accuracy
   - **Validation**: Test suite with 100 diverse date phrases
   - **Target**: ≥90 correctly parsed

5. **SC-013**: Streak tracking 100% accuracy
   - **Validation**: Unit tests for edge cases (midnight rollover, skipped days)
   - **Target**: All tests pass

## Next Steps

1. ✅ **Complete Phase 0**: Generate `research.md` with all technical decisions
2. ✅ **Complete Phase 1**: Generate `data-model.md`, `contracts/agent_interfaces.md`, `quickstart.md`
3. **Run `/sp.tasks`**: Generate dependency-ordered task list in `tasks.md`
4. **Begin Implementation**: Start with Phase 1 tasks (Core Foundation - P1 User Story)

---

**Plan Status**: ✅ Complete
**Constitution Compliance**: ✅ Validated
**Ready for Task Generation**: ✅ Yes (run `/sp.tasks`)
