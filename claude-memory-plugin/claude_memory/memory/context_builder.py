"""
Costruisce il contesto da iniettare al SessionStart.

Assembla informazioni da:
1. CONTEXT.md (sempre caricato)
2. LEARNINGS.md (ultimi N)
3. Qdrant semantic search (opzionale, se configurato)
"""

from pathlib import Path

from claude_memory.config import Config
from claude_memory.memory.manager import read_context, read_learnings


def build_session_context(project_root: Path, config: Config) -> str:
    """
    Costruisce il contesto completo per la sessione.

    Ritorna una stringa formattata che verrà stampata su stdout
    dall'hook SessionStart e letta da Claude.
    """
    parts = []

    # 1. CONTEXT.md — sempre incluso
    context = read_context(project_root)
    if context:
        parts.append("=== PROJECT MEMORY: Current State ===")
        parts.append(context)

    # 2. LEARNINGS.md — ultimi N
    learnings = read_learnings(
        project_root, last_n=config.memory.max_learnings_on_start
    )
    if learnings:
        parts.append("\n=== PROJECT MEMORY: Recent Learnings ===")
        parts.append(learnings)

    # 3. Qdrant semantic search (opzionale)
    if config.memory.semantic_search_on_start:
        qdrant_context = _search_relevant_context(project_root, config)
        if qdrant_context:
            parts.append("\n=== PROJECT MEMORY: Related Past Sessions ===")
            parts.append(qdrant_context)

    if not parts:
        return ""

    return "\n".join(parts)


def _search_relevant_context(project_root: Path, config: Config) -> str:
    """
    Cerca contesto rilevante in Qdrant basandosi sullo stato corrente.

    Strategia: usa il contenuto di CONTEXT.md come query
    per trovare sessioni passate e decisioni correlate.
    """
    try:
        from claude_memory.indexing.indexer import search_memory

        context = read_context(project_root)
        if not context:
            return ""

        query = _extract_query_from_context(context)
        if not query:
            return ""

        results = search_memory(
            query,
            config=config,
            limit=config.memory.max_search_results,
            filter_type="session",
        )

        if not results:
            return ""

        formatted = []
        for r in results:
            formatted.append(
                f"- [{r['source']}] (relevance: {r['score']:.2f}): "
                f"{r['text'][:300]}..."
            )

        return "\n".join(formatted)

    except Exception:
        # Se Qdrant non è raggiungibile, non bloccare
        return ""


def _extract_query_from_context(context: str) -> str:
    """Estrae la parte più rilevante di CONTEXT.md per fare la query."""
    lines = context.split("\n")
    capture = False
    query_lines = []

    for line in lines:
        if "Work in Progress" in line or "Current State" in line:
            capture = True
            continue
        elif line.startswith("## ") and capture:
            break
        elif capture:
            query_lines.append(line)

    query = " ".join(query_lines).strip()
    return query[:500] if query else ""
