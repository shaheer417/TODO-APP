# Analytics Agent Skill

Generate productivity metrics, insights, and visualizations for task completion patterns.

## Purpose
This skill provides access to the AnalyticsAgent sub-agent which analyzes task data to provide comprehensive productivity metrics, statistics, and CLI-based charts for completion patterns and insights.

## Usage

When you need to analyze productivity data or generate reports, invoke the AnalyticsAgent's methods.

### Available Skills

#### Calculate Comprehensive Metrics
```python
from todo_app.agents.analytics_agent import AnalyticsAgent

analytics = AnalyticsAgent()
metrics = analytics.calculate_metrics_skill(tasks)
# Returns: {
#     'tasks_today': 3,
#     'tasks_this_week': 15,
#     'overdue_count': 2,
#     'completion_rate': 75.0,
#     'avg_completion_time': 24.5,  # hours
#     'most_productive_day': 'Monday',
#     'most_productive_hour': 14  # 2 PM
# }
```

#### Generate Weekly Chart
```python
chart = analytics.generate_weekly_chart_skill(tasks)
# Returns: ASCII bar chart string showing completions for last 7 days
```

#### Get Priority Distribution
```python
distribution = analytics.get_priority_distribution_skill(tasks)
# Returns: {
#     'high': 5,
#     'medium': 10,
#     'low': 3
# }
```

#### Get Tag Statistics
```python
tag_stats = analytics.get_tag_statistics_skill(tasks)
# Returns: [
#     {
#         'tag': 'work',
#         'total': 15,
#         'completed': 10,
#         'pending': 5,
#         'completion_rate': 66.7
#     }
# ]
```

#### Display Analytics Dashboard
```python
analytics.display_analytics_dashboard_skill(tasks)
# Displays comprehensive dashboard in terminal
```

#### Get Completion Trend
```python
trend = analytics.get_completion_trend_skill(tasks, days=30)
# Returns: [
#     {'date': '2025-11-07', 'count': 3},
#     {'date': '2025-11-08', 'count': 5},
#     ...
# ]
```

#### Get Performance Insights
```python
insights = analytics.get_performance_insights_skill(tasks)
# Returns: [
#     "🎉 Excellent! You're completing most of your tasks.",
#     "🌅 You're most productive in the morning!",
#     "🔥 Amazing! You've completed 5 tasks today!"
# ]
```

## Metrics Explained

### Completion Rate
Percentage of tasks that are completed:
```
completion_rate = (completed_tasks / total_tasks) * 100
```

### Average Completion Time
Average time (in hours) from task creation to completion:
```
avg_completion_time = total_completion_time / number_of_completed_tasks
```

### Most Productive Day
Day of the week with the highest number of task completions.

### Most Productive Hour
Hour of the day (0-23) with the highest number of task completions.

## Chart Visualization

The weekly chart displays:
- Last 7 days of completion data
- Bar length proportional to completion count
- Color coding:
  - **Green**: High completion day (≥70% of max)
  - **Yellow**: Medium completion day (40-70% of max)
  - **Red**: Low completion day (<40% of max)
  - **Dim**: No completions

Example output:
```
📊 Weekly Completion Chart (Last 7 Days)
==================================================
Mon 12/01: ████████████████████ (8)
Tue 12/02: ██████████████ (6)
Wed 12/03: ████████████████████████████ (12)
Thu 12/04: ███████ (3)
Fri 12/05: ████████████ (5)
Sat 12/06: ██ (1)
Sun 12/07: ░░░ (0)
==================================================
```

## Performance Insights

The analytics agent generates contextual insights:

### Completion Rate Insights
- ≥80%: "Excellent! You're completing most of your tasks."
- 50-79%: "Good progress! Try to complete more pending tasks."
- <50%: "Keep going! Focus on completing your pending tasks."

### Overdue Insights
- If overdue tasks exist: "You have X overdue task(s). Prioritize these!"

### Productivity Pattern Insights
- Morning productive (hour < 12): "You're most productive in the morning!"
- Afternoon productive (hour 12-17): "You're most productive in the afternoon!"
- Evening productive (hour > 17): "You're most productive in the evening!"

### Daily Performance
- 0 tasks today: "No tasks completed today yet. Start now!"
- ≥5 tasks today: "Amazing! You've completed X tasks today!"

## Dashboard Display

The dashboard includes:
- Tasks completed today
- Tasks completed this week
- Overdue tasks count (highlighted in red if > 0)
- Completion rate percentage
- Average completion time
- Most productive day
- Most productive hour (in 12-hour format with AM/PM)
- Weekly completion chart

## When to Use

- When displaying productivity statistics to users
- When generating weekly/monthly reports
- When identifying productivity patterns
- When providing actionable insights for improvement
- When visualizing task completion trends
- When analyzing tag usage and effectiveness

## Dependencies

- Rich library (for formatted dashboard display)
- todo_app.models.task module (for Task and Status models)

## Notes

- All metrics are calculated from provided task list
- Chart scaling is automatic based on maximum daily count
- Tag statistics are sorted by total usage (descending)
- Completion trend supports customizable day ranges
- Dashboard requires Rich library for formatted output
- All time calculations use task creation and completion timestamps
- Hour display in dashboard uses 12-hour format for readability
