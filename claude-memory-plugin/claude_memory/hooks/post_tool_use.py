"""
Hook PostToolUse per Edit|Write|MultiEdit: traccia i file modificati nella sessione.

DEVE essere veloce (< 200ms) perché gira su ogni edit.
Appende solo il path e timestamp a un file JSON di checkpoint.
"""

import json
import sys
import time

from claude_memory.config import find_project_root


def main():
    stdin_data = sys.stdin.read().strip()
    if not stdin_data:
        sys.exit(0)

    hook_input = json.loads(stdin_data)

    # Estrai il file path dal tool_input
    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path") or tool_input.get("path", "")

    if not file_path:
        sys.exit(0)

    # Non tracciare modifiche ai file .memory/ stessi
    if ".memory/" in file_path or ".memory\\" in file_path:
        sys.exit(0)

    # Usa cwd dal hook input per trovare la project root
    cwd = hook_input.get("cwd", "")
    project_root = find_project_root(cwd if cwd else None)
    checkpoint_dir = project_root / ".memory" / "checkpoints"
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    checkpoint_file = checkpoint_dir / ".session.json"

    # Leggi checkpoint esistente o crea nuovo
    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            session_data = json.load(f)
    else:
        session_data = {
            "started_at": time.time(),
            "files_modified": [],
        }

    # Aggiungi il file
    entry = {
        "path": file_path,
        "timestamp": time.time(),
        "tool": hook_input.get("tool_name", "unknown"),
    }
    session_data["files_modified"].append(entry)

    # Scrivi checkpoint
    with open(checkpoint_file, "w") as f:
        json.dump(session_data, f, indent=2)

    sys.exit(0)


if __name__ == "__main__":
    main()
