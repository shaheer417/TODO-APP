# Tasks: In-Memory Python CLI Todo Application

**Input**: Design documents from `/specs/001-cli-todo-app/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/agent_interfaces.md, research.md

**Tests**: Tests are NOT requested in the specification. This is a direct implementation project focusing on building working features. Test tasks are excluded.

**Organization**: Tasks are grouped by user story (P1-P12) to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

All paths use `todo_app/` as the root directory (single Python application):
- Models: `todo_app/models/`
- Agents: `todo_app/agents/`
- Locales: `todo_app/locales/`
- Utils: `todo_app/utils/`
- Main: `todo_app/main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure (todo_app/, tests/, docs/, locales/)
- [x] T002 Create requirements.txt with dependencies (rich, dateparser, SpeechRecognition, PyAudio, pytest, requests)
- [x] T003 [P] Create .gitignore for Python project (venv/, __pycache__/, *.pyc, .pytest_cache/, htmlcov/)
- [x] T004 [P] Create pytest.ini with coverage configuration
- [x] T005 [P] Create all __init__.py files (todo_app/, todo_app/models/, todo_app/agents/, todo_app/utils/)
- [x] T006 [P] Create config.json template with default values (language: "en", color_theme: "default", default_priority: "Medium")

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data models and infrastructure that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T007 Create Task model in todo_app/models/task.py with all fields (id, title, description, status, priority, tags, due_date, created_at, completed_at, recurrence) and enums (Status, Priority, Recurrence)
- [x] T008 [P] Create UserProfile model in todo_app/models/user_profile.py with fields (total_xp, daily_streak, last_completion_date, earned_badges, completion_history)
- [ ] T009 [P] Create Configuration model in todo_app/models/config.py with fields (language, color_theme, default_priority)
- [x] T010 Add validation logic to Task model (title max 200 chars, description max 1000 chars, non-empty title check)
- [ ] T011 [P] Create input validators in todo_app/utils/validators.py for date formats, priority values, and general input sanitization

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, update, delete, and complete tasks with a menu-driven CLI interface

**Independent Test**: Launch app, add tasks with different priorities/dates, view in formatted table, mark complete, update fields, delete tasks. Verify all CRUD operations work.

### Implementation for User Story 1

- [x] T012 [P] [US1] Create TaskManager Sub-Agent skeleton in todo_app/agents/task_manager.py with __init__ method and empty task list/index
- [x] T013 [P] [US1] Create UIAgent Sub-Agent skeleton in todo_app/agents/ui_agent.py with Rich Console instance
- [x] T014 [US1] Implement add_task_skill in TaskManager (create task with auto-increment ID, add to list and index)
- [x] T015 [US1] Implement get_task_skill in TaskManager (O(1) lookup from index)
- [x] T016 [US1] Implement update_task_skill in TaskManager (update fields, preserve others, validate)
- [x] T017 [US1] Implement delete_task_skill in TaskManager (remove from list and index)
- [x] T018 [US1] Implement mark_complete_skill in TaskManager (toggle status, set completed_at timestamp)
- [x] T019 [US1] Implement mark_incomplete_skill in TaskManager (revert to Pending, clear completed_at)
- [x] T020 [US1] Implement view_all_tasks_skill in TaskManager (return all tasks in insertion order)
- [x] T021 [US1] Implement display_task_table_skill in UIAgent using rich.table.Table with columns (ID, Title, Priority, Status, Due Date, Tags), color coding, and icons
- [x] T022 [US1] Implement display_main_menu_skill in UIAgent with options (Add Task, View Tasks, Update Task, Delete Task, Mark Complete, Exit)
- [x] T023 [US1] Implement prompt_text_input_skill in UIAgent for getting user text input
- [x] T024 [US1] Implement prompt_choice_skill in UIAgent for multiple-choice menus
- [x] T025 [US1] Implement display_success_message_skill in UIAgent (green text with checkmark)
- [x] T026 [US1] Implement display_error_message_skill in UIAgent (red text with X icon)
- [x] T027 [US1] Create main.py with basic menu loop structure, instantiate TaskManager and UIAgent
- [x] T028 [US1] Implement "Add Task" menu handler in main.py (prompt for title, description, priority, tags, due date, call add_task_skill)
- [x] T029 [US1] Implement "View All Tasks" menu handler in main.py (call view_all_tasks_skill, display_task_table_skill)
- [x] T030 [US1] Implement "Update Task" menu handler in main.py (prompt for ID and fields, call update_task_skill)
- [x] T031 [US1] Implement "Delete Task" menu handler in main.py (prompt for ID, call delete_task_skill)
- [x] T032 [US1] Implement "Mark Complete" menu handler in main.py (prompt for ID, call mark_complete_skill)
- [x] T033 [US1] Add error handling for invalid task IDs (display "Task ID not found" message)
- [x] T034 [US1] Add error handling for invalid date formats (display format error with example)
- [x] T035 [US1] Wire all menu options to handlers and test full CRUD workflow

**Checkpoint**: US1 complete - functional todo list with all basic operations working

---

## Phase 4: User Story 2 - Search, Filter, and Sort (Priority: P2)

**Goal**: Enable users to find, filter, and organize large task lists efficiently

**Independent Test**: Create 20+ tasks with diverse properties, search by keyword, filter by status/priority/tag, sort by various criteria. Verify accuracy and performance.

### Implementation for User Story 2

- [x] T036 [US2] Implement search_tasks_skill in TaskManager (case-insensitive keyword search in title and description)
- [x] T037 [US2] Implement filter_tasks_skill in TaskManager with parameters (status, priority, tag), return filtered list
- [x] T038 [US2] Implement sort_tasks_skill in TaskManager with parameters (sort_by: due_date/priority/title/created_at, reverse: bool)
- [x] T039 [US2] Implement get_overdue_tasks_skill in TaskManager (find pending tasks past due date)
- [x] T040 [US2] Add "Search Tasks" option to main menu in main.py
- [x] T041 [US2] Implement "Search Tasks" menu handler (prompt for keyword, call search_tasks_skill, display results)
- [x] T042 [US2] Add "Filter Tasks" option to main menu in main.py
- [x] T043 [US2] Implement "Filter Tasks" menu handler (prompt for status/priority/tag, call filter_tasks_skill, display results)
- [ ] T044 [US2] Add "Sort Tasks" option to main menu in main.py
- [ ] T045 [US2] Implement "Sort Tasks" menu handler (prompt for sort field and order, call sort_tasks_skill, display results)
- [ ] T046 [US2] Add "View Overdue Tasks" option to main menu in main.py
- [ ] T047 [US2] Implement "View Overdue Tasks" menu handler (call get_overdue_tasks_skill, highlight in bright red)
- [x] T048 [US2] Handle edge case: no tasks match search/filter criteria (display "No tasks found" message)

**Checkpoint**: US2 complete - users can efficiently organize and find tasks in large lists

---

## Phase 5: User Story 3 - Natural Language Task Input (Priority: P3)

**Goal**: Allow users to create tasks using natural language instead of filling multiple form fields

**Independent Test**: Type phrases like "Urgent report by tomorrow 5pm", "Buy groceries this weekend", verify correct extraction of title, date, priority.

### Implementation for User Story 3

- [x] T049 [P] [US3] Create NLPAgent Sub-Agent skeleton in todo_app/agents/nlp_agent.py
- [x] T050 [US3] Implement parse_natural_language_skill in NLPAgent (extract title, due_date using dateparser, priority from keywords)
- [x] T051 [US3] Add priority keyword dictionaries to NLPAgent (HIGH: ["urgent", "asap", "critical"], MEDIUM: ["soon"], LOW: ["someday", "maybe"])
- [x] T052 [US3] Implement title extraction logic in NLPAgent (remove date phrases and priority keywords from input)
- [x] T053 [US3] Handle edge case: no date found in NLPAgent (return None for due_date, notify user)
- [ ] T054 [US3] Add "Add Task (Natural Language)" option to main menu in main.py
- [ ] T055 [US3] Implement "Add Task (Natural Language)" menu handler (prompt for natural language input, call parse_natural_language_skill, create task with extracted data)
- [ ] T056 [US3] Instantiate NLPAgent in main.py and integrate with TaskManager
- [ ] T057 [US3] Add confirmation display showing extracted fields before task creation

**Checkpoint**: US3 complete - users can create tasks with natural language input

---

## Phase 6: User Story 4 - Voice Input for Task Creation (Priority: P4)

**Goal**: Enable hands-free task creation via speech-to-text

**Independent Test**: Launch voice input mode, speak task descriptions, verify transcription and task creation. Test error handling for poor audio.

### Implementation for User Story 4

- [x] T058 [P] [US4] Create VoiceAgent Sub-Agent skeleton in todo_app/agents/voice_agent.py
- [x] T059 [US4] Implement transcribe_voice_skill in VoiceAgent using SpeechRecognition with Google API as primary backend
- [x] T060 [US4] Add CMU Sphinx fallback to transcribe_voice_skill for offline mode
- [x] T061 [US4] Implement microphone input with PyAudio in VoiceAgent (5 second timeout, 10 second phrase limit)
- [x] T062 [US4] Add error handling for VoiceAgent (no microphone, poor audio quality, network errors)
- [ ] T063 [US4] Display user-friendly error messages for voice input failures in UIAgent
- [ ] T064 [US4] Add "Add Task (Voice Input)" option to main menu in main.py
- [ ] T065 [US4] Implement "Add Task (Voice Input)" menu handler (call transcribe_voice_skill, pass to NLPAgent, create task)
- [ ] T066 [US4] Instantiate VoiceAgent in main.py
- [ ] T067 [US4] Show transcribed text to user for confirmation before creating task
- [ ] T068 [US4] Handle edge case: transcription timeout (return to menu without error)

**Checkpoint**: US4 complete - users can create tasks via voice input

---

## Phase 7: User Story 5 - Multi-Language Support (Priority: P5)

**Goal**: Support English, Urdu, and Spanish interfaces with JSON-based translations

**Independent Test**: Switch languages, verify all UI elements display in selected language, test fallback to English for missing translations.

### Implementation for User Story 5

- [x] T069 [P] [US5] Create LanguageAgent Sub-Agent skeleton in todo_app/agents/language_agent.py
- [x] T070 [P] [US5] Create English translation file todo_app/locales/en.json with all UI strings (menu items, labels, errors, success messages)
- [x] T071 [P] [US5] Create Urdu translation file todo_app/locales/ur.json with all UI strings translated
- [x] T072 [P] [US5] Create Spanish translation file todo_app/locales/es.json with all UI strings translated
- [x] T073 [US5] Implement load_language_skill in LanguageAgent (load JSON file, store in translations dict)
- [x] T074 [US5] Implement translate_skill in LanguageAgent (lookup key, fallback to English if missing)
- [x] T075 [US5] Implement get_current_language_skill in LanguageAgent (return active language code)
- [ ] T076 [US5] Refactor UIAgent to use LanguageAgent.translate_skill for all display text
- [ ] T077 [US5] Update all menu text in main.py to use translations
- [ ] T078 [US5] Update all error and success messages to use translations
- [ ] T079 [US5] Add "Change Language" option to main menu in main.py
- [ ] T080 [US5] Implement "Change Language" menu handler (prompt for language code, call load_language_skill)
- [ ] T081 [US5] Instantiate LanguageAgent in main.py, load default language from config.json
- [ ] T082 [US5] Handle edge case: missing or corrupted language file (fallback to English, log warning)
- [ ] T083 [US5] Document terminal requirements for Urdu script (Unicode support) in README

**Checkpoint**: US5 complete - application supports 3 languages with graceful fallback

---

## Phase 8: User Story 6 - Mood-Based Task Suggestion (Priority: P6)

**Goal**: Recommend tasks based on user's current mood/energy level

**Independent Test**: Trigger mood check, enter various mood levels (1-5), verify appropriate task suggestions (low mood → easy tasks, high mood → hard tasks).

### Implementation for User Story 6

- [ ] T084 [US6] Implement suggest_task_by_mood_skill in TaskManager (filter tasks by priority and complexity based on mood rating 1-5)
- [ ] T085 [US6] Add logic to suggest_task_by_mood_skill (mood 1-2 → low priority pending tasks, mood 4-5 → high priority pending tasks, mood 3 → medium priority)
- [ ] T086 [US6] Handle edge case in suggest_task_by_mood_skill (no matching tasks → inform user and suggest creating new task)
- [ ] T087 [US6] Add "Mood-Based Suggestion" option to main menu in main.py
- [ ] T088 [US6] Implement "Mood-Based Suggestion" menu handler (prompt for mood rating 1-5, call suggest_task_by_mood_skill, display suggested task)
- [ ] T089 [US6] Display mood rating prompt with explanatory text ("How are you feeling? 1=Low Energy, 5=High Energy")
- [ ] T090 [US6] Add option to accept or decline suggested task

**Checkpoint**: US6 complete - users get mood-appropriate task recommendations

---

## Phase 9: User Story 7 - Recurring Tasks (Priority: P7)

**Goal**: Support daily/weekly/monthly recurring tasks that auto-regenerate on completion

**Independent Test**: Create recurring tasks (daily, weekly, monthly), complete them, verify new instances created with correct next due dates.

### Implementation for User Story 7

- [x] T091 [US7] Implement process_recurring_tasks_skill in TaskManager (create next instance based on recurrence pattern)
- [x] T092 [US7] Add recurrence date calculation logic to process_recurring_tasks_skill (DAILY: +1 day, WEEKLY: +7 days, MONTHLY: +1 month same day)
- [x] T093 [US7] Handle edge case: monthly recurrence when next month has fewer days (use last day of month)
- [x] T094 [US7] Integrate process_recurring_tasks_skill into mark_complete_skill (call after setting completed status)
- [ ] T095 [US7] Update "Add Task" menu handler to prompt for recurrence setting (None/Daily/Weekly/Monthly)
- [ ] T096 [US7] Update "Update Task" menu handler to allow changing recurrence setting
- [ ] T097 [US7] Display recurrence indicator in task table (icon or label showing recurrence pattern)
- [ ] T098 [US7] Handle edge case: delete recurring task (confirm deletion, ensure no new instances created)

**Checkpoint**: US7 complete - recurring tasks automatically regenerate on completion

---

## Phase 10: User Story 8 - Gamification (Streaks, XP, Badges) (Priority: P8)

**Goal**: Track daily streaks, award XP for completions, and grant badges for milestones

**Independent Test**: Complete tasks on consecutive days, verify streak tracking, XP awards (10 base, +25 before due date, +15 before 8 AM), badge unlocks (Early Bird, 7-Day Streak, Task Master).

### Implementation for User Story 8

- [x] T099 [P] [US8] Create GamificationAgent Sub-Agent skeleton in todo_app/agents/gamification_agent.py
- [x] T100 [US8] Implement award_xp_skill in GamificationAgent (calculate XP: 10 base, +25 if before due date, +15 if before 8 AM)
- [x] T101 [US8] Implement update_streak_skill in GamificationAgent (check last_completion_date, increment or reset streak)
- [x] T102 [US8] Implement check_badge_eligibility_skill in GamificationAgent (check for Early Bird, 7-Day Streak, Task Master badges)
- [x] T103 [US8] Add badge definitions to GamificationAgent (Early Bird: completed before 8 AM, 7-Day Streak: 7 consecutive days, Task Master: 50 total completions)
- [ ] T104 [US8] Integrate GamificationAgent into mark_complete_skill (call award_xp, update_streak, check_badge_eligibility after completion)
- [ ] T105 [US8] Instantiate GamificationAgent and UserProfile in main.py
- [ ] T106 [US8] Add "View Stats" option to main menu in main.py
- [ ] T107 [US8] Implement "View Stats" menu handler (display total_xp, daily_streak, earned_badges)
- [ ] T108 [US8] Display XP gain notification after task completion (e.g., "+10 XP earned!")
- [ ] T109 [US8] Display badge unlock notification when badge is earned (e.g., "🏆 Badge Unlocked: Early Bird!")
- [ ] T110 [US8] Display streak icon (🏆) and count in startup screen

**Checkpoint**: US8 complete - gamification mechanics motivate user engagement

---

## Phase 11: User Story 9 - Focus Mode (Pomodoro Timer) (Priority: P9)

**Goal**: Provide Pomodoro timer (25/50 minutes) with live countdown for focused work sessions

**Independent Test**: Select task, start focus mode (25 or 50 min), observe live countdown, test cancellation with Ctrl+C, verify completion notification.

### Implementation for User Story 9

- [x] T111 [P] [US9] Create FocusAgent Sub-Agent skeleton in todo_app/agents/focus_agent.py
- [x] T112 [US9] Implement start_pomodoro_skill in FocusAgent using rich.live.Live for dynamic countdown display
- [x] T113 [US9] Add threading logic to start_pomodoro_skill for non-blocking timer updates
- [x] T114 [US9] Implement countdown timer logic (decrement every second, display MM:SS format)
- [x] T115 [US9] Add keyboard interrupt handling (Ctrl+C) to cancel timer and return False
- [x] T116 [US9] Display completion notification when timer finishes (green panel with "Focus session complete!" message)
- [ ] T117 [US9] Add "Focus Mode" option to main menu in main.py
- [ ] T118 [US9] Implement "Focus Mode" menu handler (prompt for task selection, prompt for duration 25/50, call start_pomodoro_skill)
- [ ] T119 [US9] Instantiate FocusAgent in main.py
- [ ] T120 [US9] Handle edge case: no task selected for focus mode (prompt user to select task first)
- [ ] T121 [US9] Display task title and focus icon (🎯) during countdown

**Checkpoint**: US9 complete - users can start focused work sessions with timer

---

## Phase 12: User Story 10 - Productivity Analytics Dashboard (Priority: P10)

**Goal**: Display productivity metrics (tasks completed today/week, overdue count, most productive day/time, average completion time)

**Independent Test**: Use app over several days, complete tasks at various times, view analytics dashboard, verify all metrics are accurate.

### Implementation for User Story 10

- [x] T122 [P] [US10] Create AnalyticsAgent Sub-Agent skeleton in todo_app/agents/analytics_agent.py
- [x] T123 [US10] Implement calculate_metrics_skill in AnalyticsAgent (return dict with all metrics)
- [x] T124 [US10] Add tasks_completed_today calculation to calculate_metrics_skill (count completed tasks with today's date)
- [x] T125 [US10] Add tasks_completed_this_week calculation to calculate_metrics_skill (count completed tasks in current week)
- [x] T126 [US10] Add total_overdue calculation to calculate_metrics_skill (count pending tasks past due date)
- [x] T127 [US10] Add most_productive_day calculation to calculate_metrics_skill (group by day of week, find max)
- [x] T128 [US10] Add most_productive_hour calculation to calculate_metrics_skill (group by hour, find max)
- [x] T129 [US10] Add average_completion_time calculation to calculate_metrics_skill (average of completed_at - created_at)
- [x] T130 [US10] Implement display_analytics_dashboard_skill in UIAgent (render metrics in formatted panels)
- [ ] T131 [US10] Add "Analytics Dashboard" option to main menu in main.py
- [ ] T132 [US10] Implement "Analytics Dashboard" menu handler (call calculate_metrics_skill, display_analytics_dashboard_skill)
- [ ] T133 [US10] Instantiate AnalyticsAgent in main.py
- [ ] T134 [US10] Handle edge case: no completed tasks (display "No data available yet" message)

**Checkpoint**: US10 complete - users can view comprehensive productivity metrics

---

## Phase 13: User Story 11 - CLI Charts for Visualization (Priority: P11)

**Goal**: Generate text-based bar charts showing tasks completed per day over last week

**Independent Test**: Complete varying numbers of tasks across multiple days, view chart, verify bars are correctly scaled and readable.

### Implementation for User Story 11

- [x] T135 [US11] Implement generate_weekly_chart_skill in AnalyticsAgent (create Rich Table with text-based bar chart)
- [x] T136 [US11] Add data aggregation logic to generate_weekly_chart_skill (count tasks per day for last 7 days)
- [x] T137 [US11] Add bar scaling logic to generate_weekly_chart_skill (normalize to max 40 characters)
- [x] T138 [US11] Add color coding to bars (green for high counts, yellow for medium, red for low)
- [x] T139 [US11] Use full-block character (█) for solid bars
- [ ] T140 [US11] Add "View Weekly Chart" option to main menu in main.py
- [ ] T141 [US11] Implement "View Weekly Chart" menu handler (call generate_weekly_chart_skill, display chart)
- [ ] T142 [US11] Handle edge case: no data for certain days (display zero or empty bars)
- [ ] T143 [US11] Ensure chart fits within typical terminal width (80-120 characters)

**Checkpoint**: US11 complete - users can visualize productivity trends with charts

---

## Phase 14: User Story 12 - Startup Screen and Quote of the Day (Priority: P12)

**Goal**: Display welcome screen with ASCII art, pending task count, streak, and inspirational quote

**Independent Test**: Launch app, verify ASCII art displays, pending count accurate, streak shown, quote fetched (or fallback used if API unavailable).

### Implementation for User Story 12

- [ ] T144 [P] [US12] Create quotes utility in todo_app/utils/quotes.py with fetch_quote_skill function
- [ ] T145 [US12] Implement fetch_quote_skill using requests to call ZenQuotes API (https://zenquotes.io/api/random) with 5 second timeout
- [ ] T146 [US12] Add embedded fallback quotes list to quotes.py (5-10 inspirational quotes with authors)
- [ ] T147 [US12] Add error handling to fetch_quote_skill (timeout, network error, invalid JSON → use fallback)
- [ ] T148 [US12] Implement display_startup_screen_skill in UIAgent with parameters (pending_count, streak, quote)
- [ ] T149 [US12] Design ASCII art logo for todo application in display_startup_screen_skill
- [ ] T150 [US12] Add pending task count display to startup screen with 📊 icon
- [ ] T151 [US12] Add daily streak display to startup screen with 🏆 icon
- [ ] T152 [US12] Add quote of the day display to startup screen with 💡 icon and author attribution
- [ ] T153 [US12] Call display_startup_screen_skill at beginning of main.py before menu loop
- [ ] T154 [US12] Pass pending_count (from TaskManager), streak (from UserProfile), and quote (from fetch_quote_skill) to startup screen
- [ ] T155 [US12] Handle edge case: quote API unavailable (silently use fallback, no error to user)

**Checkpoint**: US12 complete - application has polished startup experience

---

## Phase 15: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, documentation, and quality assurance

- [ ] T156 [P] Create comprehensive README.md in docs/ with setup instructions, usage guide, feature list
- [ ] T157 [P] Create future_improvements.md in docs/ with potential enhancements
- [ ] T158 [P] Add PEP 257 docstrings to all modules, classes, and public methods across all agents
- [ ] T159 [P] Add inline comments for complex logic in NLPAgent, AnalyticsAgent, GamificationAgent
- [ ] T160 Review error handling across all agents (ensure all user inputs validated, friendly error messages)
- [ ] T161 Review and optimize performance for 10,000 task scenario (verify search/filter/sort performance)
- [ ] T162 Add sample task loading mechanism (create sample_tasks fixture with diverse examples)
- [ ] T163 Add help command to main menu displaying feature explanations and usage tips
- [ ] T164 [P] Create .env template if needed for configuration
- [ ] T165 Final end-to-end testing of all user stories in sequence
- [ ] T166 Verify constitutional compliance (Python 3.10+, Sub-Agent architecture, in-memory only, approved libraries)
- [ ] T167 Run full application and validate against all 12 user stories acceptance scenarios

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (Phase 1) - BLOCKS all user stories
- **User Stories (Phase 3-14)**: All depend on Foundational (Phase 2) completion
  - User stories P1-P12 can proceed in priority order
  - Some stories have natural dependencies:
    - US3 (NLP) builds on US1 (Basic Task Management)
    - US4 (Voice) builds on US3 (NLP)
    - US6 (Mood) depends on US1 (needs tasks to suggest)
    - US7 (Recurring) builds on US1 (extends task completion)
    - US8 (Gamification) builds on US1 (tracks completions)
    - US9 (Focus) depends on US1 (needs tasks to focus on)
    - US10 (Analytics) depends on US8 (uses completion history)
    - US11 (Charts) builds on US10 (visualizes analytics)
    - US12 (Startup) depends on US1 and US8 (displays stats)
- **Polish (Phase 15)**: Depends on all desired user stories being complete

### User Story Dependencies (Sequential Recommended)

1. **US1 (P1)** → Core MVP - MUST complete first
2. **US2 (P2)** → Builds on US1 - Independent increment
3. **US3 (P3)** → Uses US1's TaskManager - Independent increment
4. **US4 (P4)** → Uses US3's NLP - Dependent on US3
5. **US5 (P5)** → Independent - Refactors UI text
6. **US6 (P6)** → Uses US1's tasks - Dependent on US1
7. **US7 (P7)** → Extends US1's completion - Dependent on US1
8. **US8 (P8)** → Tracks US1 completions - Dependent on US1
9. **US9 (P9)** → Uses US1's tasks - Dependent on US1
10. **US10 (P10)** → Uses US8's data - Dependent on US8
11. **US11 (P11)** → Visualizes US10 data - Dependent on US10
12. **US12 (P12)** → Displays US1 and US8 stats - Dependent on US1, US8

### Within Each User Story

- Models created first
- Services/Agents implement skills
- Main menu integration
- Error handling added
- Story validated independently

### Parallel Opportunities

**Setup Phase (all can run in parallel)**:
- T003 (.gitignore), T004 (pytest.ini), T005 (__init__ files), T006 (config.json)

**Foundational Phase (some can run in parallel)**:
- T008 (UserProfile), T009 (Configuration), T011 (validators) - all parallel with T007 (Task model)

**Within User Stories**:
- US1: T012 (TaskManager skeleton) and T013 (UIAgent skeleton) can run in parallel
- US5: T070 (en.json), T071 (ur.json), T072 (es.json) can all run in parallel
- US8: T099 (GamificationAgent skeleton) parallel with other agents
- US9: T111 (FocusAgent skeleton) parallel with other agents
- US10: T122 (AnalyticsAgent skeleton) parallel with other agents
- Polish: T156 (README), T157 (future_improvements), T158 (docstrings), T159 (comments), T164 (.env) all parallel

---

## Parallel Example: User Story 1 (MVP)

```bash
# After Foundational phase completes, launch US1 in parallel where possible:

# Parallel Group 1 (different files):
Task T012: Create TaskManager skeleton in todo_app/agents/task_manager.py
Task T013: Create UIAgent skeleton in todo_app/agents/ui_agent.py

# Then Sequential Group (TaskManager skills):
Task T014-T020: Implement TaskManager skills one by one

# Then Sequential Group (UIAgent skills):
Task T021-T026: Implement UIAgent skills one by one

# Then Sequential (main.py integration):
Task T027-T035: Implement menu loop and handlers
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Complete Phase 1: Setup (T001-T006)
2. ✅ Complete Phase 2: Foundational (T007-T011) - **CRITICAL CHECKPOINT**
3. ✅ Complete Phase 3: User Story 1 (T012-T035) - **MVP COMPLETE**
4. 🎯 **STOP and VALIDATE**: Test all CRUD operations independently
5. 🚀 Deploy/demo functional todo list
6. 📊 Gather feedback before adding more features

### Incremental Delivery (Recommended)

1. Setup + Foundational (T001-T011) → Foundation ready
2. **Add US1 (T012-T035)** → Test independently → ✅ MVP deployed
3. **Add US2 (T036-T048)** → Test independently → ✅ Enhanced organization
4. **Add US3 (T049-T057)** → Test independently → ✅ Natural language input
5. **Add US4 (T058-T068)** → Test independently → ✅ Voice input
6. **Add US5 (T069-T083)** → Test independently → ✅ Multi-language
7. **Add US6 (T084-T090)** → Test independently → ✅ Mood suggestions
8. **Add US7 (T091-T098)** → Test independently → ✅ Recurring tasks
9. **Add US8 (T099-T110)** → Test independently → ✅ Gamification
10. **Add US9 (T111-T121)** → Test independently → ✅ Focus mode
11. **Add US10 (T122-T134)** → Test independently → ✅ Analytics
12. **Add US11 (T135-T143)** → Test independently → ✅ Charts
13. **Add US12 (T144-T155)** → Test independently → ✅ Startup screen
14. Polish (T156-T167) → Final quality assurance

**Each story adds value without breaking previous stories**

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T011)
2. Once Foundational is done:
   - **Developer A**: US1 (MVP) - Priority 1
   - Wait for US1 completion (it's blocking for most stories)
3. After US1 complete:
   - **Developer A**: US2 (Search/Filter/Sort)
   - **Developer B**: US5 (Multi-language) - Independent
   - **Developer C**: US3 (Natural Language)
4. Continue with priority-based assignment

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** = maps task to specific user story for traceability (US1-US12)
- **Tests NOT included** = Specification does not request TDD approach
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Constitutional compliance verified in Phase 15
- Total: **167 tasks** across 15 phases
- MVP: **35 tasks** (Phase 1-3: Setup + Foundational + US1)
- Full feature set: **155 tasks** (excluding Polish)

---

**Task Breakdown Status**: ✅ Complete
**Total Tasks**: 167
**Parallelizable Tasks**: 32 (marked with [P])
**User Stories**: 12 (P1-P12)
**MVP Scope**: Phase 1-3 (T001-T035, 35 tasks)
**Ready for Implementation**: Yes
