"""CLI Click: init, flush, search, status, reindex, clean."""

import json
import shutil
from datetime import date, datetime, timedelta
from pathlib import Path

import click

from claude_memory.config import Config, find_project_root, load_config
from claude_memory.constants import (
    CHECKPOINTS_DIR,
    CLAUDE_MD_MARKER_END,
    CLAUDE_MD_MARKER_START,
    CONTEXT_FILE,
    DECISIONS_FILE,
    LEARNINGS_FILE,
    MEMORY_DIR,
    SESSIONS_DIR,
)
from claude_memory.utils import get_current_branch


@click.group()
def cli():
    """claude-memory: Persistent memory plugin for Claude Code."""
    pass


@cli.command()
@click.option("--project-name", default=None, help="Nome del progetto (default: nome directory)")
@click.option("--qdrant-host", default="localhost", help="Override host Qdrant")
@click.option("--qdrant-port", default=6333, type=int, help="Override porta Qdrant")
@click.option("--ollama-host", default=None, help="Override host Ollama")
@click.option("--no-index", is_flag=True, help="Skip indicizzazione iniziale")
@click.option("--force", is_flag=True, help="Sovrascrive config esistente")
def init(project_name, qdrant_host, qdrant_port, ollama_host, no_index, force):
    """Inizializza claude-memory nel progetto corrente."""
    project_root = find_project_root()

    if project_name is None:
        project_name = project_root.name

    memory_dir = project_root / MEMORY_DIR
    collection_name = f"memory_{project_name.replace('-', '_').replace(' ', '_')}"

    click.echo(f"Inizializzazione claude-memory per '{project_name}'...")
    click.echo(f"Project root: {project_root}")

    # 1. Crea struttura .memory/
    memory_dir.mkdir(exist_ok=True)
    (memory_dir / SESSIONS_DIR).mkdir(exist_ok=True)
    (memory_dir / CHECKPOINTS_DIR).mkdir(exist_ok=True)
    (memory_dir / SESSIONS_DIR / ".gitkeep").touch()
    (memory_dir / CHECKPOINTS_DIR / ".gitkeep").touch()

    # 2. Genera file template
    templates_dir = Path(__file__).parent / "templates"

    today = date.today().isoformat()
    branch = get_current_branch(project_root) or "main"

    template_vars = {
        "date": today,
        "project_name": project_name,
        "branch": branch,
        "collection_name": collection_name,
    }

    _create_from_template(
        templates_dir / "CONTEXT.md.tpl",
        memory_dir / CONTEXT_FILE,
        template_vars,
        force,
    )
    _create_from_template(
        templates_dir / "DECISIONS.md.tpl",
        memory_dir / DECISIONS_FILE,
        template_vars,
        force,
    )
    _create_from_template(
        templates_dir / "LEARNINGS.md.tpl",
        memory_dir / LEARNINGS_FILE,
        template_vars,
        force,
    )
    _create_from_template(
        templates_dir / "config.yaml.tpl",
        memory_dir / "config.yaml",
        template_vars,
        force,
    )

    # 3. Configura hook in .claude/settings.json
    _setup_hooks(project_root)

    # 4. Aggiungi sezione al claude.md
    _setup_claude_md(project_root, templates_dir, template_vars)

    # 5. Aggiorna .gitignore
    _setup_gitignore(project_root)

    # 6. Crea collection Qdrant e indicizza
    if not no_index:
        try:
            config = load_config(project_root)
            # Override config con parametri CLI
            config.qdrant.host = qdrant_host
            config.qdrant.port = qdrant_port
            if ollama_host:
                config.embeddings.ollama_host = ollama_host

            from claude_memory.indexing.indexer import (
                ensure_collection,
                get_qdrant_client,
                index_updated_files,
            )

            client = get_qdrant_client(config)
            ensure_collection(client, config)
            count = index_updated_files(project_root, config)
            click.echo(f"Indicizzati {count} chunk in Qdrant (collection: {config.qdrant.collection})")
        except Exception as e:
            click.echo(f"Warning: indicizzazione fallita ({e}). Qdrant/Ollama non disponibili?", err=True)
            click.echo("La memoria file-based funziona comunque. Puoi ri-indicizzare con: claude-memory reindex")

    click.echo("Inizializzazione completata!")
    click.echo(f"  .memory/ creata in {memory_dir}")
    click.echo("  Hook configurati in .claude/settings.json")
    click.echo("  Sezione Memory aggiunta al claude.md")


@cli.command()
def flush():
    """Esegue manualmente il flush della memoria."""
    project_root = find_project_root()
    config = load_config(project_root)

    from claude_memory.memory.flush import execute_flush
    from claude_memory.memory.session_logger import generate_session_log

    execute_flush(project_root, config, trigger="manual")

    session_file = generate_session_log(project_root, config)
    if session_file:
        click.echo(f"Session log generato: {session_file}")

        try:
            from claude_memory.indexing.indexer import index_updated_files
            count = index_updated_files(project_root, config)
            click.echo(f"Indicizzati {count} chunk in Qdrant")
        except Exception as e:
            click.echo(f"Warning: indicizzazione fallita ({e})", err=True)
    else:
        click.echo("Nessuna attività da salvare (checkpoint vuoto)")


@cli.command()
@click.argument("query")
@click.option("--limit", default=5, type=int, help="Numero massimo risultati")
@click.option("--type", "filter_type", default=None, help="Filtrare per tipo: curated, session, docs")
@click.option("--after", "after_date", default=None, help="Solo risultati dopo una certa data (YYYY-MM-DD)")
def search(query, limit, filter_type, after_date):
    """Cerca nella memoria del progetto tramite Qdrant."""
    config = load_config()

    try:
        from claude_memory.indexing.indexer import search_memory

        results = search_memory(query, config=config, limit=limit, filter_type=filter_type)

        if not results:
            click.echo("Nessun risultato trovato.")
            return

        for i, r in enumerate(results, 1):
            # Filtra per data se specificato
            if after_date and r.get("date") and r["date"] < after_date:
                continue

            click.echo(f"\n--- Risultato {i} (score: {r['score']:.3f}) ---")
            click.echo(f"Source: {r['source']}")
            if r.get("heading"):
                click.echo(f"Section: {r['heading']}")
            if r.get("type"):
                click.echo(f"Type: {r['type']}")
            click.echo(f"Text: {r['text'][:500]}")

    except Exception as e:
        click.echo(f"Errore nella ricerca: {e}", err=True)
        click.echo("Assicurati che Qdrant e Ollama siano attivi.", err=True)


@cli.command()
def status():
    """Mostra stato corrente della memoria."""
    project_root = find_project_root()
    config = load_config(project_root)
    memory_dir = project_root / MEMORY_DIR

    if not memory_dir.exists():
        click.echo("claude-memory non inizializzato. Esegui: claude-memory init")
        return

    click.echo(f"=== claude-memory status ({project_root.name}) ===\n")

    # Sessioni
    sessions_dir = memory_dir / SESSIONS_DIR
    session_count = len(list(sessions_dir.glob("*.md"))) if sessions_dir.exists() else 0
    click.echo(f"Sessioni registrate: {session_count}")

    # Decisioni
    decisions_file = memory_dir / DECISIONS_FILE
    if decisions_file.exists():
        content = decisions_file.read_text(encoding="utf-8")
        decision_count = content.count("\n## ")
        click.echo(f"Decisioni in DECISIONS.md: {decision_count}")
    else:
        click.echo("DECISIONS.md: non trovato")

    # Learnings
    learnings_file = memory_dir / LEARNINGS_FILE
    if learnings_file.exists():
        content = learnings_file.read_text(encoding="utf-8")
        learning_count = content.count("\n### ")
        click.echo(f"Learnings in LEARNINGS.md: {learning_count}")
    else:
        click.echo("LEARNINGS.md: non trovato")

    # CONTEXT.md
    context_file = memory_dir / CONTEXT_FILE
    if context_file.exists():
        import os
        mtime = os.path.getmtime(context_file)
        last_mod = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M")
        click.echo(f"CONTEXT.md ultimo aggiornamento: {last_mod}")
    else:
        click.echo("CONTEXT.md: non trovato")

    # Checkpoint
    checkpoint_file = memory_dir / CHECKPOINTS_DIR / ".session.json"
    if checkpoint_file.exists():
        with open(checkpoint_file) as f:
            data = json.load(f)
        files_count = len(data.get("files_modified", []))
        click.echo(f"Checkpoint sessione attiva: {files_count} file tracciati")
    else:
        click.echo("Checkpoint sessione: nessuna sessione attiva")

    # Qdrant
    try:
        from claude_memory.indexing.indexer import get_qdrant_client
        client = get_qdrant_client(config)
        info = client.get_collection(config.qdrant.collection)
        click.echo(f"Qdrant collection '{config.qdrant.collection}': {info.points_count} punti")
    except Exception:
        click.echo("Qdrant: non raggiungibile o collection non trovata")


@cli.command()
@click.option("--full", is_flag=True, help="Include tutto il codebase")
@click.option("--sessions-only", is_flag=True, help="Ri-indicizza solo i session log")
def reindex(full, sessions_only):
    """Ri-indicizza tutti i file .memory/ in Qdrant."""
    project_root = find_project_root()
    config = load_config(project_root)

    try:
        from claude_memory.indexing.indexer import reindex_all
        click.echo("Ri-indicizzazione in corso...")
        count = reindex_all(project_root, config, full=full, sessions_only=sessions_only)
        click.echo(f"Ri-indicizzati {count} chunk in Qdrant")
    except Exception as e:
        click.echo(f"Errore: {e}", err=True)


@cli.command()
def clean():
    """Archivia sessioni più vecchie di session_retention_days."""
    project_root = find_project_root()
    config = load_config(project_root)

    sessions_dir = project_root / ".memory" / SESSIONS_DIR
    archive_dir = sessions_dir / "archive"

    if not sessions_dir.exists():
        click.echo("Nessuna sessione da archiviare.")
        return

    cutoff = date.today() - timedelta(days=config.memory.session_retention_days)
    archived = 0

    for session_file in sessions_dir.glob("*.md"):
        try:
            date_str = session_file.stem[:10]
            file_date = date.fromisoformat(date_str)
            if file_date < cutoff:
                archive_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(session_file), str(archive_dir / session_file.name))
                archived += 1
        except ValueError:
            continue

    click.echo(f"Archiviate {archived} sessioni più vecchie di {config.memory.session_retention_days} giorni")


# --- Helper functions ---


def _create_from_template(
    template_path: Path, target_path: Path, variables: dict, force: bool
) -> None:
    """Crea un file da template, sostituendo le variabili."""
    if target_path.exists() and not force:
        click.echo(f"  [skip] {target_path.name} esiste già (usa --force per sovrascrivere)")
        return

    content = template_path.read_text(encoding="utf-8")
    for key, value in variables.items():
        content = content.replace(f"{{{key}}}", value)

    target_path.write_text(content, encoding="utf-8")
    click.echo(f"  [crea] {target_path.name}")


def _setup_hooks(project_root: Path) -> None:
    """Configura gli hook in .claude/settings.json."""
    claude_dir = project_root / ".claude"
    claude_dir.mkdir(exist_ok=True)
    settings_file = claude_dir / "settings.json"

    if settings_file.exists():
        with open(settings_file) as f:
            settings = json.load(f)
    else:
        settings = {}

    hooks = settings.setdefault("hooks", {})

    # Hook definitions
    hook_defs = {
        "SessionStart": {
            "matcher": "",
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 -m claude_memory.hooks.session_start",
                }
            ],
        },
        "PreCompact": {
            "matcher": "",
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 -m claude_memory.hooks.pre_compact",
                }
            ],
        },
        "Stop": {
            "matcher": "",
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 -m claude_memory.hooks.stop",
                }
            ],
        },
        "PostToolUse": {
            "matcher": "Edit|Write|MultiEdit",
            "hooks": [
                {
                    "type": "command",
                    "command": "python3 -m claude_memory.hooks.post_tool_use",
                }
            ],
        },
    }

    for event_name, hook_def in hook_defs.items():
        existing_hooks = hooks.get(event_name, [])

        # Rimuovi hook claude_memory esistenti (per sovrascrivere sempre)
        existing_hooks = [
            entry for entry in existing_hooks
            if not any("claude_memory" in h.get("command", "") for h in entry.get("hooks", []))
        ]

        # Aggiungi la versione aggiornata
        existing_hooks.append(hook_def)
        hooks[event_name] = existing_hooks

    settings["hooks"] = hooks

    with open(settings_file, "w") as f:
        json.dump(settings, f, indent=2)

    click.echo("  [hook] Configurazione hook aggiornata in .claude/settings.json")


def _setup_claude_md(project_root: Path, templates_dir: Path, variables: dict) -> None:
    """Aggiungi sezione Memory al claude.md o CLAUDE.md."""
    # Cerca il file (case-insensitive)
    claude_md = None
    for name in ["CLAUDE.md", "claude.md"]:
        candidate = project_root / name
        if candidate.exists():
            claude_md = candidate
            break

    # Se non esiste, crealo
    if claude_md is None:
        claude_md = project_root / "CLAUDE.md"

    # Leggi il template della sezione
    section_template = (templates_dir / "claude_md_section.md.tpl").read_text(encoding="utf-8")
    for key, value in variables.items():
        section_template = section_template.replace(f"{{{key}}}", value)

    if claude_md.exists():
        content = claude_md.read_text(encoding="utf-8")

        # Controlla se la sezione è già presente
        if CLAUDE_MD_MARKER_START in content:
            # Sostituisci la sezione esistente
            start_idx = content.index(CLAUDE_MD_MARKER_START)
            end_idx = content.index(CLAUDE_MD_MARKER_END) + len(CLAUDE_MD_MARKER_END)
            content = content[:start_idx] + section_template + content[end_idx:]
        else:
            content += "\n\n" + section_template
    else:
        content = section_template

    claude_md.write_text(content, encoding="utf-8")
    click.echo(f"  [claude.md] Sezione Memory aggiunta a {claude_md.name}")


def _setup_gitignore(project_root: Path) -> None:
    """Aggiunge entry a .gitignore per i checkpoint temporanei."""
    gitignore = project_root / ".gitignore"
    entry = "\n# claude-memory checkpoints (temporanei)\n.memory/checkpoints/.session.json\n"

    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if ".memory/checkpoints/.session.json" not in content:
            with open(gitignore, "a", encoding="utf-8") as f:
                f.write(entry)
            click.echo("  [gitignore] Aggiunta esclusione checkpoint")
    else:
        gitignore.write_text(entry.lstrip(), encoding="utf-8")
        click.echo("  [gitignore] Creato .gitignore con esclusione checkpoint")


if __name__ == "__main__":
    cli()
