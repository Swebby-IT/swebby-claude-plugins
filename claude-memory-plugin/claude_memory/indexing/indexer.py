"""
Indicizzazione dei file .memory/ in Qdrant.

Usa il client Qdrant direttamente (non MCP) per la scrittura.
La lettura da parte di Claude avviene via MCP Qdrant già configurato.
"""

import hashlib
from datetime import date, datetime, timedelta
from pathlib import Path

from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    FieldCondition,
    Filter,
    MatchValue,
    PointStruct,
    VectorParams,
)

from claude_memory.config import Config
from claude_memory.indexing.chunker import chunk_markdown
from claude_memory.indexing.embeddings import get_embedding, get_vector_size


def get_qdrant_client(config: Config) -> QdrantClient:
    return QdrantClient(host=config.qdrant.host, port=config.qdrant.port)


def ensure_collection(client: QdrantClient, config: Config) -> None:
    """Crea la collection se non esiste."""
    collections = [c.name for c in client.get_collections().collections]
    if config.qdrant.collection not in collections:
        vector_size = get_vector_size(config)

        client.create_collection(
            collection_name=config.qdrant.collection,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE,
            ),
        )


def index_updated_files(project_root: Path, config: Config) -> int:
    """
    Indicizza i file .memory/ aggiornati in Qdrant.
    Ritorna il numero di punti indicizzati.
    """
    client = get_qdrant_client(config)
    ensure_collection(client, config)

    points = []
    memory_dir = project_root / ".memory"

    # 1. Indicizza file curati
    for filename in ["CONTEXT.md", "DECISIONS.md", "LEARNINGS.md"]:
        filepath = memory_dir / filename
        if not filepath.exists():
            continue

        content = filepath.read_text(encoding="utf-8")
        chunks = chunk_markdown(content, filename)

        for chunk in chunks:
            point_id = _make_point_id(f"{filename}:{chunk['heading']}")
            embedding = get_embedding(chunk["text"], config)

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "source": filename,
                        "type": "curated",
                        "heading": chunk["heading"],
                        "text": chunk["text"],
                        "updated_at": datetime.now().isoformat(),
                    },
                )
            )

    # 2. Indicizza sessioni recenti
    sessions_dir = memory_dir / "sessions"
    if sessions_dir.exists():
        cutoff = date.today() - timedelta(
            days=config.memory.session_retention_days
        )

        for session_file in sessions_dir.glob("*.md"):
            try:
                date_str = session_file.stem[:10]
                file_date = date.fromisoformat(date_str)
                if file_date < cutoff:
                    continue
            except ValueError:
                continue

            content = session_file.read_text(encoding="utf-8")
            point_id = _make_point_id(session_file.name)
            embedding = get_embedding(content[:2000], config)

            points.append(
                PointStruct(
                    id=point_id,
                    vector=embedding,
                    payload={
                        "source": session_file.name,
                        "type": "session",
                        "text": content[:3000],
                        "date": date_str,
                        "updated_at": datetime.now().isoformat(),
                    },
                )
            )

    # 3. Indicizza extra paths (docs/, README, etc.)
    for extra_path_str in config.extra_index_paths:
        extra_path = project_root / extra_path_str
        if extra_path.is_file():
            _index_file(extra_path, project_root, config, points)
        elif extra_path.is_dir():
            for md_file in extra_path.rglob("*.md"):
                _index_file(md_file, project_root, config, points)

    # Upsert in Qdrant
    if points:
        batch_size = 100
        for i in range(0, len(points), batch_size):
            batch = points[i : i + batch_size]
            client.upsert(
                collection_name=config.qdrant.collection,
                points=batch,
            )

    return len(points)


def reindex_all(project_root: Path, config: Config, full: bool = False, sessions_only: bool = False) -> int:
    """
    Ri-indicizza tutti i file .memory/ in Qdrant.
    Cancella i punti esistenti e re-inserisce.
    """
    client = get_qdrant_client(config)

    # Ricrea la collection
    try:
        client.delete_collection(config.qdrant.collection)
    except Exception:
        pass

    ensure_collection(client, config)

    if sessions_only:
        # Indicizza solo sessioni
        points = []
        sessions_dir = project_root / ".memory" / "sessions"
        if sessions_dir.exists():
            for session_file in sessions_dir.glob("*.md"):
                content = session_file.read_text(encoding="utf-8")
                point_id = _make_point_id(session_file.name)
                embedding = get_embedding(content[:2000], config)
                points.append(
                    PointStruct(
                        id=point_id,
                        vector=embedding,
                        payload={
                            "source": session_file.name,
                            "type": "session",
                            "text": content[:3000],
                            "updated_at": datetime.now().isoformat(),
                        },
                    )
                )
        if points:
            client.upsert(collection_name=config.qdrant.collection, points=points)
        return len(points)

    # Full reindex
    return index_updated_files(project_root, config)


def search_memory(
    query: str,
    config: Config,
    limit: int = 5,
    filter_type: str | None = None,
) -> list[dict]:
    """
    Cerca nella memoria tramite Qdrant.

    Args:
        query: testo della query
        config: configurazione
        limit: max risultati
        filter_type: filtrare per tipo (curated, session, docs)
    """
    client = get_qdrant_client(config)
    embedding = get_embedding(query, config)

    search_filter = None
    if filter_type:
        search_filter = Filter(
            must=[
                FieldCondition(key="type", match=MatchValue(value=filter_type))
            ]
        )

    results = client.search(
        collection_name=config.qdrant.collection,
        query_vector=embedding,
        limit=limit,
        query_filter=search_filter,
    )

    return [
        {
            "source": r.payload.get("source", ""),
            "type": r.payload.get("type", ""),
            "heading": r.payload.get("heading", ""),
            "text": r.payload.get("text", ""),
            "date": r.payload.get("date", ""),
            "score": r.score,
        }
        for r in results
    ]


def _index_file(
    filepath: Path, project_root: Path, config: Config, points: list
) -> None:
    """Indicizza un singolo file."""
    content = filepath.read_text(encoding="utf-8")
    relative_path = str(filepath.relative_to(project_root))
    chunks = chunk_markdown(content, relative_path)

    for chunk in chunks:
        point_id = _make_point_id(f"{relative_path}:{chunk['heading']}")
        embedding = get_embedding(chunk["text"], config)

        points.append(
            PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "source": relative_path,
                    "type": "docs",
                    "heading": chunk["heading"],
                    "text": chunk["text"],
                    "updated_at": datetime.now().isoformat(),
                },
            )
        )


def _make_point_id(key: str) -> int:
    """Genera un ID numerico deterministico da una stringa."""
    return int(hashlib.md5(key.encode()).hexdigest()[:15], 16)
