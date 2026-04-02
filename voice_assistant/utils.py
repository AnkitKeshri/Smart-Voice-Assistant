"""Utility helpers for logging, platform checks, and persistence."""

from __future__ import annotations

import json
import logging
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from config import HISTORY_FILE, LOG_FILE, LOG_LEVEL


def setup_logging() -> None:
    """Configure application-wide logging."""
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
    )


def detect_os() -> str:
    """Return normalized OS key used by command mappings."""
    system = platform.system().lower()
    if "windows" in system:
        return "windows"
    if "linux" in system:
        return "linux"
    return "unknown"


def safe_load_json(path: Path, default: Any) -> Any:
    """Safely load JSON and return default when unavailable/invalid."""
    try:
        if not path.exists():
            return default
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        logging.getLogger(__name__).warning("Failed loading JSON from %s: %s", path, exc)
        return default


def append_history(record: Dict[str, Any]) -> None:
    """Append command execution history as JSON lines."""
    payload = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        **record,
    }
    try:
        with HISTORY_FILE.open("a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception as exc:
        logging.getLogger(__name__).warning("Failed to write history: %s", exc)
