"""Test per CLI."""

import json

import pytest
from click.testing import CliRunner

from claude_memory.cli import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def project(tmp_path, monkeypatch):
    """Progetto git temporaneo."""
    import subprocess

    subprocess.run(["git", "init"], cwd=str(tmp_path), capture_output=True)
    subprocess.run(
        ["git", "config", "user.email", "test@test.com"],
        cwd=str(tmp_path),
        capture_output=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test"],
        cwd=str(tmp_path),
        capture_output=True,
    )

    monkeypatch.chdir(tmp_path)
    return tmp_path


def test_init_creates_structure(runner, project):
    result = runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])
    assert result.exit_code == 0

    memory_dir = project / ".memory"
    assert memory_dir.exists()
    assert (memory_dir / "CONTEXT.md").exists()
    assert (memory_dir / "DECISIONS.md").exists()
    assert (memory_dir / "LEARNINGS.md").exists()
    assert (memory_dir / "config.yaml").exists()
    assert (memory_dir / "sessions").is_dir()
    assert (memory_dir / "checkpoints").is_dir()


def test_init_creates_hooks(runner, project):
    result = runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])
    assert result.exit_code == 0

    settings_file = project / ".claude" / "settings.json"
    assert settings_file.exists()

    settings = json.loads(settings_file.read_text())
    assert "hooks" in settings
    assert "SessionStart" in settings["hooks"]
    assert "Stop" in settings["hooks"]
    assert "PostToolUse" in settings["hooks"]


def test_init_creates_claude_md(runner, project):
    result = runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])
    assert result.exit_code == 0

    claude_md = project / "CLAUDE.md"
    assert claude_md.exists()
    content = claude_md.read_text()
    assert "claude-memory:start" in content
    assert "Memory System" in content


def test_init_no_overwrite(runner, project):
    """Il secondo init non sovrascrive i file esistenti."""
    runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])

    # Modifica CONTEXT.md
    context = project / ".memory" / "CONTEXT.md"
    context.write_text("Custom content", encoding="utf-8")

    runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])
    assert context.read_text() == "Custom content"


def test_init_gitignore(runner, project):
    result = runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])
    assert result.exit_code == 0

    gitignore = project / ".gitignore"
    assert gitignore.exists()
    assert ".memory/checkpoints/.session.json" in gitignore.read_text()


def test_status_not_initialized(runner, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = runner.invoke(cli, ["status"])
    assert "non inizializzato" in result.output


def test_status_initialized(runner, project):
    runner.invoke(cli, ["init", "--no-index", "--project-name", "test"])
    result = runner.invoke(cli, ["status"])
    assert result.exit_code == 0
    assert "Sessioni registrate" in result.output
    assert "CONTEXT.md" in result.output
