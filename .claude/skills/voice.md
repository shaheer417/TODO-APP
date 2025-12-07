# Voice Agent Skill

Convert speech to text for hands-free task creation.

## Purpose
This skill provides access to the VoiceAgent sub-agent which handles voice input using speech recognition with Google Speech API (primary) and CMU Sphinx (offline fallback).

## Usage

When you need to capture voice input from users, invoke the VoiceAgent's methods.

### Available Skills

#### Listen and Transcribe
```python
from todo_app.agents.voice_agent import VoiceAgent

voice = VoiceAgent()
text = voice.listen_and_transcribe_skill(timeout=5, phrase_time_limit=10, use_google=True)
# Returns: "Buy groceries tomorrow" or None if recognition failed
```

#### Check Availability
```python
is_available = voice.is_available_skill()
# Returns: True if SpeechRecognition installed and microphone detected
```

#### Get Status Message
```python
status = voice.get_status_message_skill()
# Returns: Human-readable status about voice input availability
```

#### Test Microphone
```python
test_passed = voice.test_microphone_skill()
# Returns: True if microphone test successful, False otherwise
```

## Parameters

### listen_and_transcribe_skill

- **timeout** (int): Maximum seconds to wait for speech to start (default: 5)
- **phrase_time_limit** (int): Maximum seconds for a phrase (default: 10)
- **use_google** (bool): Use Google API if True, Sphinx if False (default: True)

## When to Use

- When implementing hands-free task creation
- When providing accessibility features for users who cannot type
- When enabling task capture while multitasking
- When the user explicitly requests voice input mode

## Error Handling

The voice agent handles errors gracefully:

- Returns None if no speech detected within timeout
- Returns None if speech is unintelligible
- Falls back to Sphinx if Google API fails
- Raises RuntimeError if SpeechRecognition library not installed
- Raises RuntimeError if no microphone available

## Dependencies

- SpeechRecognition library (required, install with: pip install SpeechRecognition)
- PyAudio library (required for microphone access, install with: pip install PyAudio)
- Internet connection (for Google Speech API, optional with Sphinx fallback)

## Notes

- Google Speech API provides better accuracy but requires internet
- CMU Sphinx works offline but has lower accuracy
- Microphone availability is checked during initialization
- Ambient noise adjustment is performed automatically before listening
- The agent adjusts for ambient noise for 0.5 seconds before listening
