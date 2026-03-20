"""
Client per generare embedding via Ollama locale.

Supporta qualsiasi modello di embedding disponibile su Ollama.
Default: nomic-embed-text (768 dimensioni, buon bilanciamento qualità/velocità).
"""

import requests

from claude_memory.config import Config

# Cache semplice per evitare ri-embedding dello stesso testo nella stessa run
_cache: dict[str, list[float]] = {}


def get_embedding(text: str, config: Config) -> list[float]:
    """
    Genera embedding per un testo usando Ollama.

    Args:
        text: testo da embeddare (verrà troncato a 8000 char)
        config: configurazione con host e modello Ollama

    Returns:
        Lista di float (vettore embedding)

    Raises:
        ConnectionError: se Ollama non è raggiungibile
        ValueError: se il modello non è disponibile
    """
    text = text[:8000].strip()

    if not text:
        raise ValueError("Empty text for embedding")

    cache_key = f"{config.ollama.model}:{hash(text)}"
    if cache_key in _cache:
        return _cache[cache_key]

    try:
        response = requests.post(
            f"{config.ollama.host}/api/embed",
            json={
                "model": config.ollama.model,
                "input": text,
            },
            timeout=30,
        )
        response.raise_for_status()

        data = response.json()
        embedding = data["embeddings"][0]

        if len(_cache) < 1000:
            _cache[cache_key] = embedding

        return embedding

    except requests.ConnectionError:
        raise ConnectionError(
            f"Cannot connect to Ollama at {config.ollama.host}. "
            f"Make sure Ollama is running: ollama serve"
        )
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(
                f"Model '{config.ollama.model}' not found in Ollama. "
                f"Pull it first: ollama pull {config.ollama.model}"
            )
        raise
