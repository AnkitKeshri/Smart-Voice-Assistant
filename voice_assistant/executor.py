"""System command execution layer."""

from __future__ import annotations

import logging
import os
import shutil
import subprocess
import webbrowser
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple

import pyautogui

from config import APP_MAPPINGS
from utils import detect_os


class Executor:
    """Executes parsed commands safely with detailed status output."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.os_name = detect_os()

    def _resolve_app(self, name: str) -> Optional[str]:
        mapping = APP_MAPPINGS.get(self.os_name, {})
        key = (name or "").strip().lower()
        return mapping.get(key, key or None)

    def _run_shell(self, command: str) -> Tuple[bool, str]:
        try:
            subprocess.Popen(command, shell=True)
            return True, "Command launched"
        except Exception as exc:
            self.logger.error("Failed running shell command '%s': %s", command, exc)
            return False, f"Execution failed: {exc}"

    def open_app(self, app_name: str) -> Tuple[bool, str]:
        executable = self._resolve_app(app_name)
        if not executable:
            return False, "No application provided"

        # If alias points to a shell command containing spaces, run as shell.
        if " " in executable and shutil.which(executable.split()[0]) is None:
            return self._run_shell(executable)

        try:
            if self.os_name == "windows":
                subprocess.Popen(executable, shell=True)
            else:
                subprocess.Popen(executable.split())
            return True, f"Opening {app_name}"
        except FileNotFoundError:
            return False, f"App '{app_name}' is not installed or not in PATH"
        except Exception as exc:
            self.logger.error("Open app error: %s", exc)
            return False, f"Failed to open {app_name}: {exc}"

    def close_app(self, app_name: str) -> Tuple[bool, str]:
        target = self._resolve_app(app_name)
        if not target:
            return False, "No application provided"

        binary = target.split()[0]
        try:
            if self.os_name == "windows":
                subprocess.run(["taskkill", "/IM", f"{binary}.exe", "/F"], check=False)
            elif self.os_name == "linux":
                subprocess.run(["pkill", "-f", binary], check=False)
            else:
                pyautogui.hotkey("alt", "f4")
            return True, f"Attempted to close {app_name}"
        except Exception as exc:
            self.logger.error("Close app error: %s", exc)
            return False, f"Failed to close {app_name}: {exc}"

    def create_folder(self, folder_name: str) -> Tuple[bool, str]:
        try:
            path = Path(folder_name).expanduser().resolve()
            path.mkdir(parents=True, exist_ok=True)
            return True, f"Folder created at {path}"
        except Exception as exc:
            self.logger.error("Create folder error: %s", exc)
            return False, f"Could not create folder: {exc}"

    def delete_folder(self, folder_name: str) -> Tuple[bool, str]:
        try:
            path = Path(folder_name).expanduser().resolve()
            if not path.exists() or not path.is_dir():
                return False, f"Folder does not exist: {path}"
            os.rmdir(path)
            return True, f"Folder deleted: {path}"
        except OSError:
            return False, "Folder is not empty; delete manually or extend command support"
        except Exception as exc:
            self.logger.error("Delete folder error: %s", exc)
            return False, f"Could not delete folder: {exc}"

    def shutdown_system(self) -> Tuple[bool, str]:
        try:
            if self.os_name == "windows":
                subprocess.Popen("shutdown /s /t 5", shell=True)
            elif self.os_name == "linux":
                subprocess.Popen(["shutdown", "-h", "+1"])
            else:
                return False, "Shutdown is unsupported on this OS"
            return True, "System shutdown scheduled"
        except Exception as exc:
            return False, f"Failed to shutdown: {exc}"

    def restart_system(self) -> Tuple[bool, str]:
        try:
            if self.os_name == "windows":
                subprocess.Popen("shutdown /r /t 5", shell=True)
            elif self.os_name == "linux":
                subprocess.Popen(["shutdown", "-r", "+1"])
            else:
                return False, "Restart is unsupported on this OS"
            return True, "System restart scheduled"
        except Exception as exc:
            return False, f"Failed to restart: {exc}"

    def open_website(self, target: str) -> Tuple[bool, str]:
        websites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "gmail": "https://mail.google.com",
        }
        url = websites.get(target.lower())
        if not url:
            if target.startswith("http"):
                url = target
            else:
                url = f"https://{target.replace(' ', '')}.com"
        try:
            webbrowser.open(url)
            # Optional browser automation hook
            pyautogui.press("f6")
            return True, f"Opening {url}"
        except Exception as exc:
            return False, f"Failed to open website: {exc}"

    def get_time(self) -> Tuple[bool, str]:
        current = datetime.now().strftime("%I:%M %p")
        return True, f"Current time is {current}"
