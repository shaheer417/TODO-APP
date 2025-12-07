# Language Agent Skill

Provide multi-language support for the Todo application UI.

## Purpose
This skill provides access to the LanguageAgent sub-agent which handles internationalization (i18n) by loading and managing translations for English, Urdu, and Spanish using JSON-based language files.

## Usage

When you need to display translated UI text or manage language settings, invoke the LanguageAgent's methods.

### Available Skills

#### Load Language
```python
from todo_app.agents.language_agent import LanguageAgent

lang = LanguageAgent()
success = lang.load_language_skill("ur")  # Load Urdu translations
# Returns: True if loaded successfully, False otherwise
```

#### Set Active Language
```python
success = lang.set_language_skill("es")  # Switch to Spanish
# Returns: True if language set successfully, False if unsupported
```

#### Translate Text
```python
translated = lang.translate_skill("menu.add_task")
# Returns: "Add New Task" (English) or translated equivalent
```

#### Translate with Specific Language
```python
translated = lang.translate_skill("menu.add_task", language="ur")
# Returns: Translation in Urdu
```

#### Get Current Language
```python
current = lang.get_current_language_skill()
# Returns: "en", "ur", or "es"
```

#### Get Language Display Name
```python
name = lang.get_language_name_skill()
# Returns: "English", "اردو (Urdu)", or "Español (Spanish)"
```

#### Get Supported Languages
```python
languages = lang.get_supported_languages_skill()
# Returns: [
#     {"code": "en", "name": "English"},
#     {"code": "ur", "name": "اردو (Urdu)"},
#     {"code": "es", "name": "Español (Spanish)"}
# ]
```

#### Check if Right-to-Left
```python
is_rtl = lang.is_rtl_skill()
# Returns: True for Urdu/Arabic/Hebrew, False otherwise
```

## Supported Languages

- **en**: English (default)
- **ur**: اردو (Urdu) - RTL language
- **es**: Español (Spanish)

## Translation File Structure

Translation files are stored in JSON format at `todo_app/locales/`:

```json
{
  "menu": {
    "title": "Main Menu",
    "add_task": "Add New Task",
    "view_tasks": "View All Tasks"
  },
  "messages": {
    "success": "Operation successful",
    "error": "An error occurred"
  }
}
```

## Translation Key Format

Use dot notation for nested keys:
- `menu.add_task` → accesses `menu.add_task` in JSON
- `messages.success` → accesses `messages.success` in JSON

## Fallback Behavior

- If a translation is not found in the current language, falls back to English
- If not found in English, returns the key itself
- Missing translation files create empty translation dictionaries

## When to Use

- When displaying any UI text (menus, prompts, messages)
- When changing the application language based on user preference
- When checking language capabilities (RTL support)
- When listing available language options to users

## Dependencies

- JSON files in `todo_app/locales/` directory:
  - `en.json` (English)
  - `ur.json` (Urdu)
  - `es.json` (Spanish)

## Notes

- All translation files are loaded during initialization
- Language switching happens instantly without restart
- RTL languages (like Urdu) may require terminal RTL support for proper rendering
- Missing translation files will not cause errors but will return keys as-is
