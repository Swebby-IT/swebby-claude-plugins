#!/bin/bash

# ═══════════════════════════════════════════
#  🎯 Swebby Team — Uninstaller
# ═══════════════════════════════════════════

set -e

TARGET_DIR="${1:-.}"

echo ""
echo "🗑️  Swebby Team — Uninstaller"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Rimuovi commands
for cmd in orchestrate research develop review plan; do
    if [ -f "$TARGET_DIR/.claude/commands/$cmd.md" ]; then
        rm "$TARGET_DIR/.claude/commands/$cmd.md"
        echo "✅ Rimosso /.$cmd"
    fi
done

# Ripristina settings backup se esiste
if [ -f "$TARGET_DIR/.claude/settings.json.bak" ]; then
    mv "$TARGET_DIR/.claude/settings.json.bak" "$TARGET_DIR/.claude/settings.json"
    echo "✅ Settings ripristinati dal backup"
fi

echo ""
echo "⚠️  CLAUDE.md non è stato modificato — rimuovi manualmente"
echo "   la sezione 'Orchestrator Plugin' se presente."
echo ""
echo "🎉 Swebby Team disinstallato."
echo ""
