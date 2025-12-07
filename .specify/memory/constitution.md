<!--
Sync Impact Report:
Version Change: [CONSTITUTION_VERSION] → 1.0.0
Modified Principles: Initial constitution creation
Added Sections:
  - Core Language & Environment
  - Architecture & Design
  - Key Technology Stack
  - Quality & Reliability
Removed Sections: None (initial creation)
Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section already generic
  ✅ spec-template.md - No constitution-specific references
  ✅ tasks-template.md - No constitution-specific references
Follow-up TODOs: None
-->

# In-Memory Python CLI Todo Application Constitution

## Core Principles

### I. Core Language & Environment

The project MUST be written exclusively in **Python 3.10 or newer**. All external packages MUST be listed in a `requirements.txt` file for reproducible dependency management.

**Rationale**: Python 3.10+ provides modern type hinting, pattern matching, and performance improvements essential for clean, maintainable code. Explicit dependency tracking ensures consistent environments across development, testing, and deployment.

### II. Architecture & Design

The codebase MUST follow strict **Object-Oriented Programming (OOP)** principles using classes for all major components.

The application MUST be architected as a system of **Sub-Agents**:
- A **Sub-Agent** is a high-level class responsible for a complete functional domain (e.g., `TaskManager`, `AnalyticsAgent`, `UIAgent`)
- Each Sub-Agent MUST reside in its own dedicated file
- Each Sub-Agent's functionality MUST be broken down into discrete methods called **Skills**
- A **Skill** MUST be a focused, reusable, and independently testable unit of logic (e.g., `add_task_skill()`, `generate_chart_skill()`)

The application MUST be **fully in-memory**. No databases, files, or external storage for application data are permitted. All data state MUST be volatile and reset when the application closes.

**Rationale**: The Sub-Agent/Skill architecture promotes modularity, testability, and clear separation of concerns. Each agent owns a domain, and skills provide granular, reusable operations. In-memory storage ensures simplicity, fast iteration, and eliminates persistence complexity for this use case.

### III. Key Technology Stack

**User Interface**: The Command Line Interface (CLI) MUST be the sole interface. All visual output (tables, colors, styles, icons) MUST be rendered using the **`rich`** library. No other UI library is permitted.

**Natural Language Processing**: For parsing dates from user text, the **`dateparser`** library MUST be used. Other NLP logic (like priority detection) MUST be implemented using `nltk` or `spaCy` in conjunction with a compatible microphone engine like `PyAudio`.

**Internationalization (i18n)**: Multi-language support MUST be implemented by loading UI strings and commands from structured **JSON files** (e.g., `en.json`, `ur.json`).

**Rationale**: The `rich` library provides professional-grade terminal UI capabilities. `dateparser` offers robust, locale-aware date parsing. JSON-based i18n allows for easy translation management without code changes. These choices balance capability, maintainability, and performance.

### IV. Quality & Reliability

**Code Quality**: All code MUST be well-documented with PEP 257 compliant docstrings for all modules, classes, and public methods. The code MUST be clean, readable, and maintainable.

**Testing**: A comprehensive suite of unit tests MUST be written using the **`pytest`** framework. Core logic within the task manager, analytics, and gamification modules MUST be tested to ensure correctness.

**Error Handling**: The application MUST gracefully handle invalid user inputs and potential runtime errors, providing clear, user-friendly feedback instead of crashing.

**Rationale**: Quality is non-negotiable. PEP 257 docstrings ensure code is self-documenting. Pytest provides a powerful, Pythonic testing framework. Graceful error handling creates a professional user experience and prevents data loss.

## Development Workflow

### Code Review Requirements

All code changes MUST be reviewed for:
- Compliance with the Sub-Agent/Skill architecture
- Presence of PEP 257 docstrings
- Pytest coverage for new logic
- Use of approved libraries only (`rich`, `dateparser`, `nltk`/`spaCy`, `PyAudio`)
- In-memory data handling (no persistence violations)

### Testing Gates

Before merging any feature:
- All existing tests MUST pass
- New functionality MUST have corresponding pytest tests
- Test coverage for Sub-Agent skills MUST be ≥80%
- Manual CLI testing MUST verify `rich` rendering correctness

## Deployment & Operations

### Runtime Requirements

- Python 3.10+ runtime environment
- All dependencies from `requirements.txt` installed
- No external storage or database dependencies
- Terminal supporting ANSI colors and Unicode (for `rich` rendering)

### Performance Standards

- CLI commands MUST respond within 500ms for typical operations
- In-memory data structures MUST support at least 10,000 todo items without degradation
- NLP parsing (dates, priorities) MUST complete within 200ms per user input

## Governance

This constitution supersedes all other practices and preferences. Amendments require:
1. Documentation of the proposed change and rationale
2. Review of impact on existing Sub-Agents and Skills
3. Approval from project maintainer(s)
4. Migration plan if existing code violates new principles

All code reviews MUST verify compliance with this constitution. Complexity that violates these principles MUST be justified with clear reasoning or rejected.

For runtime development guidance, agents should consult the `CLAUDE.md` file.

**Version**: 1.0.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05
