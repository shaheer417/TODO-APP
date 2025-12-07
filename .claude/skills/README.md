# Todo Application Skills

This directory contains skill definitions for the Todo CLI application's sub-agents. Each skill provides access to specialized functionality through dedicated agent classes.

## Available Skills

### 1. UI Agent (`ui.md`)
**Purpose**: Terminal UI rendering and user interaction
**Key Features**:
- Display tasks in formatted Rich tables
- Show task details, menus, and headers
- Prompt for user input and confirmations
- Display success/error/info messages
- Show statistics dashboards
- Clear screen

**When to use**: Any time you need to display information to the user or get user input.

---

### 2. NLP Agent (`nlp.md`)
**Purpose**: Natural language processing for task input
**Key Features**:
- Parse natural language to extract task details
- Recognize priority keywords (urgent, asap, important, etc.)
- Extract due dates from relative expressions (tomorrow, next Friday, etc.)
- Extract and remove hashtags from text
- Clean task titles by removing keywords

**When to use**: When processing user input in natural language format.

---

### 3. Voice Agent (`voice.md`)
**Purpose**: Speech-to-text conversion for hands-free input
**Key Features**:
- Listen to microphone and transcribe speech
- Support Google Speech API (primary) and CMU Sphinx (offline fallback)
- Check microphone availability
- Test microphone functionality
- Graceful error handling

**When to use**: When implementing voice input mode for task creation.

---

### 4. Language Agent (`language.md`)
**Purpose**: Multi-language support and internationalization
**Key Features**:
- Load and manage translations (English, Urdu, Spanish)
- Translate UI text using dot notation keys
- Switch languages at runtime
- Detect RTL languages
- Fallback to English for missing translations

**When to use**: When displaying any UI text that should be translatable.

---

### 5. Gamification Agent (`gamification.md`)
**Purpose**: XP, streaks, and achievement badges
**Key Features**:
- Calculate XP for task completion (base + bonuses)
- Track daily completion streaks
- Award badges for achievements
- Provide gamification statistics
- Manage user profile data

**When to use**: When processing task completions or displaying user progress.

**XP System**:
- Base: 10 XP
- Before due date: +25 XP
- Before 8 AM: +15 XP

**Available Badges**:
- 🌅 Early Bird (task before 8 AM)
- 🔥 Week Warrior (7-day streak)
- 🏆 Month Master (30-day streak)
- ⭐ Task Master (10 tasks)
- 💎 Task Legend (50 tasks)
- 👑 Task Champion (100 tasks)
- 💯 Perfect Score (before due + before 8 AM)

---

### 6. Focus Agent (`focus.md`)
**Purpose**: Pomodoro timer for focused work sessions
**Key Features**:
- Start focus sessions (25 or 50 minutes)
- Display live countdown timer
- Support break timers (5 or 15 minutes)
- Color-coded progress visualization
- Callback support for session completion

**When to use**: When implementing focus mode or Pomodoro technique.

**Timer Presets**:
- Work: 25 min, 50 min
- Break: 5 min, 15 min

---

### 7. Analytics Agent (`analytics.md`)
**Purpose**: Productivity metrics and visualizations
**Key Features**:
- Calculate comprehensive productivity metrics
- Generate weekly ASCII bar charts
- Track priority and tag distributions
- Identify most productive day/hour
- Provide performance insights
- Display analytics dashboard

**When to use**: When showing productivity statistics, trends, or insights.

**Key Metrics**:
- Tasks completed (today, this week)
- Overdue tasks count
- Completion rate
- Average completion time
- Most productive day/hour
- Tag usage statistics

---

## Usage Pattern

Each skill follows this pattern:

```python
# 1. Import the agent
from todo_app.agents.{agent_name} import {AgentClass}

# 2. Initialize the agent
agent = AgentClass()

# 3. Use the agent's skills
result = agent.{skill_name}_skill(parameters)
```

## Agent Architecture

All agents follow the sub-agent pattern:
- Each agent is responsible for a specific domain
- Methods are suffixed with `_skill` to indicate they are invokable skills
- Agents are independent and can be used in isolation or composition
- Agents handle their own error cases gracefully

## Dependencies

Common dependencies across agents:
- **Rich**: UI rendering and formatting (ui, focus, analytics)
- **SpeechRecognition**: Voice input (voice)
- **dateparser**: Natural language date parsing (nlp)
- **JSON files**: Translation data (language)

## File Organization

```
.claude/skills/
├── README.md           # This file
├── ui.md              # UI Agent skill
├── nlp.md             # NLP Agent skill
├── voice.md           # Voice Agent skill
├── language.md        # Language Agent skill
├── gamification.md    # Gamification Agent skill
├── focus.md           # Focus Agent skill
└── analytics.md       # Analytics Agent skill
```

## Notes

- All skills are documented with examples and usage patterns
- Skills include error handling guidance
- Dependencies are clearly listed for each skill
- Skills can be composed to create complex workflows
- Each skill file includes "When to Use" sections for guidance
