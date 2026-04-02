"""Configuration for the Smart Voice Assistant."""

from pathlib import Path

# Wake word configuration
WAKE_WORDS = ["hey assistant", "assistant"]

# Audio tuning
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 7
AMBIENT_NOISE_DURATION = 1.0

# Optional online STT fallback. Set False for strict offline behavior.
ENABLE_GOOGLE_FALLBACK = False

# Matching thresholds
COMMAND_SIMILARITY_THRESHOLD = 0.55

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = Path("assistant.log")
HISTORY_FILE = Path("command_history.jsonl")

# Platform application aliases (extend as needed)
APP_MAPPINGS = {
    "windows": {
        "chrome": "chrome",
        "google chrome": "chrome",
        "notepad": "notepad",
        "vs code": "code",
        "visual studio code": "code",
        "calculator": "calc",
        "explorer": "explorer",
    },
    "linux": {
        "chrome": "google-chrome",
        "google chrome": "google-chrome",
        "notepad": "gedit",
        "text editor": "gedit",
        "vs code": "code",
        "visual studio code": "code",
        "files": "xdg-open .",
        "calculator": "gnome-calculator",
    },
}

# File paths for user-extensible command map
CUSTOM_COMMANDS_FILE = Path("custom_commands.json")
