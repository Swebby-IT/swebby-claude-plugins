"""
Genera il session log da git diff e checkpoint.

Il session log è un file markdown in .memory/sessions/YYYY-MM-DD_slug.md
che cattura cosa è stato fatto nella sessione.
"""

import time
from datetime import date, datetime
from pathlib import Path

from claude_memory.config import Config
from claude_memory.memory.manager import read_checkpoint, read_context
from claude_memory.utils import (
    get_git_diff,
    get_git_diff_stat,
    get_git_log_oneline,
    get_recent_commits_messages,
    slugify,
)


def generate_session_log(project_root: Path, config: Config) -> Path | None:
    """
    Genera il session log per la sessione corrente.

    Ritorna il Path del file generato, o None se non c'era nulla da loggare.
    """
    checkpoint = read_checkpoint(project_root)

    if not checkpoint or not checkpoint.get("files_modified"):
        return None

    sessions_dir = project_root / ".memory" / "sessions"
    sessions_dir.mkdir(parents=True, exist_ok=True)

    today = date.today().isoformat()
    now = datetime.now().strftime("%H%M%S")

    # Genera slug — sempre timestamp per evitare duplicati "fix"
    if config.session.slug_strategy == "git":
        commits = get_recent_commits_messages(project_root, n=3)
        slug = slugify(commits[0] if commits else "session")
    else:
        slug = datetime.now().strftime("%H%M")

    # Evita conflitti di nome
    base_name = f"{today}_{slug}"
    session_file = sessions_dir / f"{base_name}.md"
    counter = 1
    while session_file.exists():
        session_file = sessions_dir / f"{base_name}_{counter}.md"
        counter += 1

    # Raccogli informazioni
    files_modified = checkpoint.get("files_modified", [])
    unique_files = list({f["path"] for f in files_modified})

    diff_stat = get_git_diff_stat(project_root, depth=config.git.log_depth)
    git_log = get_git_log_oneline(project_root, n=config.git.log_depth)

    # Durata sessione
    duration = ""
    if checkpoint.get("started_at"):
        elapsed = time.time() - checkpoint["started_at"]
        minutes = int(elapsed // 60)
        duration = f"Durata: ~{minutes} min"

    # Identifica le aree toccate dai file modificati
    areas = _identify_areas(unique_files)
    areas_str = ", ".join(areas) if areas else "varie"

    files_list = "\n".join(f"- {f}" for f in sorted(unique_files))

    # Leggi work in progress da CONTEXT.md per contesto
    wip = _get_work_in_progress(project_root)
    wip_section = f"\n## Contesto\n{wip}\n" if wip else ""

    content = f"""# Session {today} {now} — {areas_str}
{duration} | {len(unique_files)} file modificati
{wip_section}
## File Modificati
{files_list}

## Git Activity
```
{git_log}
```

## Diff Summary
```
{diff_stat}
```
"""

    # Aggiungi git diff completo se configurato
    if config.session.include_git_diff:
        full_diff = get_git_diff(project_root)
        if full_diff:
            truncated = full_diff[: config.session.max_diff_length]
            if len(full_diff) > config.session.max_diff_length:
                truncated += "\n... (diff troncato)"
            content += f"""
## Full Diff
```diff
{truncated}
```
"""

    session_file.write_text(content, encoding="utf-8")
    return session_file


def _identify_areas(files: list[str]) -> list[str]:
    """Identifica le aree/app toccate dai file modificati."""
    areas = set()
    for f in files:
        parts = Path(f).parts
        # Cerca pattern tipo app/nome_app/ o src/nome/
        for i, part in enumerate(parts):
            if part in ("app", "apps", "src", "templates", "static"):
                if i + 1 < len(parts):
                    areas.add(parts[i + 1])
                break
            # Django app detection: se contiene models.py, views.py etc
            if part.endswith(".py") or part.endswith(".html") or part.endswith(".css"):
                if i > 0 and parts[i - 1] not in (".", "..", "src", "static", "templates"):
                    areas.add(parts[i - 1])
                break
    return sorted(areas)[:5]  # Max 5 aree


def _get_work_in_progress(project_root: Path) -> str:
    """Estrae la sezione Work in Progress da CONTEXT.md."""
    context = read_context(project_root)
    if not context:
        return ""

    lines = context.split("\n")
    capture = False
    wip_lines = []

    for line in lines:
        if "Work in Progress" in line:
            capture = True
            continue
        elif line.startswith("## ") and capture:
            break
        elif capture and line.strip():
            wip_lines.append(line)

    return "\n".join(wip_lines).strip()
