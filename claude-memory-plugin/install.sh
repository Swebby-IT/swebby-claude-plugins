#!/bin/bash

# ═══════════════════════════════════════════
#  claude-memory v0.4.2 — Installer
#  Memoria persistente per Claude Code
# ═══════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:-.}"

echo ""
echo "claude-memory v0.4.2 — Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "Progetto target: $(cd "$TARGET_DIR" && pwd)"
echo ""

# Crea struttura .claude
mkdir -p "$TARGET_DIR/.claude/commands"

# Copia commands
cp "$SCRIPT_DIR/commands/"*.md "$TARGET_DIR/.claude/commands/"
echo "Comandi installati in .claude/commands/"

# Installa pacchetto Python
echo "Installazione pacchetto Python..."
PIP_FLAGS="--break-system-packages"
if command -v pip3 &> /dev/null; then
    pip3 install $PIP_FLAGS -e "$SCRIPT_DIR" 2>&1 || {
        echo "pip3 install fallito, provo con python3 -m pip..."
        python3 -m pip install $PIP_FLAGS -e "$SCRIPT_DIR" 2>&1 || {
            echo "ATTENZIONE: installazione Python fallita."
            echo "Installa manualmente: pip3 install --break-system-packages -e $SCRIPT_DIR"
        }
    }
elif command -v pip &> /dev/null; then
    pip install $PIP_FLAGS -e "$SCRIPT_DIR" 2>&1
else
    echo "ATTENZIONE: pip non trovato. Installa manualmente: pip3 install --break-system-packages -e $SCRIPT_DIR"
fi

# Verifica installazione
if command -v claude-memory &> /dev/null; then
    echo "CLI claude-memory installata correttamente"
else
    echo "ATTENZIONE: comando claude-memory non trovato nel PATH"
    echo "Prova: python3 -m claude_memory.cli --help"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Installazione completata!"
echo ""
echo "Comandi disponibili in Claude Code:"
echo "  /memory-init    — Inizializza .memory/ nel progetto"
echo "  /memory-status  — Stato della memoria"
echo "  /memory-search  — Cerca nella memoria"
echo "  /memory-flush   — Salva memoria sessione"
echo "  /memory-reindex — Ri-indicizza in Qdrant"
echo ""
