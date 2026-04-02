"""Entry point for Smart Voice Assistant."""

from __future__ import annotations

import logging
import time

from command_handler import CommandHandler
from executor import Executor
from listener import Listener
from nlp_engine import NLPEngine
from speech_to_text import SpeechToText
from tts_engine import TTSEngine
from utils import append_history, setup_logging


def run_assistant() -> None:
    setup_logging()
    logger = logging.getLogger("Main")

    tts = TTSEngine()
    stt = SpeechToText()
    listener = Listener(stt=stt)
    nlp = NLPEngine()
    executor = Executor()
    command_handler = CommandHandler(executor=executor)

    logger.info("Smart Voice Assistant started. Waiting for wake word...")
    tts.speak("Assistant is online. Say hey assistant to begin.")

    while True:
        try:
            if not listener.wait_for_wake_word():
                time.sleep(0.15)
                continue

            tts.speak("I am listening")
            command_text = listener.listen_for_command()
            if not command_text:
                tts.speak("I could not hear a command clearly. Please try again.")
                continue

            parsed = nlp.parse(command_text)
            success, response = command_handler.handle(parsed)

            append_history(
                {
                    "heard_text": command_text,
                    "parsed": parsed,
                    "success": success,
                    "response": response,
                }
            )
            tts.speak(response)

        except KeyboardInterrupt:
            logger.info("Assistant stopped by user.")
            tts.speak("Goodbye")
            break
        except Exception as exc:
            logger.exception("Unhandled error in main loop: %s", exc)
            tts.speak("An unexpected error occurred. I will continue listening.")
            time.sleep(0.3)


if __name__ == "__main__":
    run_assistant()
