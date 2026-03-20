"""
Logic del pre-compaction flush.

Quando la context window sta per essere compattata (PreCompact hook)
o quando viene chiamato manualmente (claude-memory flush),
salva lo stato corrente della sessione.
"""

import json
from datetime import datetime
from pathlib import Path

from claude_memory.config import Config
from claude_memory.constants import CHECKPOINTS_DIR, SESSION_CHECKPOINT
from claude_memory.memory.manager import read_checkpoint
from claude_memory.utils import get_git_diff_stat


def execute_flush(
    project_root: Path, config: Config, trigger: str = "manual"
) -> None:
    """
    Esegue il flush della memoria.

    Args:
        project_root: root del progetto
        config: configurazione
        trigger: "pre_compact" | "manual" | "stop"
    """
    checkpoint = read_checkpoint(project_root)

    if not checkpoint:
        return

    # Aggiorna CONTEXT.md con lo stato corrente
    if config.flush.update_context_on_flush:
        _update_context_with_current_state(project_root, checkpoint)

    # Salva un checkpoint intermedio con timestamp del flush
    checkpoint["last_flush"] = datetime.now().isoformat()
    checkpoint["flush_trigger"] = trigger

    checkpoint_file = (
        project_root / ".memory" / CHECKPOINTS_DIR / SESSION_CHECKPOINT
    )
    with open(checkpoint_file, "w") as f:
        json.dump(checkpoint, f, indent=2)


def _update_context_with_current_state(
    project_root: Path, checkpoint: dict
) -> None:
    """
    Aggiorna CONTEXT.md con le informazioni dal checkpoint.

    Strategia conservativa: aggiorna solo la sezione "Recent Activity",
    non tocca il resto.
    """
    context_path = project_root / ".memory" / "CONTEXT.md"

    if not context_path.exists():
        return

    content = context_path.read_text(encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    files_modified = list(
        {f["path"] for f in checkpoint.get("files_modified", [])}
    )
    diff_stat = get_git_diff_stat(project_root)

    activity_section = f"""## Recent Activity (auto-updated: {now})
- File modificati in questa sessione: {len(files_modified)}
- Ultimi file toccati: {', '.join(files_modified[:10])}
- Git status: {diff_stat[:200]}
"""

    if "## Recent Activity" in content:
        lines = content.split("\n")
        new_lines = []
        skip = False
        for line in lines:
            if line.startswith("## Recent Activity"):
                skip = True
                new_lines.append(activity_section)
            elif line.startswith("## ") and skip:
                skip = False
                new_lines.append(line)
            elif not skip:
                new_lines.append(line)
        content = "\n".join(new_lines)
    else:
        content += "\n" + activity_section

    # Aggiorna il timestamp in header
    lines = content.split("\n")
    for i, line in enumerate(lines):
        if line.startswith("Last updated:"):
            lines[i] = f"Last updated: {now}"
            break
    content = "\n".join(lines)

    context_path.write_text(content, encoding="utf-8")
