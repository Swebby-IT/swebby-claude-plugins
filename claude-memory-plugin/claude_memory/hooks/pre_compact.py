"""
Hook PreCompact: salva checkpoint prima della compaction del contesto.

NON genera session log completo — salva solo il checkpoint con timestamp
del flush per non perdere il tracking dei file modificati.
Il riassunto semantico viene fatto da /save-memory o dal comando Claude.
"""

import json
import sys
from datetime import datetime

from claude_memory.config import find_project_root
from claude_memory.constants import CHECKPOINTS_DIR, SESSION_CHECKPOINT


def main():
    stdin_data = sys.stdin.read().strip()
    hook_input = json.loads(stdin_data) if stdin_data else {}

    cwd = hook_input.get("cwd", "")
    project_root = find_project_root(cwd if cwd else None)

    # Salva timestamp del flush nel checkpoint
    checkpoint_file = (
        project_root / ".memory" / CHECKPOINTS_DIR / SESSION_CHECKPOINT
    )
    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            data = json.load(f)
        data["last_flush"] = datetime.now().isoformat()
        data["flush_trigger"] = "pre_compact"
        with open(checkpoint_file, "w") as f:
            json.dump(data, f, indent=2)

    # Stampa promemoria su stdout — Claude lo vede nel contesto
    print("⚠️ Contesto in compattazione. Scrivi un riassunto di cosa hai fatto in questa sessione in .memory/sessions/ e aggiorna .memory/CONTEXT.md prima di continuare.")

    sys.exit(0)


if __name__ == "__main__":
    main()
