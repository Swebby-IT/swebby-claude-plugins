"""
Hook Stop: genera session log e indicizza quando Claude finisce.

Operazioni:
1. Legge il checkpoint della sessione corrente
2. Genera il session log .md
3. Aggiorna CONTEXT.md
4. Indicizza in Qdrant
5. Pulisce il checkpoint
"""

import json
import sys

from claude_memory.config import find_project_root, load_config
from claude_memory.memory.manager import update_context_from_session
from claude_memory.memory.session_logger import generate_session_log


def main():
    stdin_data = sys.stdin.read().strip()
    hook_input = json.loads(stdin_data) if stdin_data else {}  # noqa: F841

    project_root = find_project_root()
    config = load_config(project_root)

    if not config.session.auto_session_log:
        sys.exit(0)

    # 1. Genera session log
    session_file = generate_session_log(project_root, config)

    # 2. Aggiorna CONTEXT.md
    if session_file:
        update_context_from_session(project_root, session_file)

    # 3. Indicizza in Qdrant
    try:
        from claude_memory.indexing.indexer import index_updated_files

        index_updated_files(project_root, config)
    except Exception as e:
        print(f"Warning: indexing failed: {e}", file=sys.stderr)

    # 4. Pulisci checkpoint
    checkpoint_file = project_root / ".memory" / "checkpoints" / ".session.json"
    if checkpoint_file.exists():
        checkpoint_file.unlink()

    sys.exit(0)


if __name__ == "__main__":
    main()
