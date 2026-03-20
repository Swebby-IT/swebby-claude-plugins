"""Test per indexing/chunker.py (non richiede Qdrant/Ollama)."""

from claude_memory.indexing.chunker import chunk_markdown


def test_chunk_simple():
    content = """# Title

Some intro text that is long enough.

## Section One
Content of section one with some details.

## Section Two
Content of section two with more details.
"""
    chunks = chunk_markdown(content, "test.md")
    assert len(chunks) >= 2
    assert any("Section One" in c["heading"] for c in chunks)
    assert any("Section Two" in c["heading"] for c in chunks)


def test_chunk_skips_short():
    content = """## A
x
## B
This is a longer section with enough content to pass the minimum.
"""
    chunks = chunk_markdown(content, "test.md")
    # "x" è troppo corto, dovrebbe essere scartato
    assert all(len(c["text"]) >= 50 for c in chunks)


def test_chunk_splits_long():
    long_text = "## Big Section\n" + ("A" * 3000)
    chunks = chunk_markdown(long_text, "test.md")
    assert len(chunks) >= 1
    # Almeno un chunk dal contenuto lungo
    assert any(len(c["text"]) > 0 for c in chunks)


def test_chunk_empty():
    chunks = chunk_markdown("", "empty.md")
    assert chunks == []


def test_chunk_h3():
    content = """# Title

### Sub Section
Content of sub section with enough text to be included here.
"""
    chunks = chunk_markdown(content, "test.md")
    assert any("Sub Section" in c["heading"] for c in chunks)
