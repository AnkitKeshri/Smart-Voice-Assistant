"""Speech-to-text processing with offline-first behavior."""

from __future__ import annotations

import logging
from typing import Optional

import speech_recognition as sr

from config import ENABLE_GOOGLE_FALLBACK


class SpeechToText:
    """Convert microphone audio to text."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.recognizer = sr.Recognizer()

    def transcribe(self, audio: sr.AudioData) -> Optional[str]:
        """Transcribe audio to text.

        Offline-first using Sphinx. Optionally fallback to Google recognizer.
        """
        try:
            text = self.recognizer.recognize_sphinx(audio)
            cleaned = text.strip().lower()
            if cleaned:
                return cleaned
        except sr.UnknownValueError:
            self.logger.info("Offline STT could not understand audio")
        except sr.RequestError as exc:
            self.logger.warning("Offline STT engine issue: %s", exc)
        except Exception as exc:
            self.logger.error("Unexpected offline STT error: %s", exc)

        if ENABLE_GOOGLE_FALLBACK:
            try:
                text = self.recognizer.recognize_google(audio)
                cleaned = text.strip().lower()
                if cleaned:
                    return cleaned
            except sr.UnknownValueError:
                self.logger.info("Google STT could not understand audio")
            except sr.RequestError as exc:
                self.logger.warning("Google STT service issue: %s", exc)
            except Exception as exc:
                self.logger.error("Unexpected Google STT error: %s", exc)

        return None
