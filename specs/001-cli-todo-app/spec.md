# Feature Specification: In-Memory Python CLI Todo Application

**Feature Branch**: `001-cli-todo-app`
**Created**: 2025-12-05
**Status**: Draft
**Input**: User description: "In-Memory Python CLI Todo Application with advanced features including natural language processing, voice input, multi-language support, gamification, and productivity analytics"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Basic Task Management (Priority: P1)

A user needs to quickly capture, organize, and track their daily tasks using a simple command-line interface without needing to learn complex commands or syntax.

**Why this priority**: Core task management is the foundation of the entire application. Without the ability to create, view, update, delete, and complete tasks, no other features have value.

**Independent Test**: Can be fully tested by launching the app, adding several tasks with different priorities and due dates, viewing them in a formatted table, marking some complete, updating others, and deleting unwanted tasks. Delivers immediate value as a functional todo list.

**Acceptance Scenarios**:

1. **Given** the CLI is launched, **When** user selects "Add Task" and enters title "Complete project report", description "Quarterly report for Q4", priority "High", tags "work,urgent", and due date "2025-12-10 17:00", **Then** task is created with unique ID, pending status, and current timestamp
2. **Given** multiple tasks exist, **When** user selects "View All Tasks", **Then** all tasks are displayed in a formatted table with icons for status and priority, color-coded by priority and completion status
3. **Given** a task exists with ID 5, **When** user selects "Update Task" and changes priority to "Low" and adds tag "deferred", **Then** task 5 is updated with new priority and tags while preserving other fields
4. **Given** a task exists with ID 3, **When** user marks it as complete, **Then** task status changes to "Completed", completion timestamp is set, and task displays with green completed icon
5. **Given** a task exists with ID 7, **When** user deletes it, **Then** task is removed from the list and no longer appears in any views

---

### User Story 2 - Search, Filter, and Sort (Priority: P2)

A user with many tasks needs to quickly find specific tasks or focus on subsets of tasks (e.g., high priority items, work-related tasks, or overdue items) without manually scanning the entire list.

**Why this priority**: As the task list grows beyond 10-15 items, the ability to organize and find tasks becomes essential for productivity. This enables the application to scale with the user's needs.

**Independent Test**: Can be tested by creating 20+ diverse tasks with various priorities, tags, statuses, and due dates, then using search to find tasks by keyword, filtering to show only high-priority pending tasks, and sorting by different criteria (due date, priority, creation date). Delivers value by making large task lists manageable.

**Acceptance Scenarios**:

1. **Given** 20 tasks exist with various titles and descriptions, **When** user searches for "report", **Then** only tasks containing "report" in title or description are displayed
2. **Given** tasks with mixed status (completed/pending), **When** user filters by status "Pending", **Then** only pending tasks are shown
3. **Given** tasks with different priority levels, **When** user filters by priority "High", **Then** only high-priority tasks are displayed
4. **Given** tasks with various tags, **When** user filters by tag "work", **Then** only tasks tagged with "work" are shown
5. **Given** tasks with different due dates, **When** user sorts by due date ascending, **Then** tasks are ordered from earliest to latest due date
6. **Given** tasks with alphabetically diverse titles, **When** user sorts by title, **Then** tasks are displayed in alphabetical order by title

---

### User Story 3 - Natural Language Task Input (Priority: P3)

A user wants to add tasks quickly using natural language (e.g., "Finish ML assignment by next Friday at 6pm") instead of filling out multiple form fields, making task capture faster and more intuitive.

**Why this priority**: Reduces friction in task creation and makes the application more user-friendly. While not essential for core functionality, it significantly improves user experience and adoption.

**Independent Test**: Can be tested by typing natural language strings like "Submit report by tomorrow 5pm urgent", "Buy groceries this weekend", "Call mom next Monday morning high priority" and verifying the system correctly extracts task title, due date/time, and priority. Delivers value by streamlining the most frequent operation (task creation).

**Acceptance Scenarios**:

1. **Given** user enters "Finish ML assignment by next Friday at 6pm", **When** system parses the input, **Then** task is created with title "Finish ML assignment", due date set to next Friday at 18:00, and medium priority
2. **Given** user enters "Submit urgent report by tomorrow 9am", **When** system parses the input, **Then** task is created with title "Submit report", due date set to tomorrow at 09:00, and high priority (due to "urgent" keyword)
3. **Given** user enters "Buy groceries this weekend", **When** system parses the input, **Then** task is created with title "Buy groceries", due date set to upcoming Saturday, and low priority
4. **Given** user enters "Call mom asap", **When** system parses the input, **Then** task is created with title "Call mom" and high priority (due to "asap" keyword)

---

### User Story 4 - Voice Input for Task Creation (Priority: P4)

A user wants to add tasks hands-free using voice input (speech-to-text), enabling task capture while multitasking or when typing is inconvenient.

**Why this priority**: Enhances accessibility and convenience but requires additional dependencies and setup. Useful for specific scenarios but not critical for most users.

**Independent Test**: Can be tested by launching voice input mode, speaking task descriptions naturally, and verifying they are transcribed and parsed correctly as tasks. Delivers value for hands-free operation.

**Acceptance Scenarios**:

1. **Given** user selects voice input mode, **When** user speaks "Add task: review presentation by Wednesday afternoon", **Then** speech is transcribed to text and processed as natural language input to create a task
2. **Given** voice input is active, **When** user speaks clearly in a quiet environment, **Then** transcription accuracy is high enough to create usable tasks
3. **Given** voice input fails or user cancels, **When** operation is terminated, **Then** user returns to main menu without errors

---

### User Story 5 - Multi-Language Support (Priority: P5)

A user who prefers to work in Urdu, Spanish, or other supported languages wants the entire interface (menus, prompts, messages) to display in their chosen language.

**Why this priority**: Critical for international users or non-English speakers, but can be implemented after core features are stable. Requires careful planning for maintainability.

**Independent Test**: Can be tested by switching language to Urdu or Spanish and verifying all UI elements (menu items, prompts, error messages, table headers) display in the selected language while functionality remains unchanged. Delivers value by making the application accessible to non-English speakers.

**Acceptance Scenarios**:

1. **Given** user selects Urdu language, **When** application displays menus and prompts, **Then** all text is shown in Urdu script
2. **Given** user selects Spanish language, **When** application displays menus and prompts, **Then** all text is shown in Spanish
3. **Given** user changes language from English to Urdu, **When** existing tasks are displayed, **Then** UI elements are in Urdu but task content remains in original language
4. **Given** missing translation exists, **When** application encounters untranslated text, **Then** it falls back to English gracefully

---

### User Story 6 - Mood-Based Task Suggestion (Priority: P6)

A user starting their work session wants the application to recommend an appropriate task based on their current mood/energy level, helping them choose where to start without decision fatigue.

**Why this priority**: Novel feature that adds value but is not essential. Should be implemented after core task management and filtering features are complete.

**Independent Test**: Can be tested by starting the application or triggering the mood check, entering different mood levels (1-5), and verifying appropriate task suggestions (low mood → easy tasks, high mood → challenging tasks). Delivers value by reducing decision paralysis.

**Acceptance Scenarios**:

1. **Given** user rates mood as 1 or 2 (low), **When** system suggests a task, **Then** it recommends a low-priority or easy task (e.g., tasks with fewer dependencies or shorter estimated time)
2. **Given** user rates mood as 4 or 5 (high), **When** system suggests a task, **Then** it recommends a high-priority or challenging task
3. **Given** user rates mood as 3 (neutral), **When** system suggests a task, **Then** it recommends a medium-priority task
4. **Given** no tasks match mood criteria, **When** system attempts suggestion, **Then** it informs user and suggests creating a new task

---

### User Story 7 - Recurring Tasks (Priority: P7)

A user with regular repeating tasks (e.g., "Weekly team meeting every Monday 10am", "Monthly expense report") wants to create a task once and have it automatically regenerate when completed, rather than manually recreating it each time.

**Why this priority**: Valuable for users with routine tasks but adds complexity. Should be implemented after core task management is stable.

**Independent Test**: Can be tested by creating tasks marked as recurring (daily/weekly/monthly), completing them, and verifying new instances are automatically created with updated due dates. Delivers value by reducing repetitive data entry.

**Acceptance Scenarios**:

1. **Given** a task is marked as recurring daily, **When** user completes it, **Then** a new instance is created with due date set to next day
2. **Given** a task is marked as recurring weekly, **When** user completes it, **Then** a new instance is created with due date set to same day next week
3. **Given** a task is marked as recurring monthly, **When** user completes it, **Then** a new instance is created with due date set to same day next month
4. **Given** a recurring task is deleted, **When** deletion is confirmed, **Then** no future instances are created

---

### User Story 8 - Gamification (Streaks, XP, Badges) (Priority: P8)

A user wants to stay motivated and track their productivity achievements through game-like elements such as daily streaks, experience points for completing tasks, and badges for milestones.

**Why this priority**: Enhances engagement and motivation but is not essential for core functionality. Best implemented after analytics features are in place.

**Independent Test**: Can be tested by completing tasks on consecutive days (streak tracking), performing various actions to earn XP, and achieving milestones to unlock badges. Delivers value by increasing user engagement and motivation.

**Acceptance Scenarios**:

1. **Given** user completes at least one task per day for 7 consecutive days, **When** viewing gamification stats, **Then** daily streak shows "7 days" with streak icon
2. **Given** user completes a task, **When** task is marked complete, **Then** user earns 10 XP
3. **Given** user completes a task before its due date, **When** task is marked complete, **Then** user earns 25 XP (bonus)
4. **Given** user completes a task before 8 AM, **When** task is marked complete, **Then** "Early Bird" badge is awarded
5. **Given** user maintains 7-day streak, **When** streak milestone is reached, **Then** "7-Day Streak" badge is awarded
6. **Given** user completes 50 tasks total, **When** 50th task is completed, **Then** "Task Master" badge is awarded
7. **Given** user skips a day without completing tasks, **When** new day begins, **Then** streak resets to 0

---

### User Story 9 - Focus Mode (Pomodoro Timer) (Priority: P9)

A user wants to dedicate focused time to a specific task by starting a countdown timer (25 or 50 minutes) displayed in the CLI, helping them maintain concentration and track time spent.

**Why this priority**: Useful productivity feature but requires live updating CLI display and timer management. Should be implemented after core features are complete.

**Independent Test**: Can be tested by selecting a task, starting a focus session (25 or 50 minutes), observing the live countdown timer, and verifying the session completes correctly. Delivers value by encouraging focused work sessions.

**Acceptance Scenarios**:

1. **Given** user selects a task and chooses 25-minute focus mode, **When** timer starts, **Then** countdown displays live in CLI showing remaining time
2. **Given** focus timer is running, **When** timer reaches zero, **Then** notification/alert is displayed and task is highlighted as "focus session completed"
3. **Given** focus timer is running, **When** user cancels session, **Then** timer stops and user returns to main menu
4. **Given** user selects 50-minute focus mode, **When** timer starts, **Then** countdown displays 50:00 and decrements correctly

---

### User Story 10 - Productivity Analytics Dashboard (Priority: P10)

A user wants to review their productivity metrics and patterns (tasks completed today/this week, overdue tasks, most productive time/day, average completion time) to understand their work habits and improve efficiency.

**Why this priority**: Valuable insights but requires significant data collection and analysis. Should be implemented after sufficient task completion data is available.

**Independent Test**: Can be tested by using the application over several days/weeks, completing various tasks at different times, then viewing the analytics dashboard to verify accurate metrics and insights. Delivers value by providing actionable productivity insights.

**Acceptance Scenarios**:

1. **Given** user has completed tasks today, **When** viewing analytics dashboard, **Then** "Tasks completed today" metric is accurate
2. **Given** user has completed tasks this week, **When** viewing analytics dashboard, **Then** "Tasks completed this week" metric is accurate
3. **Given** tasks are overdue, **When** viewing analytics dashboard, **Then** "Total overdue tasks" count is accurate
4. **Given** user has completed tasks on various days, **When** viewing analytics dashboard, **Then** "Most productive day of the week" is identified correctly
5. **Given** user has completed tasks at various times, **When** viewing analytics dashboard, **Then** "Most productive time of day" is identified correctly
6. **Given** tasks have completion timestamps, **When** viewing analytics dashboard, **Then** "Average task completion time" is calculated correctly

---

### User Story 11 - CLI Charts for Visualization (Priority: P11)

A user wants to see visual representations of their productivity data (e.g., bar chart showing tasks completed per day over the last week) directly in the CLI for quick insights.

**Why this priority**: Enhances analytics with visual feedback but is purely supplementary. Should be implemented last as a polish feature.

**Independent Test**: Can be tested by completing various numbers of tasks across multiple days, then viewing the chart and verifying it accurately represents the data in a readable text-based format. Delivers value by making productivity trends immediately visible.

**Acceptance Scenarios**:

1. **Given** user has completed varying numbers of tasks over the last 7 days, **When** viewing weekly completion chart, **Then** text-based bar chart displays correct bars for each day
2. **Given** chart data exists, **When** chart is rendered, **Then** it is readable, properly scaled, and fits within typical CLI width
3. **Given** no data exists for certain days, **When** viewing chart, **Then** those days show zero or empty bars

---

### User Story 12 - Startup Screen and Quote of the Day (Priority: P12)

A user launching the application wants to see an attractive welcome screen with ASCII art logo, quick summary (pending tasks, streak), and inspirational quote to create a positive and informative startup experience.

**Why this priority**: Nice-to-have polish feature that enhances UX but provides no functional value. Should be implemented last.

**Independent Test**: Can be tested by launching the application and verifying the welcome screen displays correctly with all elements. Delivers value through improved user experience and engagement.

**Acceptance Scenarios**:

1. **Given** application is launched, **When** startup screen is displayed, **Then** ASCII art logo/name is shown
2. **Given** pending tasks exist, **When** startup screen is displayed, **Then** total pending tasks count is accurate
3. **Given** user has an active streak, **When** startup screen is displayed, **Then** current daily streak is shown with icon
4. **Given** startup screen is displayed, **When** quote of the day is fetched, **Then** a random inspirational quote is shown

---

### Edge Cases

- What happens when a user tries to update or delete a task with a non-existent ID? System should display a clear error message: "Task ID not found" and return to menu.
- What happens when a user enters an invalid date format during task creation/update? System should display format error and prompt for correct format (e.g., "YYYY-MM-DD HH:MM").
- What happens when natural language parsing cannot extract a due date from user input? System should create task with no due date and notify user that no date was detected.
- What happens when voice input cannot be transcribed (poor audio quality, background noise)? System should display error message and offer option to retry or return to menu.
- What happens when a language file is missing or corrupted? System should fall back to English and log a warning.
- What happens when no tasks match filter criteria? System should display "No tasks found matching criteria" message.
- What happens when a recurring task's next due date would be in the past (e.g., completed late)? System should calculate next valid future occurrence.
- What happens when user tries to start focus mode but no task is selected? System should prompt user to select a task first.
- What happens when quote of the day API is unavailable or times out? System should display a fallback quote or skip quote display gracefully.
- What happens when application is run for the first time with no existing data? System should offer to load sample/demo tasks and display tutorial/help option.

## Requirements *(mandatory)*

### Functional Requirements

**Core Task Management**:

- **FR-001**: System MUST allow users to create a new task with title (required), description (optional), priority (High/Medium/Low), tags (list of strings), and due date/time (optional)
- **FR-002**: System MUST assign a unique ID to each task upon creation (integer or UUID)
- **FR-003**: System MUST automatically set creation timestamp when a task is created
- **FR-004**: System MUST allow users to delete any task by its ID
- **FR-005**: System MUST allow users to update any task field (title, description, priority, tags, due date) by task ID
- **FR-006**: System MUST allow users to view all tasks in a formatted table with color coding and icons
- **FR-007**: System MUST allow users to toggle task status between Pending and Completed
- **FR-008**: System MUST set completion timestamp when a task is marked as Completed
- **FR-009**: System MUST display tasks with appropriate icons: ✅ for Completed, 🕒 for Pending, 🔥 for High Priority, ⚡ for Medium Priority, 🌱 for Low Priority
- **FR-010**: System MUST color-code tasks: Green for completed, Red for high priority, Yellow for medium priority, Blue for low priority, Bright Red for overdue tasks
- **FR-011**: System MUST display table headers in Cyan and Bold

**Organization Features**:

- **FR-012**: System MUST allow users to search tasks by keyword in title or description
- **FR-013**: System MUST allow users to filter tasks by status (Pending/Completed)
- **FR-014**: System MUST allow users to filter tasks by priority (High/Medium/Low)
- **FR-015**: System MUST allow users to filter tasks by specific tag
- **FR-016**: System MUST allow users to sort tasks by due date (ascending/descending)
- **FR-017**: System MUST allow users to sort tasks by priority (High to Low)
- **FR-018**: System MUST allow users to sort tasks by title (alphabetical)
- **FR-019**: System MUST allow users to sort tasks by creation date (newest/oldest)

**Advanced Features**:

- **FR-020**: System MUST parse natural language task input to extract title, due date, and priority keywords
- **FR-021**: System MUST recognize priority keywords such as "urgent", "asap", "important" and set priority accordingly
- **FR-022**: System MUST recognize relative date expressions like "tomorrow", "next Friday", "this weekend", "next Monday"
- **FR-023**: System MUST extract time information from natural language input (e.g., "6pm", "9am", "morning", "afternoon")
- **FR-024**: System MUST support voice input for task creation using speech-to-text conversion
- **FR-025**: System MUST support multi-language interface with English (en), Urdu (ur), and Spanish (es) as minimum required languages
- **FR-026**: System MUST load language strings from JSON files for easy translation management
- **FR-027**: System MUST allow users to switch interface language at runtime
- **FR-028**: System MUST prompt user for mood rating (1-5 scale) on startup or via command
- **FR-029**: System MUST suggest appropriate tasks based on mood: low mood (1-2) suggests easy/low-priority tasks, high mood (4-5) suggests challenging/high-priority tasks
- **FR-030**: System MUST support marking tasks as recurring (daily, weekly, monthly)
- **FR-031**: System MUST automatically create next instance of recurring task when current instance is completed, with updated due date

**Gamification**:

- **FR-032**: System MUST track daily streak (consecutive days with at least one completed task)
- **FR-033**: System MUST reset streak to 0 if a day passes with no completed tasks
- **FR-034**: System MUST award 10 XP for completing a task
- **FR-035**: System MUST award 25 XP bonus for completing a task before its due date
- **FR-036**: System MUST award "Early Bird" badge for completing a task before 8 AM
- **FR-037**: System MUST award "7-Day Streak" badge when user maintains 7 consecutive days of task completion
- **FR-038**: System MUST award "Task Master" badge when user completes 50 total tasks
- **FR-039**: System MUST display current streak count with 🏆 icon
- **FR-040**: System MUST display earned badges in user profile or stats view

**Focus Mode**:

- **FR-041**: System MUST allow users to start focus session (Pomodoro timer) on a selected task
- **FR-042**: System MUST support 25-minute and 50-minute focus session durations
- **FR-043**: System MUST display live countdown timer in CLI during focus session with 🎯 icon
- **FR-044**: System MUST allow users to cancel focus session before completion
- **FR-045**: System MUST notify user when focus session completes

**Analytics and Visualization**:

- **FR-046**: System MUST track and display number of tasks completed today
- **FR-047**: System MUST track and display number of tasks completed this week
- **FR-048**: System MUST calculate and display total overdue tasks
- **FR-049**: System MUST identify and display most productive day of the week based on completion history
- **FR-050**: System MUST identify and display most productive time of day based on completion timestamps
- **FR-051**: System MUST calculate and display average task completion time
- **FR-052**: System MUST generate text-based bar charts for tasks completed per day over the last week

**User Experience**:

- **FR-053**: System MUST display welcome screen on startup with ASCII art logo/name
- **FR-054**: System MUST display pending task count on welcome screen
- **FR-055**: System MUST display current daily streak on welcome screen
- **FR-056**: System MUST fetch and display random inspirational "Quote of the Day" on welcome screen
- **FR-057**: System MUST provide menu-based interaction model for all features
- **FR-058**: System MUST provide help command explaining all available features and usage
- **FR-059**: System MUST handle invalid user inputs gracefully with clear error messages
- **FR-060**: System MUST validate date/time formats and prompt for correction if invalid
- **FR-061**: System MUST provide option to load sample/demo tasks for demonstration and testing

**Configuration and Persistence**:

- **FR-062**: System MUST support configuration file (e.g., config.json) for settings like default language and color theme
- **FR-063**: System MUST store all data in-memory (no database persistence required)
- **FR-064**: System MUST maintain data consistency during runtime session

### Key Entities

- **Task**: Represents a todo item with unique ID, title, optional description, status (Pending/Completed), priority (High/Medium/Low), tags (list of strings), optional due date/time, creation timestamp, optional completion timestamp, and optional recurrence settings (daily/weekly/monthly)

- **User Profile**: Represents gamification and analytics data including total XP, daily streak count, last completion date (for streak tracking), earned badges list, and task completion history (timestamps, task IDs)

- **Language Pack**: Represents a translation set containing all UI strings (menu items, prompts, messages, errors) for a specific language, stored in JSON format

- **Configuration**: Represents user preferences including default language, color theme settings, and other configurable options

- **Analytics Data**: Represents productivity metrics derived from task completion history, including daily/weekly completion counts, productivity patterns by day/time, and calculated statistics

## Success Criteria *(mandatory)*

### Measurable Outcomes

**Usability**:

- **SC-001**: Users can create a basic task (title and priority) in under 10 seconds
- **SC-002**: Users can create a task using natural language input in under 15 seconds without needing to understand form fields
- **SC-003**: Users can find a specific task from a list of 50+ tasks using search in under 5 seconds
- **SC-004**: Users can successfully complete primary workflows (add, view, complete, delete tasks) on first use without consulting help documentation 90% of the time

**Performance**:

- **SC-005**: Application startup completes in under 2 seconds on standard hardware
- **SC-006**: Task list displays with formatting and colors for up to 500 tasks without noticeable lag (under 1 second)
- **SC-007**: Search, filter, and sort operations complete in under 1 second for lists up to 1000 tasks
- **SC-008**: Focus mode timer updates display every second without lag or drift

**Functionality**:

- **SC-009**: Natural language parser correctly extracts due date from common phrases (tomorrow, next week, next Friday) with 90% accuracy
- **SC-010**: Natural language parser correctly identifies priority keywords (urgent, asap, important) with 85% accuracy
- **SC-011**: Voice input transcription achieves 80% accuracy in quiet environment with clear speech
- **SC-012**: All UI elements display correctly in all supported languages (English, Urdu, Spanish)
- **SC-013**: Streak tracking maintains 100% accuracy (increments on completion, resets on missed days)
- **SC-014**: Recurring tasks generate next instance correctly with proper due date calculation 100% of the time

**Accessibility**:

- **SC-015**: Users who prefer Urdu or Spanish can use the entire application in their chosen language without encountering untranslated elements in 95% of interface elements
- **SC-016**: Voice input provides functional task creation for users who cannot or prefer not to type
- **SC-017**: CLI display remains readable on terminals with minimum 80 character width and 24 line height

**Engagement**:

- **SC-018**: Gamification features (streaks, XP, badges) are tracked accurately 100% of the time
- **SC-019**: Analytics dashboard provides actionable insights by correctly identifying most productive day/time with 90% confidence
- **SC-020**: Users receive motivational feedback (XP gain, badge unlocks, streak notifications) immediately after relevant actions

**Reliability**:

- **SC-021**: Application handles invalid inputs without crashing and provides clear error messages 100% of the time
- **SC-022**: Application gracefully degrades when optional external services fail (quote API, voice input) and continues core functionality
- **SC-023**: Data remains consistent throughout runtime session with no data loss or corruption

## Dependencies and Assumptions *(mandatory)*

### Dependencies

- **External Libraries**: Application requires Python 3.10+, Rich library for CLI formatting, speech recognition library for voice input, natural language processing library (e.g., dateparser, parsedatetime) for parsing dates and times
- **External Services**: Quote of the day functionality requires access to external quote API or local quote database (fallback required if API unavailable)
- **System Requirements**: Voice input requires microphone access and functional audio input device

### Assumptions

- **Environment**: Users have Python 3.10+ installed and can run CLI applications
- **Language Files**: JSON translation files for English, Urdu, and Spanish will be created and maintained separately from code
- **Data Persistence**: In-memory storage is acceptable; data does not persist between application sessions (assumption based on "in-memory" requirement)
- **Speech Recognition**: Voice input uses standard speech recognition APIs available in Python ecosystem (e.g., SpeechRecognition library with Google Speech API or CMU Sphinx)
- **Natural Language Processing**: Date/time parsing uses existing NLP libraries rather than custom parsing logic
- **Default Behavior**: When natural language parsing cannot determine priority, default to Medium priority
- **Default Behavior**: When natural language parsing cannot extract due date, create task without due date
- **Recurrence Calculation**: Monthly recurring tasks use same day of month; if original due date is 31st and next month has 30 days, use last day of month
- **Timezone**: All dates and times use local system timezone
- **Quote Source**: Quote of the day uses free public API or embedded fallback quote list
- **Configuration Format**: Configuration file uses JSON format for easy parsing and editing
- **Sample Data**: Demo/sample tasks are hardcoded or loaded from JSON file for quick testing
- **Test Coverage**: Unit tests focus on core logic (task CRUD, filtering, sorting, gamification calculations, NLP parsing) rather than UI rendering
- **Color Support**: Terminal supports ANSI color codes (standard in modern terminals)
- **Unicode Support**: Terminal supports Unicode characters for icons and Urdu script
