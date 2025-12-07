"""
NLPAgent Sub-Agent for natural language processing.

This agent parses natural language input to extract task components like
dates, priorities, and titles using dateparser and keyword matching.
"""

from datetime import datetime
from typing import Optional, Dict, Any
import re

try:
    import dateparser
    DATEPARSER_AVAILABLE = True
except ImportError:
    DATEPARSER_AVAILABLE = False

from todo_app.models.task import Priority


class NLPAgent:
    """
    Sub-Agent responsible for natural language processing.

    Parses natural language input to extract structured task information
    including dates, priorities, and cleaned titles.
    """

    def __init__(self):
        """Initialize NLPAgent with priority keywords."""
        self.priority_keywords = {
            Priority.HIGH: [
                "urgent", "important", "critical", "asap", "high priority",
                "crucial", "vital", "emergency", "top priority"
            ],
            Priority.LOW: [
                "low priority", "minor", "someday", "maybe", "optional",
                "nice to have", "when possible"
            ],
            Priority.MEDIUM: [
                "medium", "normal", "regular", "standard"
            ]
        }

    def parse_natural_language_skill(self, text: str) -> Dict[str, Any]:
        """
        Parse natural language text into structured task components.

        Extracts:
        - Due date from date expressions
        - Priority from keywords
        - Clean title (with date/priority keywords removed)

        Args:
            text: Natural language task description

        Returns:
            Dictionary with keys:
            - title: Cleaned task title
            - due_date: Parsed datetime or None
            - priority: Detected Priority enum or None
            - original_text: Original input text

        Examples:
            >>> nlp.parse_natural_language_skill("Buy groceries tomorrow high priority")
            {
                'title': 'Buy groceries',
                'due_date': datetime(...),  # tomorrow's date
                'priority': Priority.HIGH,
                'original_text': 'Buy groceries tomorrow high priority'
            }
        """
        if not text or not text.strip():
            return {
                'title': '',
                'due_date': None,
                'priority': None,
                'original_text': text
            }

        result = {
            'title': text.strip(),
            'due_date': None,
            'priority': None,
            'original_text': text
        }

        # Extract priority
        priority = self._extract_priority_skill(text)
        if priority:
            result['priority'] = priority
            # Remove priority keywords from text
            text = self._remove_priority_keywords_skill(text)

        # Extract due date
        if DATEPARSER_AVAILABLE:
            due_date = self._extract_date_skill(text)
            if due_date:
                result['due_date'] = due_date
                # Remove date expression from text
                text = self._remove_date_expressions_skill(text)

        # Clean up title
        result['title'] = text.strip()

        return result

    def _extract_priority_skill(self, text: str) -> Optional[Priority]:
        """
        Extract priority from text based on keyword matching.

        Priority detection order: HIGH > LOW > MEDIUM (default if no match)

        Args:
            text: Text to analyze

        Returns:
            Priority enum if keyword found, None otherwise
        """
        text_lower = text.lower()

        # Check HIGH priority keywords first (most specific)
        for keyword in self.priority_keywords[Priority.HIGH]:
            if keyword in text_lower:
                return Priority.HIGH

        # Check LOW priority keywords
        for keyword in self.priority_keywords[Priority.LOW]:
            if keyword in text_lower:
                return Priority.LOW

        # Check MEDIUM priority keywords
        for keyword in self.priority_keywords[Priority.MEDIUM]:
            if keyword in text_lower:
                return Priority.MEDIUM

        return None

    def _extract_date_skill(self, text: str) -> Optional[datetime]:
        """
        Extract date from natural language text using dateparser.

        Args:
            text: Text containing date expression

        Returns:
            Parsed datetime or None if no date found

        Examples:
            - "tomorrow" -> tomorrow's date
            - "next Friday" -> date of next Friday
            - "in 3 days" -> date 3 days from now
            - "2025-12-31" -> December 31, 2025
        """
        if not DATEPARSER_AVAILABLE:
            return None

        # Configure dateparser settings
        settings = {
            'PREFER_DATES_FROM': 'future',  # Prefer future dates
            'RELATIVE_BASE': datetime.now(),
            'RETURN_AS_TIMEZONE_AWARE': False
        }

        try:
            parsed_date = dateparser.parse(text, settings=settings)
            return parsed_date
        except Exception:
            return None

    def _remove_priority_keywords_skill(self, text: str) -> str:
        """
        Remove priority keywords from text.

        Args:
            text: Text containing priority keywords

        Returns:
            Text with priority keywords removed
        """
        result = text
        text_lower = text.lower()

        # Find and remove priority keywords (case-insensitive)
        for priority_level in self.priority_keywords.values():
            for keyword in priority_level:
                # Create case-insensitive regex pattern
                pattern = re.compile(re.escape(keyword), re.IGNORECASE)
                result = pattern.sub('', result)

        return result.strip()

    def _remove_date_expressions_skill(self, text: str) -> str:
        """
        Remove common date expressions from text.

        Args:
            text: Text containing date expressions

        Returns:
            Text with date expressions removed
        """
        # Common date expression patterns
        date_patterns = [
            r'\btomorrow\b',
            r'\btoday\b',
            r'\byesterday\b',
            r'\bnext\s+\w+\b',  # next week, next Monday, etc.
            r'\blast\s+\w+\b',  # last week, last Monday, etc.
            r'\bin\s+\d+\s+(day|days|week|weeks|month|months)\b',
            r'\b\d{4}-\d{2}-\d{2}\b',  # ISO date format
            r'\b\d{1,2}/\d{1,2}/\d{4}\b',  # MM/DD/YYYY
            r'\b\d{1,2}-\d{1,2}-\d{4}\b',  # MM-DD-YYYY
        ]

        result = text
        for pattern in date_patterns:
            result = re.sub(pattern, '', result, flags=re.IGNORECASE)

        return result.strip()

    def extract_tags_from_text_skill(self, text: str) -> list[str]:
        """
        Extract hashtags from text.

        Args:
            text: Text containing hashtags (e.g., "Task #work #urgent")

        Returns:
            List of extracted tags (without # symbol)

        Example:
            >>> nlp.extract_tags_from_text_skill("Meeting #work #team #important")
            ['work', 'team', 'important']
        """
        # Find all hashtags in text
        hashtags = re.findall(r'#(\w+)', text)
        return hashtags

    def remove_tags_from_text_skill(self, text: str) -> str:
        """
        Remove hashtags from text.

        Args:
            text: Text containing hashtags

        Returns:
            Text with hashtags removed

        Example:
            >>> nlp.remove_tags_from_text_skill("Meeting #work #team")
            'Meeting'
        """
        result = re.sub(r'#\w+', '', text)
        return result.strip()
