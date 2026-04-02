"""Microphone listener and wake-word detection."""

from __future__ import annotations

import logging
from typing import Optional

import speech_recognition as sr

from config import AMBIENT_NOISE_DURATION, LISTEN_TIMEOUT, PHRASE_TIME_LIMIT, WAKE_WORDS
from speech_to_text import SpeechToText


class Listener:
    """Listens for wake words and command audio."""

    def __init__(self, stt: SpeechToText) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.stt = stt
        self.recognizer = stt.recognizer

    def _capture_audio(self, timeout: int = LISTEN_TIMEOUT) -> Optional[sr.AudioData]:
        """Capture one microphone phrase and return raw audio."""
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=AMBIENT_NOISE_DURATION)
                self.logger.debug("Listening...")
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=PHRASE_TIME_LIMIT)
                return audio
        except sr.WaitTimeoutError:
            self.logger.debug("Listen timeout waiting for speech")
        except OSError as exc:
            self.logger.error("Microphone not available: %s", exc)
        except Exception as exc:
            self.logger.error("Unexpected microphone error: %s", exc)
        return None

    def wait_for_wake_word(self) -> bool:
        """Block until wake word is detected or continue loop on failure."""
        audio = self._capture_audio(timeout=LISTEN_TIMEOUT)
        if not audio:
            return False

        text = self.stt.transcribe(audio)
        if not text:
            return False

        self.logger.info("Heard (wake check): %s", text)
        return any(wake in text for wake in WAKE_WORDS)

    def listen_for_command(self) -> Optional[str]:
        """Capture user command after wake word detection."""
        audio = self._capture_audio(timeout=LISTEN_TIMEOUT)
        if not audio:
            return None

        command = self.stt.transcribe(audio)
        if command:
            self.logger.info("Heard command: %s", command)
        return command
