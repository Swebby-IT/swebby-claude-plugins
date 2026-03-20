"""Test per memory/manager.py."""

import json
from pathlib import Path

import pytest


@pytest.fixture
def project(tmp_path):
    """Crea un progetto temporaneo con struttura .memory/."""
    memory_dir = tmp_path / ".memory"
    memory_dir.mkdir()
    (memory_dir / "sessions").mkdir()
    (memory_dir / "checkpoints").mkdir()
    return tmp_path


@pytest.fixture
def project_with_files(project):
    """Progetto con file di memoria pre-popolati."""
    memory_dir = project / ".memory"

    (memory_dir / "CONTEXT.md").write_text(
        "# Project Context (auto-updated)\n"
        "Last updated: 2026-03-20 10:00\n\n"
        "## Current State\n"
        "- Progetto: test\n\n"
        "## Work in Progress\n"
        "- Task 1\n",
        encoding="utf-8",
    )

    (memory_dir / "DECISIONS.md").write_text(
        "# Architectural Decisions\n\n"
        "## 2026-03-18: Prima decisione\n"
        "- **Contesto**: test\n"
        "- **Decisione**: fare A\n\n"
        "## 2026-03-19: Seconda decisione\n"
        "- **Contesto**: test2\n"
        "- **Decisione**: fare B\n\n"
        "## 2026-03-20: Terza decisione\n"
        "- **Contesto**: test3\n"
        "- **Decisione**: fare C\n",
        encoding="utf-8",
    )

    (memory_dir / "LEARNINGS.md").write_text(
        "# Learnings & Patterns\n\n"
        "### Bug auth (scoperto: 2026-03-18)\n"
        "- **Errore**: crash\n\n"
        "### Fix deploy (scoperto: 2026-03-19)\n"
        "- **Errore**: timeout\n\n"
        "### Pattern API (scoperto: 2026-03-20)\n"
        "- **Errore**: 500\n",
        encoding="utf-8",
    )

    return project


def test_read_context_empty(project):
    from claude_memory.memory.manager import read_context

    assert read_context(project) == ""


def test_read_context(project_with_files):
    from claude_memory.memory.manager import read_context

    content = read_context(project_with_files)
    assert "Project Context" in content
    assert "Current State" in content


def test_read_decisions_all(project_with_files):
    from claude_memory.memory.manager import read_decisions

    content = read_decisions(project_with_files)
    assert "Prima decisione" in content
    assert "Terza decisione" in content


def test_read_decisions_last_n(project_with_files):
    from claude_memory.memory.manager import read_decisions

    content = read_decisions(project_with_files, last_n=1)
    assert "Terza decisione" in content
    assert "Prima decisione" not in content


def test_read_learnings_last_n(project_with_files):
    from claude_memory.memory.manager import read_learnings

    content = read_learnings(project_with_files, last_n=1)
    assert "Pattern API" in content
    assert "Bug auth" not in content


def test_append_decision(project_with_files):
    from claude_memory.memory.manager import append_decision, read_decisions

    append_decision(
        project_with_files,
        title="Nuova decisione",
        context="test context",
        decision="fare D",
        reason="motivo D",
        files=["file1.py", "file2.py"],
    )

    content = read_decisions(project_with_files)
    assert "Nuova decisione" in content
    assert "fare D" in content
    assert "file1.py" in content


def test_append_learning(project_with_files):
    from claude_memory.memory.manager import append_learning, read_learnings

    append_learning(
        project_with_files,
        title="Nuovo learning",
        error="errore X",
        correction="fix Y",
        rule="regola Z",
    )

    content = read_learnings(project_with_files)
    assert "Nuovo learning" in content
    assert "regola Z" in content


def test_read_checkpoint_none(project):
    from claude_memory.memory.manager import read_checkpoint

    assert read_checkpoint(project) is None


def test_read_checkpoint(project):
    from claude_memory.memory.manager import read_checkpoint

    checkpoint_file = project / ".memory" / "checkpoints" / ".session.json"
    checkpoint_file.write_text(
        json.dumps({"started_at": 1000, "files_modified": [{"path": "a.py", "timestamp": 1001}]}),
        encoding="utf-8",
    )

    data = read_checkpoint(project)
    assert data is not None
    assert len(data["files_modified"]) == 1


def test_update_context(project):
    from claude_memory.memory.manager import read_context, update_context

    (project / ".memory" / "CONTEXT.md").touch()
    update_context(project, "New state info")

    content = read_context(project)
    assert "Project Context" in content
    assert "New state info" in content
