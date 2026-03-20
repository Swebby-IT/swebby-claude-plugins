"""
Client per generare embedding via Ollama, OpenAI o OpenRouter.

Provider supportati:
- ollama: locale, nomic-embed-text (768 dim) — default
- openai: text-embedding-3-small (1536 dim), text-embedding-3-large (3072 dim)
- openrouter: qualsiasi modello embedding disponibile su OpenRouter
"""

import os

import requests

from claude_memory.config import Config

# Cache semplice per evitare ri-embedding dello stesso testo nella stessa run
_cache: dict[str, list[float]] = {}


def get_embedding(text: str, config: Config) -> list[float]:
    """
    Genera embedding per un testo usando il provider configurato.

    Args:
        text: testo da embeddare (verrà troncato a 8000 char)
        config: configurazione con provider e credenziali

    Returns:
        Lista di float (vettore embedding)
    """
    text = text[:8000].strip()

    if not text:
        raise ValueError("Empty text for embedding")

    cache_key = f"{config.embeddings.provider}:{config.embeddings.model}:{hash(text)}"
    if cache_key in _cache:
        return _cache[cache_key]

    provider = config.embeddings.provider
    if provider == "ollama":
        embedding = _embed_ollama(text, config)
    elif provider == "openai":
        embedding = _embed_openai(text, config)
    elif provider == "openrouter":
        embedding = _embed_openrouter(text, config)
    else:
        raise ValueError(f"Unknown embedding provider: {provider}. Use: ollama, openai, openrouter")

    if len(_cache) < 1000:
        _cache[cache_key] = embedding

    return embedding


def get_vector_size(config: Config) -> int:
    """Ritorna la dimensione del vettore in base al provider/modello."""
    model = config.embeddings.model
    provider = config.embeddings.provider

    # Dimensioni note per modelli comuni
    known_sizes = {
        # Ollama
        "nomic-embed-text": 768,
        "mxbai-embed-large": 1024,
        "all-minilm": 384,
        "snowflake-arctic-embed": 1024,
        # OpenAI
        "text-embedding-3-small": 1536,
        "text-embedding-3-large": 3072,
        "text-embedding-ada-002": 1536,
        # Qwen
        "qwen/qwen3-embedding-8b": 4096,
    }

    if model in known_sizes:
        return known_sizes[model]

    # Default per provider
    defaults = {"ollama": 768, "openai": 1536, "openrouter": 1536}
    return defaults.get(provider, 768)


def _embed_ollama(text: str, config: Config) -> list[float]:
    """Embedding via Ollama locale."""
    host = config.embeddings.ollama_host
    try:
        response = requests.post(
            f"{host}/api/embed",
            json={"model": config.embeddings.model, "input": text},
            timeout=30,
        )
        response.raise_for_status()
        return response.json()["embeddings"][0]

    except requests.ConnectionError:
        raise ConnectionError(
            f"Cannot connect to Ollama at {host}. "
            f"Make sure Ollama is running: ollama serve"
        )
    except requests.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(
                f"Model '{config.embeddings.model}' not found in Ollama. "
                f"Pull it first: ollama pull {config.embeddings.model}"
            )
        raise


def _embed_openai(text: str, config: Config) -> list[float]:
    """Embedding via OpenAI API."""
    api_key = config.embeddings.openai_api_key or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError(
            "OpenAI API key not configured. Set embeddings.openai_api_key in config.yaml "
            "or export OPENAI_API_KEY"
        )

    response = requests.post(
        f"{config.embeddings.openai_base_url}/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.embeddings.model,
            "input": text,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def _embed_openrouter(text: str, config: Config) -> list[float]:
    """Embedding via OpenRouter API (compatibile OpenAI)."""
    api_key = config.embeddings.openrouter_api_key or os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key:
        raise ValueError(
            "OpenRouter API key not configured. Set embeddings.openrouter_api_key in config.yaml "
            "or export OPENROUTER_API_KEY"
        )

    response = requests.post(
        f"{config.embeddings.openrouter_base_url}/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": config.embeddings.model,
            "input": text,
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]
