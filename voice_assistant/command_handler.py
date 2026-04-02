"""Command validation and routing module."""

from __future__ import annotations

import logging
import shlex
import subprocess
from typing import Dict, Optional, Tuple

from config import CUSTOM_COMMANDS_FILE
from executor import Executor
from utils import safe_load_json


class CommandHandler:
    """Validate parsed commands and dispatch to executor methods."""

    def __init__(self, executor: Executor) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.executor = executor
        self.custom_commands = self._load_custom_commands()

    def _load_custom_commands(self) -> Dict[str, str]:
        data = safe_load_json(CUSTOM_COMMANDS_FILE, default={})
        if isinstance(data, dict):
            return {str(k).strip().lower(): str(v) for k, v in data.items()}
        return {}

    @staticmethod
    def _validate_entity(entity: Optional[str]) -> bool:
        return bool(entity and entity.strip())

    def _run_custom_command(self, text: str) -> Tuple[bool, str]:
        shell_cmd = self.custom_commands.get(text.strip().lower())
        if not shell_cmd:
            return False, "No custom command match"
        try:
            subprocess.Popen(shlex.split(shell_cmd))
            return True, "Custom command executed"
        except Exception as exc:
            return False, f"Custom command failed: {exc}"

    def handle(self, parsed: Dict[str, Optional[str]]) -> Tuple[bool, str]:
        intent = (parsed.get("intent") or "unknown").strip().lower()
        entity = parsed.get("entity")
        raw_text = (parsed.get("raw_text") or "").strip().lower()

        if raw_text:
            custom_ok, custom_msg = self._run_custom_command(raw_text)
            if custom_ok:
                return True, custom_msg

        if intent == "open_app":
            if not self._validate_entity(entity):
                return False, "Please tell me which app to open"
            return self.executor.open_app(entity or "")

        if intent == "close_app":
            if not self._validate_entity(entity):
                return False, "Please tell me which app to close"
            return self.executor.close_app(entity or "")

        if intent == "create_folder":
            if not self._validate_entity(entity):
                return False, "Please provide a folder name"
            return self.executor.create_folder(entity or "")

        if intent == "delete_folder":
            if not self._validate_entity(entity):
                return False, "Please provide a folder name"
            return self.executor.delete_folder(entity or "")

        if intent == "shutdown_system":
            return self.executor.shutdown_system()

        if intent == "restart_system":
            return self.executor.restart_system()

        if intent == "open_website":
            if not self._validate_entity(entity):
                return False, "Please provide website name"
            return self.executor.open_website(entity or "")

        if intent == "get_time":
            return self.executor.get_time()

        if intent == "help":
            return (
                True,
                "I can open or close apps, create or delete folders, open websites, tell time, and run custom commands.",
            )

        return False, "Sorry, I did not understand that command"
