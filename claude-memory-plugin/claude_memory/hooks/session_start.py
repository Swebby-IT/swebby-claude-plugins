"""
Hook SessionStart: carica contesto della memoria all'avvio sessione.

Viene invocato come: python3 -m claude_memory.hooks.session_start
Riceve JSON su stdin con informazioni della sessione.
Stampa su stdout il contesto da iniettare nella conversazione.
"""

import json
import sys

from claude_memory.config import find_project_root, load_config
from claude_memory.memory.context_builder import build_session_context


def main():
    """Entry point dell'hook SessionStart."""
    stdin_data = sys.stdin.read().strip()
    hook_input = json.loads(stdin_data) if stdin_data else {}  # noqa: F841

    project_root = find_project_root()
    config = load_config(project_root)

    context = build_session_context(project_root, config)

    if context:
        print(context)

    sys.exit(0)


if __name__ == "__main__":
    main()
