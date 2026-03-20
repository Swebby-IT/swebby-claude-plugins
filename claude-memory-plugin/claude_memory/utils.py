"""Utility condivise: git helpers, formatting, etc."""

import re
import subprocess
from pathlib import Path


def run_git(project_root: Path, *args, timeout: int = 10) -> str:
    """Esegue un comando git e ritorna stdout. Ritorna stringa vuota su errore."""
    try:
        result = subprocess.run(
            ["git", *args],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(project_root),
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return ""


def get_git_diff_stat(project_root: Path, depth: int = 10) -> str:
    """Ritorna il git diff --stat degli ultimi N commit."""
    return run_git(project_root, "diff", "--stat", f"HEAD~{depth}..HEAD")


def get_git_diff(project_root: Path) -> str:
    """Ritorna il git diff completo (unstaged + staged)."""
    staged = run_git(project_root, "diff", "--cached")
    unstaged = run_git(project_root, "diff")
    return f"{staged}\n{unstaged}".strip()


def get_git_log_oneline(project_root: Path, n: int = 10) -> str:
    """Ritorna le ultime N righe del git log --oneline."""
    return run_git(project_root, "log", "--oneline", f"-{n}")


def get_recent_commits_messages(project_root: Path, n: int = 5) -> list[str]:
    """Ritorna i messaggi degli ultimi N commit."""
    log = run_git(project_root, "log", "--format=%s", f"-{n}")
    return [line for line in log.split("\n") if line] if log else []


def get_current_branch(project_root: Path) -> str:
    """Ritorna il nome del branch corrente."""
    return run_git(project_root, "rev-parse", "--abbrev-ref", "HEAD")


def slugify(text: str, max_length: int = 50) -> str:
    """Converte testo in slug URL-safe."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    text = text.strip("-")
    return text[:max_length]
