"""
LanguageAgent Sub-Agent for multi-language support.

This agent handles loading and managing translations for English, Urdu,
and Spanish using JSON-based internationalization files.
"""

import json
from pathlib import Path
from typing import Optional, Dict


class LanguageAgent:
    """
    Sub-Agent responsible for multi-language support.

    Loads translation files and provides translation lookup with
    fallback to English for missing keys.
    """

    SUPPORTED_LANGUAGES = ["en", "ur", "es"]
    DEFAULT_LANGUAGE = "en"

    def __init__(self, locales_dir: Optional[Path] = None):
        """
        Initialize LanguageAgent.

        Args:
            locales_dir: Path to locales directory (default: auto-detect)
        """
        if locales_dir is None:
            # Auto-detect locales directory
            current_file = Path(__file__)
            locales_dir = current_file.parent.parent / "locales"

        self.locales_dir = locales_dir
        self.current_language = self.DEFAULT_LANGUAGE
        self.translations: Dict[str, Dict[str, str]] = {}

        # Load all translation files
        self._load_all_translations()

    def _load_all_translations(self) -> None:
        """Load all available translation files."""
        for lang_code in self.SUPPORTED_LANGUAGES:
            self.load_language_skill(lang_code)

    def load_language_skill(self, language_code: str) -> bool:
        """
        Load translations for a specific language.

        Args:
            language_code: Language code (en, ur, es)

        Returns:
            True if loaded successfully, False otherwise
        """
        if language_code not in self.SUPPORTED_LANGUAGES:
            return False

        translation_file = self.locales_dir / f"{language_code}.json"

        try:
            if translation_file.exists():
                with open(translation_file, 'r', encoding='utf-8') as f:
                    self.translations[language_code] = json.load(f)
                return True
            else:
                # Create empty translation dict if file doesn't exist
                self.translations[language_code] = {}
                return False
        except Exception:
            self.translations[language_code] = {}
            return False

    def set_language_skill(self, language_code: str) -> bool:
        """
        Set the current active language.

        Args:
            language_code: Language code to activate (en, ur, es)

        Returns:
            True if language set successfully, False if unsupported
        """
        if language_code not in self.SUPPORTED_LANGUAGES:
            return False

        # Ensure language is loaded
        if language_code not in self.translations:
            self.load_language_skill(language_code)

        self.current_language = language_code
        return True

    def translate_skill(self, key: str, language: Optional[str] = None) -> str:
        """
        Get translation for a key.

        Uses dot notation for nested keys (e.g., "menu.title").
        Falls back to English if translation not found, then to the key itself.

        Args:
            key: Translation key (supports dot notation)
            language: Language code (default: current language)

        Returns:
            Translated text or key if translation not found

        Example:
            >>> lang_agent.translate_skill("menu.add_task")
            "Add New Task"
        """
        lang_code = language or self.current_language

        # Get translation dictionary for language
        translations = self.translations.get(lang_code, {})

        # Handle dot notation (e.g., "menu.add_task")
        value = self._get_nested_value(translations, key)

        if value is not None:
            return value

        # Fallback to English if not current language
        if lang_code != self.DEFAULT_LANGUAGE:
            english_translations = self.translations.get(self.DEFAULT_LANGUAGE, {})
            value = self._get_nested_value(english_translations, key)
            if value is not None:
                return value

        # Fallback to key itself
        return key

    def _get_nested_value(self, dictionary: Dict, key: str) -> Optional[str]:
        """
        Get nested dictionary value using dot notation.

        Args:
            dictionary: Dictionary to search
            key: Dot-notation key (e.g., "menu.add_task")

        Returns:
            Value if found, None otherwise
        """
        keys = key.split('.')
        value = dictionary

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return None

        return value if isinstance(value, str) else None

    def get_current_language_skill(self) -> str:
        """
        Get the current active language code.

        Returns:
            Current language code (en, ur, es)
        """
        return self.current_language

    def get_language_name_skill(self, language_code: Optional[str] = None) -> str:
        """
        Get the display name for a language.

        Args:
            language_code: Language code (default: current language)

        Returns:
            Language display name
        """
        lang_code = language_code or self.current_language

        language_names = {
            "en": "English",
            "ur": "اردو (Urdu)",
            "es": "Español (Spanish)"
        }

        return language_names.get(lang_code, lang_code)

    def get_supported_languages_skill(self) -> list[Dict[str, str]]:
        """
        Get list of supported languages with metadata.

        Returns:
            List of dicts with 'code' and 'name' keys
        """
        return [
            {"code": lang, "name": self.get_language_name_skill(lang)}
            for lang in self.SUPPORTED_LANGUAGES
        ]

    def is_rtl_skill(self, language_code: Optional[str] = None) -> bool:
        """
        Check if language uses right-to-left text direction.

        Args:
            language_code: Language code (default: current language)

        Returns:
            True if RTL language (Urdu), False otherwise
        """
        lang_code = language_code or self.current_language
        rtl_languages = ["ur", "ar", "he"]  # Urdu, Arabic, Hebrew
        return lang_code in rtl_languages
