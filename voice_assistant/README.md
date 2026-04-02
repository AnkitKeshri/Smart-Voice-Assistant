# Smart Voice Assistant (Offline-First)

## 1) Setup

1. Create and activate a virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .\.venv\Scripts\Activate.ps1
     ```
   - **Linux/macOS (bash):**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Notes for offline STT
- This project uses `pocketsphinx` via `SpeechRecognition.recognize_sphinx` for offline speech recognition.
- If your platform has trouble installing `PyAudio`, install system audio headers first:
  - Ubuntu/Debian example: `sudo apt-get install portaudio19-dev python3-pyaudio`

## 2) Run

```bash
python main.py
```

## 3) Usage Flow

1. Say wake word: **"Hey Assistant"**
2. Say command after prompt.
3. Assistant executes and speaks response.
4. Returns to listening mode.

## 4) Example Commands

- "Open Chrome"
- "Close Notepad"
- "Create folder Projects"
- "Delete folder Projects"
- "Shutdown system"
- "Restart system"
- "What is the time"
- "Open YouTube"

## 5) Custom Commands

Create `custom_commands.json` beside `main.py`:

```json
{
  "open terminal": "gnome-terminal",
  "open documents": "xdg-open ~/Documents"
}
```

The assistant checks exact raw-text matches against this file before built-in intents.

## 6) Safety & Reliability

- All modules have exception handling.
- Failures are logged to `assistant.log`.
- Command history is appended to `command_history.jsonl`.
