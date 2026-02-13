#!/bin/bash

# ═══════════════════════════════════════════
#  🎯 Swebby Team v2 — Installer
#  Orchestratore multi-agente con Agent Teams
# ═══════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:-.}"

echo ""
echo "🎯 Swebby Team v2 — Installer (Agent Teams)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📁 Progetto target: $(cd "$TARGET_DIR" && pwd)"
echo ""

# Crea struttura .claude
mkdir -p "$TARGET_DIR/.claude/commands"

# Copia commands
cp "$SCRIPT_DIR/commands/"*.md "$TARGET_DIR/.claude/commands/"
echo "✅ Comandi installati in .claude/commands/"

# Copia settings (con backup se esiste)
if [ -f "$TARGET_DIR/.claude/settings.json" ]; then
    cp "$TARGET_DIR/.claude/settings.json" "$TARGET_DIR/.claude/settings.json.bak"
    echo "⚠️  settings.json esistente → backup creato (.bak)"
fi
cp "$SCRIPT_DIR/settings.json" "$TARGET_DIR/.claude/settings.json"
echo "✅ Settings installati (con CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1)"

# Verifica/abilita Agent Teams anche globalmente
GLOBAL_SETTINGS="$HOME/.claude/settings.json"
if [ -f "$GLOBAL_SETTINGS" ]; then
    if ! grep -q "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS" "$GLOBAL_SETTINGS" 2>/dev/null; then
        echo "⚠️  Agent Teams non trovato in settings globali."
        echo "    Per abilitare globalmente, esegui:"
        echo "    claude settings set env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1"
    else
        echo "✅ Agent Teams già abilitato globalmente"
    fi
fi

# Gestione CLAUDE.md (append se esiste, crea se no)
if [ -f "$TARGET_DIR/CLAUDE.md" ]; then
    echo "" >> "$TARGET_DIR/CLAUDE.md"
    echo "---" >> "$TARGET_DIR/CLAUDE.md"
    echo "" >> "$TARGET_DIR/CLAUDE.md"
    cat "$SCRIPT_DIR/CLAUDE.md" >> "$TARGET_DIR/CLAUDE.md"
    echo "✅ CLAUDE.md aggiornato (contenuto aggiunto in fondo)"
else
    cp "$SCRIPT_DIR/CLAUDE.md" "$TARGET_DIR/CLAUDE.md"
    echo "✅ CLAUDE.md creato"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Swebby Team v2 installato!"
echo ""
echo "Comandi disponibili in Claude Code:"
echo "  /run  — Lancia l'orchestratore con Agent Teams"
echo ""
echo "⚠️  IMPORTANTE: Assicurati che Agent Teams sia attivo:"
echo "  claude settings set env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1"
echo ""
