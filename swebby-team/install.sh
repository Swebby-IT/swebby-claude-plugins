#!/bin/bash

# ═══════════════════════════════════════════
#  🎯 Swebby Team — Installer
#  Orchestratore multi-agente per Claude Code
# ═══════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TARGET_DIR="${1:-.}"

echo ""
echo "🎯 Swebby Team — Installer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
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
echo "✅ Settings installati"

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
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎉 Swebby Team installato!"
echo ""
echo "Comandi disponibili in Claude Code:"
echo "  /orchestrate  — Task completo (research → develop → review)"
echo "  /research     — Solo fase di ricerca"
echo "  /develop      — Solo fase di sviluppo"
echo "  /review       — Solo verifica e code review"
echo "  /plan         — Genera piano senza eseguire"
echo ""
