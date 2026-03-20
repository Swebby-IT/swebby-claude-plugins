"""Caricamento e validazione della configurazione."""

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from claude_memory.constants import MEMORY_DIR, CONFIG_FILE


@dataclass
class QdrantConfig:
    host: str = "localhost"
    port: int = 6333
    collection: str = "project_memory"


@dataclass
class EmbeddingsConfig:
    provider: str = "ollama"  # "ollama" | "openai" | "openrouter"
    model: str = "nomic-embed-text"
    # Ollama
    ollama_host: str = "http://localhost:11434"
    # OpenAI
    openai_api_key: str = ""  # or env OPENAI_API_KEY
    openai_base_url: str = "https://api.openai.com/v1"
    # OpenRouter
    openrouter_api_key: str = ""  # or env OPENROUTER_API_KEY
    openrouter_base_url: str = "https://openrouter.ai/api/v1"


@dataclass
class MemoryConfig:
    max_learnings_on_start: int = 10
    session_retention_days: int = 60
    semantic_search_on_start: bool = True
    max_search_results: int = 5


@dataclass
class SessionConfig:
    auto_session_log: bool = True
    include_git_diff: bool = True
    max_diff_length: int = 5000
    slug_strategy: str = "timestamp"  # "git" | "timestamp"


@dataclass
class FlushConfig:
    enabled: bool = True
    update_context_on_flush: bool = True


@dataclass
class GitConfig:
    log_depth: int = 20
    track_memory_files: bool = True


@dataclass
class Config:
    qdrant: QdrantConfig = field(default_factory=QdrantConfig)
    embeddings: EmbeddingsConfig = field(default_factory=EmbeddingsConfig)
    memory: MemoryConfig = field(default_factory=MemoryConfig)
    session: SessionConfig = field(default_factory=SessionConfig)
    flush: FlushConfig = field(default_factory=FlushConfig)
    git: GitConfig = field(default_factory=GitConfig)
    extra_index_paths: list[str] = field(default_factory=list)


def _parse_dataclass(cls, data: dict):
    """Parse a dict into a dataclass, ignoring unknown keys."""
    if not data:
        return cls()
    known_fields = {f.name for f in cls.__dataclass_fields__.values()}
    filtered = {k: v for k, v in data.items() if k in known_fields}
    return cls(**filtered)


def find_project_root(start_path: str | Path | None = None) -> Path:
    """
    Risali le directory fino a trovare .memory/ o .git/ o claude.md.
    Se nessuno trovato, usa la cwd.
    start_path: directory di partenza (default: cwd).
    """
    cwd = Path(start_path) if start_path else Path.cwd()
    for parent in [cwd, *cwd.parents]:
        if (parent / MEMORY_DIR).exists():
            return parent
        if (parent / ".git").exists():
            return parent
        if (parent / "claude.md").exists() or (parent / "CLAUDE.md").exists():
            return parent
    return cwd


def load_config(project_root: Path | None = None) -> Config:
    """
    Carica la configurazione da .memory/config.yaml.
    Se il file non esiste, ritorna config di default.
    """
    if project_root is None:
        project_root = find_project_root()

    config_path = project_root / MEMORY_DIR / CONFIG_FILE

    if not config_path.exists():
        return Config()

    with open(config_path) as f:
        raw = yaml.safe_load(f) or {}

    return Config(
        qdrant=_parse_dataclass(QdrantConfig, raw.get("qdrant")),
        embeddings=_parse_dataclass(EmbeddingsConfig, raw.get("embeddings", raw.get("ollama"))),
        memory=_parse_dataclass(MemoryConfig, raw.get("memory")),
        session=_parse_dataclass(SessionConfig, raw.get("session")),
        flush=_parse_dataclass(FlushConfig, raw.get("flush")),
        git=_parse_dataclass(GitConfig, raw.get("git")),
        extra_index_paths=raw.get("extra_index_paths", []),
    )
