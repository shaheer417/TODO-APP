"""
VoiceAgent Sub-Agent for speech-to-text conversion.

This agent handles voice input using SpeechRecognition library with
Google Speech API (primary) and CMU Sphinx (offline fallback).
"""

from typing import Optional

try:
    import speech_recognition as sr
    SPEECH_RECOGNITION_AVAILABLE = True
except ImportError:
    SPEECH_RECOGNITION_AVAILABLE = False


class VoiceAgent:
    """
    Sub-Agent responsible for voice input and speech-to-text conversion.

    Uses Google Speech API as primary backend with CMU Sphinx as
    offline fallback for privacy/reliability.
    """

    def __init__(self):
        """Initialize VoiceAgent with speech recognizer."""
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            self.microphone_available = self._check_microphone_available()
        else:
            self.recognizer = None
            self.microphone_available = False

    def _check_microphone_available(self) -> bool:
        """
        Check if a microphone is available.

        Returns:
            True if microphone detected, False otherwise
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            return False

        try:
            # Try to list available microphones
            microphone_list = sr.Microphone.list_microphone_names()
            return len(microphone_list) > 0
        except Exception:
            return False

    def listen_and_transcribe_skill(
        self,
        timeout: int = 5,
        phrase_time_limit: int = 10,
        use_google: bool = True
    ) -> Optional[str]:
        """
        Listen to microphone and transcribe speech to text.

        Args:
            timeout: Maximum seconds to wait for speech to start (default: 5)
            phrase_time_limit: Maximum seconds for a phrase (default: 10)
            use_google: Use Google API if True, Sphinx if False (default: True)

        Returns:
            Transcribed text or None if recognition failed

        Raises:
            RuntimeError: If SpeechRecognition library not installed
            RuntimeError: If no microphone available

        Example:
            >>> voice_agent = VoiceAgent()
            >>> text = voice_agent.listen_and_transcribe_skill()
            Listening... Speak now!
            >>> print(text)
            "Buy groceries tomorrow"
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            raise RuntimeError(
                "SpeechRecognition library not installed. "
                "Install with: pip install SpeechRecognition"
            )

        if not self.microphone_available:
            raise RuntimeError(
                "No microphone detected. Please connect a microphone and try again."
            )

        try:
            with sr.Microphone() as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)

                # Listen for audio
                audio = self.recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )

            # Transcribe audio
            if use_google:
                text = self._transcribe_with_google_skill(audio)
                if text:
                    return text
                # Fall back to Sphinx if Google fails
                return self._transcribe_with_sphinx_skill(audio)
            else:
                return self._transcribe_with_sphinx_skill(audio)

        except sr.WaitTimeoutError:
            return None  # No speech detected within timeout
        except Exception:
            return None  # Other errors (no audio, etc.)

    def _transcribe_with_google_skill(self, audio) -> Optional[str]:
        """
        Transcribe audio using Google Speech API.

        Args:
            audio: Audio data from speech_recognition

        Returns:
            Transcribed text or None if recognition failed
        """
        try:
            text = self.recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return None  # Speech unintelligible
        except sr.RequestError:
            return None  # API unavailable

    def _transcribe_with_sphinx_skill(self, audio) -> Optional[str]:
        """
        Transcribe audio using CMU Sphinx (offline).

        Args:
            audio: Audio data from speech_recognition

        Returns:
            Transcribed text or None if recognition failed
        """
        try:
            text = self.recognizer.recognize_sphinx(audio)
            return text
        except sr.UnknownValueError:
            return None  # Speech unintelligible
        except sr.RequestError:
            return None  # Sphinx not available

    def is_available_skill(self) -> bool:
        """
        Check if voice input is available.

        Returns:
            True if SpeechRecognition installed and microphone detected
        """
        return SPEECH_RECOGNITION_AVAILABLE and self.microphone_available

    def get_status_message_skill(self) -> str:
        """
        Get a status message about voice input availability.

        Returns:
            Human-readable status message
        """
        if not SPEECH_RECOGNITION_AVAILABLE:
            return (
                "❌ Voice input unavailable: SpeechRecognition not installed.\n"
                "   Install with: pip install SpeechRecognition PyAudio"
            )

        if not self.microphone_available:
            return (
                "❌ Voice input unavailable: No microphone detected.\n"
                "   Please connect a microphone and restart the application."
            )

        return "✅ Voice input ready. Microphone detected."

    def test_microphone_skill(self) -> bool:
        """
        Test microphone by recording a short sample.

        Returns:
            True if test successful, False otherwise
        """
        if not self.is_available_skill():
            return False

        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
                # Record 1 second of audio
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=1)
            return True
        except Exception:
            return False
