"""
Gestione lettura/scrittura dei file .memory/.

Responsabilità:
- Leggere i file curati (CONTEXT, DECISIONS, LEARNINGS)
- Appendere nuove entry ai file append-only
- Aggiornare CONTEXT.md con nuovo stato
- Leggere e scrivere checkpoint sessione
"""

import json
from datetime import date, datetime
from pathlib import Path

from claude_memory.constants import (
    CHECKPOINTS_DIR,
    CONTEXT_FILE,
    DECISIONS_FILE,
    LEARNINGS_FILE,
    MEMORY_DIR,
    SESSION_CHECKPOINT,
)


def get_memory_dir(project_root: Path) -> Path:
    return project_root / MEMORY_DIR


def read_context(project_root: Path) -> str:
    """Legge CONTEXT.md. Ritorna stringa vuota se non esiste."""
    path = get_memory_dir(project_root) / CONTEXT_FILE
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_decisions(project_root: Path, last_n: int | None = None) -> str:
    """
    Legge DECISIONS.md.
    Se last_n è specificato, ritorna solo le ultime N decisioni.
    Le decisioni sono separate da "## " (heading level 2 con data).
    """
    path = get_memory_dir(project_root) / DECISIONS_FILE
    if not path.exists():
        return ""

    content = path.read_text(encoding="utf-8")

    if last_n is None:
        return content

    sections = content.split("\n## ")
    if len(sections) <= 1:
        return content

    header = sections[0]
    entries = sections[1:]
    recent = entries[-last_n:]
    return header + "\n## ".join([""] + recent)


def read_learnings(project_root: Path, last_n: int | None = None) -> str:
    """
    Legge LEARNINGS.md.
    Se last_n è specificato, ritorna solo gli ultimi N learnings.
    I learnings sono separati da "### " (heading level 3).
    """
    path = get_memory_dir(project_root) / LEARNINGS_FILE
    if not path.exists():
        return ""

    content = path.read_text(encoding="utf-8")

    if last_n is None:
        return content

    sections = content.split("\n### ")
    if len(sections) <= 1:
        return content

    header = sections[0]
    entries = sections[1:]
    recent = entries[-last_n:]
    return header + "\n### ".join([""] + recent)


def append_decision(
    project_root: Path,
    title: str,
    context: str,
    decision: str,
    reason: str,
    files: list[str],
) -> None:
    """Appende una nuova decisione a DECISIONS.md."""
    path = get_memory_dir(project_root) / DECISIONS_FILE
    today = date.today().isoformat()

    entry = f"""
## {today}: {title}
- **Contesto**: {context}
- **Decisione**: {decision}
- **Motivo**: {reason}
- **File coinvolti**: {', '.join(files)}
"""

    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)


def append_learning(
    project_root: Path, title: str, error: str, correction: str, rule: str
) -> None:
    """Appende un nuovo learning a LEARNINGS.md."""
    path = get_memory_dir(project_root) / LEARNINGS_FILE
    today = date.today().isoformat()

    entry = f"""
### {title} (scoperto: {today})
- **Errore**: {error}
- **Correzione**: {correction}
- **Regola**: {rule}
"""

    with open(path, "a", encoding="utf-8") as f:
        f.write(entry)


def update_context(project_root: Path, new_content: str) -> None:
    """Sovrascrive CONTEXT.md con nuovo contenuto."""
    path = get_memory_dir(project_root) / CONTEXT_FILE

    header = (
        "# Project Context (auto-updated)\n"
        f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    )

    if not new_content.startswith("# Project Context"):
        new_content = header + new_content

    path.write_text(new_content, encoding="utf-8")


def update_context_from_session(project_root: Path, session_file: Path) -> None:
    """
    Aggiorna CONTEXT.md basandosi sul session log appena generato.
    Legge la sezione "Context at End of Session" dal session log
    e la usa per aggiornare CONTEXT.md.
    """
    session_content = session_file.read_text(encoding="utf-8")
    context_path = get_memory_dir(project_root) / CONTEXT_FILE

    if not context_path.exists():
        return

    content = context_path.read_text(encoding="utf-8")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Estrai la prima riga del session log come sommario
    first_line = session_content.split("\n")[0].lstrip("# ").strip()

    activity_entry = f"- [{now}] {first_line}"

    if "## Recent Activity" in content:
        # Aggiungi sotto la sezione esistente
        lines = content.split("\n")
        new_lines = []
        inserted = False
        for line in lines:
            new_lines.append(line)
            if line.startswith("## Recent Activity") and not inserted:
                new_lines.append(activity_entry)
                inserted = True
        content = "\n".join(new_lines)
    else:
        content += f"\n## Recent Activity\n{activity_entry}\n"

    # Aggiorna timestamp
    if "Last updated:" in content:
        lines = content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("Last updated:"):
                lines[i] = f"Last updated: {now}"
                break
        content = "\n".join(lines)

    context_path.write_text(content, encoding="utf-8")


def read_checkpoint(project_root: Path) -> dict | None:
    """Legge il checkpoint della sessione corrente."""
    checkpoint_file = (
        get_memory_dir(project_root) / CHECKPOINTS_DIR / SESSION_CHECKPOINT
    )
    if not checkpoint_file.exists():
        return None

    with open(checkpoint_file) as f:
        return json.load(f)
