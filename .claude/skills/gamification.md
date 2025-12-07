# Gamification Agent Skill

Manage experience points, streaks, and achievement badges for user motivation.

## Purpose
This skill provides access to the GamificationAgent sub-agent which handles the gamification system including XP calculation, daily streak tracking, and badge awards based on task completion patterns.

## Usage

When you need to calculate XP, track streaks, or award badges, invoke the GamificationAgent's methods.

### Available Skills

#### Calculate XP for Task Completion
```python
from todo_app.agents.gamification_agent import GamificationAgent
from todo_app.models.user_profile import UserProfile

profile = UserProfile()
gamification = GamificationAgent(profile)

xp = gamification.calculate_xp_for_completion_skill(task)
# Returns: 10 (base) + 25 (if before due) + 15 (if before 8am)
```

#### Process Task Completion
```python
result = gamification.process_task_completion_skill(task)
# Returns: {
#     'xp_earned': 35,
#     'new_badges': ['early_bird'],
#     'current_streak': 7,
#     'total_xp': 350
# }
```

#### Get Statistics
```python
stats = gamification.get_statistics_skill()
# Returns: {
#     'total_xp': 350,
#     'current_streak': 7,
#     'longest_streak': 14,
#     'total_completions': 25,
#     'badges_earned': 3,
#     'badge_list': ['early_bird', 'streak_7', 'task_master_10']
# }
```

#### Get Badge Information
```python
badge_info = gamification.get_badge_info_skill("early_bird")
# Returns: {
#     'name': '🌅 Early Bird',
#     'description': 'Complete a task before 8 AM'
# }
```

#### Get All Badges
```python
all_badges = gamification.get_all_badges_skill()
# Returns: Dictionary of all available badges
```

#### Get Earned Badges with Details
```python
earned = gamification.get_earned_badges_with_info_skill()
# Returns: [
#     {
#         'key': 'early_bird',
#         'name': '🌅 Early Bird',
#         'description': 'Complete a task before 8 AM'
#     }
# ]
```

## XP System

### Base XP Awards
- **Base completion**: 10 XP
- **Before due date bonus**: +25 XP
- **Early morning bonus** (before 8 AM): +15 XP

### Maximum XP per Task
A task completed before due date AND before 8 AM earns: 10 + 25 + 15 = **50 XP**

## Streak System

### Streak Rules
- Increment by 1 for each consecutive day with at least one completed task
- Reset to 0 if a day passes with no completions
- Same-day completions don't change streak
- Longest streak is tracked separately

## Badge System

### Available Badges

1. **🌅 Early Bird**
   - Complete a task before 8 AM

2. **🔥 Week Warrior**
   - Maintain a 7-day streak

3. **🏆 Month Master**
   - Maintain a 30-day streak

4. **⭐ Task Master**
   - Complete 10 tasks

5. **💎 Task Legend**
   - Complete 50 tasks

6. **👑 Task Champion**
   - Complete 100 tasks

7. **💯 Perfect Score**
   - Complete a task before due date AND before 8 AM

## When to Use

- When a task is marked as complete (process completion)
- When displaying user statistics or progress
- When showing available or earned badges
- When calculating rewards for task completion
- When tracking daily streaks and motivation

## Dependencies

- todo_app.models.user_profile module (for UserProfile)
- todo_app.models.task module (for Task model)

## Notes

- Badges are awarded automatically during task completion processing
- Each badge can only be earned once
- Streak tracking uses completion date, not completion time
- XP bonuses are cumulative (can earn multiple bonuses for one task)
- User profile must be provided or will create a new default profile
