"""Rule-based NLP engine for intent and entity extraction."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Dict, Optional


@dataclass
class ParsedCommand:
    intent: str
    entity: Optional[str] = None
    raw_text: str = ""


class NLPEngine:
    """Modular NLP parser ready for future ML integration."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)

    def parse(self, text: str) -> Dict[str, Optional[str]]:
        """Parse raw text into structured command dictionary."""
        cleaned = " ".join((text or "").strip().lower().split())
        result = ParsedCommand(intent="unknown", entity=None, raw_text=cleaned)

        if not cleaned:
            return result.__dict__

        # App control
        open_match = re.match(r"^(open|start|launch)\s+(.+)$", cleaned)
        if open_match:
            target = open_match.group(2)
            if target in {"youtube", "google", "gmail"}:
                result.intent = "open_website"
            else:
                result.intent = "open_app"
            result.entity = target
            return result.__dict__

        close_match = re.match(r"^(close|exit|quit|stop)\s+(.+)$", cleaned)
        if close_match:
            result.intent = "close_app"
            result.entity = close_match.group(2)
            return result.__dict__

        # Folder operations
        create_folder_match = re.match(r"^(create|make)\s+(folder|directory)\s+(.+)$", cleaned)
        if create_folder_match:
            result.intent = "create_folder"
            result.entity = create_folder_match.group(3)
            return result.__dict__

        delete_folder_match = re.match(r"^(delete|remove)\s+(folder|directory)\s+(.+)$", cleaned)
        if delete_folder_match:
            result.intent = "delete_folder"
            result.entity = delete_folder_match.group(3)
            return result.__dict__

        # System
        if any(k in cleaned for k in ["shutdown", "power off"]):
            result.intent = "shutdown_system"
            return result.__dict__

        if any(k in cleaned for k in ["restart", "reboot"]):
            result.intent = "restart_system"
            return result.__dict__

        # Informational
        if "time" in cleaned:
            result.intent = "get_time"
            return result.__dict__

        if cleaned in {"help", "what can you do", "show commands"}:
            result.intent = "help"
            return result.__dict__

        self.logger.debug("Unknown command pattern: %s", cleaned)
        return result.__dict__
