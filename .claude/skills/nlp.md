# NLP Agent Skill

Parse natural language input to extract task components like dates, priorities, and titles.

## Purpose
This skill provides access to the NLPAgent sub-agent which handles natural language processing to parse user input and extract structured task information including due dates, priorities, tags, and cleaned titles.

## Usage

When you need to parse natural language task descriptions, invoke the NLPAgent's methods.

### Available Skills

#### Parse Natural Language Input
```python
from todo_app.agents.nlp_agent import NLPAgent

nlp = NLPAgent()
result = nlp.parse_natural_language_skill("Buy groceries tomorrow high priority")
# Returns: {
#     'title': 'Buy groceries',
#     'due_date': datetime(...),  # tomorrow's date
#     'priority': Priority.HIGH,
#     'original_text': 'Buy groceries tomorrow high priority'
# }
```

#### Extract Tags from Text
```python
tags = nlp.extract_tags_from_text_skill("Meeting #work #team #important")
# Returns: ['work', 'team', 'important']
```

#### Remove Tags from Text
```python
clean_text = nlp.remove_tags_from_text_skill("Meeting #work #team")
# Returns: 'Meeting'
```

## Priority Keywords

The NLP agent recognizes the following priority keywords:

- **High Priority**: urgent, important, critical, asap, high priority, crucial, vital, emergency, top priority
- **Low Priority**: low priority, minor, someday, maybe, optional, nice to have, when possible
- **Medium Priority**: medium, normal, regular, standard

## Date Expression Examples

The NLP agent can parse various date expressions:

- "tomorrow" → tomorrow's date
- "next Friday" → date of next Friday
- "in 3 days" → date 3 days from now
- "2025-12-31" → December 31, 2025
- "this weekend" → upcoming Saturday

## When to Use

- When processing natural language task input from users
- When extracting structured data from free-form text
- When identifying priority levels from keywords
- When parsing due dates from relative expressions
- When extracting hashtags from task descriptions

## Dependencies

- dateparser library (optional, for date parsing - degrades gracefully if not available)
- todo_app.models.task module (for Priority enum)

## Notes

- If dateparser is not available, date extraction will return None
- Priority detection defaults to None if no keywords are found
- Text is cleaned by removing extracted priority keywords and date expressions
- All parsing is case-insensitive
