"""
Genera il session log da git diff e checkpoint.

Il session log è un file markdown in .memory/sessions/YYYY-MM-DD_slug.md
che cattura cosa è stato fatto nella sessione.
"""

import time
from datetime import date, datetime
from pathlib import Path

from claude_memory.config import Config
from claude_memory.memory.manager import read_checkpoint
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

    # Genera slug
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

    # Genera contenuto
    duration = ""
    if checkpoint.get("started_at"):
        elapsed = time.time() - checkpoint["started_at"]
        minutes = int(elapsed // 60)
        duration = f"\nDurata sessione: ~{minutes} minuti"

    files_list = "\n".join(f"- {f}" for f in sorted(unique_files))

    content = f"""# Session {today} — {slug}
{duration}

## File Modificati ({len(unique_files)})
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
