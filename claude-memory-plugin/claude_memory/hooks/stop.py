"""
Hook Stop: pulisce il checkpoint quando Claude finisce.

NON genera session log — quello si fa solo con /save-memory o PreCompact.
"""

import json
import sys

from claude_memory.config import find_project_root


def main():
    stdin_data = sys.stdin.read().strip()
    hook_input = json.loads(stdin_data) if stdin_data else {}

    cwd = hook_input.get("cwd", "")
    project_root = find_project_root(cwd if cwd else None)

    # Pulisci checkpoint
    checkpoint_file = project_root / ".memory" / "checkpoints" / ".session.json"
    if checkpoint_file.exists():
        checkpoint_file.unlink()

    sys.exit(0)


if __name__ == "__main__":
    main()
