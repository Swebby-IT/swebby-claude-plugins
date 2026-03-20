"""
Hook PreCompact: salva informazioni importanti prima della compaction del contesto.

Quando Claude sta per compattare il contesto (perché la context window è piena),
questo hook salva lo stato corrente della sessione in file persistenti.
"""

import json
import sys

from claude_memory.config import find_project_root, load_config
from claude_memory.memory.flush import execute_flush


def main():
    stdin_data = sys.stdin.read().strip()
    hook_input = json.loads(stdin_data) if stdin_data else {}  # noqa: F841

    project_root = find_project_root()
    config = load_config(project_root)

    if not config.flush.enabled:
        sys.exit(0)

    execute_flush(project_root, config, trigger="pre_compact")

    sys.exit(0)


if __name__ == "__main__":
    main()
