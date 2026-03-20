"""Test per gli hook."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def project(tmp_path):
    memory_dir = tmp_path / ".memory"
    memory_dir.mkdir()
    (memory_dir / "sessions").mkdir()
    (memory_dir / "checkpoints").mkdir()

    # Crea file di base
    (memory_dir / "CONTEXT.md").write_text(
        "# Project Context (auto-updated)\nLast updated: 2026-03-20\n\n## Current State\n- Test\n",
        encoding="utf-8",
    )
    (memory_dir / "LEARNINGS.md").write_text(
        "# Learnings & Patterns\n",
        encoding="utf-8",
    )
    (memory_dir / "DECISIONS.md").write_text(
        "# Architectural Decisions\n",
        encoding="utf-8",
    )
    (memory_dir / "config.yaml").write_text(
        "version: 1\nqdrant:\n  collection: test_memory\n"
        "memory:\n  semantic_search_on_start: false\n",
        encoding="utf-8",
    )

    return tmp_path


def test_post_tool_use_creates_checkpoint(project, monkeypatch):
    """PostToolUse deve creare/aggiornare il checkpoint."""
    monkeypatch.chdir(project)

    from claude_memory.hooks.post_tool_use import main

    hook_input = json.dumps({
        "tool_name": "Edit",
        "tool_input": {"file_path": "app/models.py"},
    })

    import io
    import sys

    monkeypatch.setattr("sys.stdin", io.StringIO(hook_input))

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    checkpoint_file = project / ".memory" / "checkpoints" / ".session.json"
    assert checkpoint_file.exists()

    data = json.loads(checkpoint_file.read_text())
    assert len(data["files_modified"]) == 1
    assert data["files_modified"][0]["path"] == "app/models.py"


def test_post_tool_use_skips_memory_files(project, monkeypatch):
    """PostToolUse non deve tracciare file in .memory/."""
    monkeypatch.chdir(project)

    from claude_memory.hooks.post_tool_use import main

    hook_input = json.dumps({
        "tool_name": "Edit",
        "tool_input": {"file_path": ".memory/CONTEXT.md"},
    })

    import io

    monkeypatch.setattr("sys.stdin", io.StringIO(hook_input))

    with pytest.raises(SystemExit) as exc_info:
        main()
    assert exc_info.value.code == 0

    checkpoint_file = project / ".memory" / "checkpoints" / ".session.json"
    assert not checkpoint_file.exists()
