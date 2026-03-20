"""
Chunking semantico dei file markdown.

Splitta per heading (##, ###) mantenendo il contesto.
Ogni chunk include il heading come metadata.
Chunk troppo piccoli (< 50 char) vengono scartati.
Chunk troppo grandi (> 2000 char) vengono ulteriormente splittati.
"""

MAX_CHUNK_SIZE = 2000  # caratteri
MIN_CHUNK_SIZE = 50


def chunk_markdown(content: str, source_name: str) -> list[dict]:
    """
    Splitta un file markdown in chunk semantici per heading.

    Ritorna lista di dict con:
    - heading: titolo della sezione
    - text: contenuto della sezione (incluso heading)
    """
    chunks = []
    current_heading = source_name
    current_lines = []

    for line in content.split("\n"):
        if line.startswith("## ") or line.startswith("### "):
            if current_lines:
                text = "\n".join(current_lines).strip()
                if len(text) >= MIN_CHUNK_SIZE:
                    chunks.extend(_split_if_too_long(current_heading, text))

            current_heading = line.lstrip("#").strip()
            current_lines = [line]
        else:
            current_lines.append(line)

    # Ultimo chunk
    if current_lines:
        text = "\n".join(current_lines).strip()
        if len(text) >= MIN_CHUNK_SIZE:
            chunks.extend(_split_if_too_long(current_heading, text))

    return chunks


def _split_if_too_long(heading: str, text: str) -> list[dict]:
    """Splitta chunk troppo lunghi in sotto-chunk."""
    if len(text) <= MAX_CHUNK_SIZE:
        return [{"heading": heading, "text": text}]

    paragraphs = text.split("\n\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) > MAX_CHUNK_SIZE and current_chunk:
            chunks.append({"heading": heading, "text": current_chunk.strip()})
            current_chunk = para
        else:
            current_chunk += "\n\n" + para if current_chunk else para

    if current_chunk.strip() and len(current_chunk.strip()) >= MIN_CHUNK_SIZE:
        chunks.append({"heading": heading, "text": current_chunk.strip()})

    return chunks
