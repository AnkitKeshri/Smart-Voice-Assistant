"""Text-to-speech engine wrapper."""

from __future__ import annotations

import logging
import threading

import pyttsx3


class TTSEngine:
    """Simple, thread-safe TTS engine."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._lock = threading.Lock()
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 175)

    def speak(self, message: str) -> None:
        """Speak a message without crashing caller on TTS errors."""
        if not message:
            return
        self.logger.info("Assistant: %s", message)
        try:
            with self._lock:
                self.engine.say(message)
                self.engine.runAndWait()
        except Exception as exc:
            self.logger.error("TTS error: %s", exc)
