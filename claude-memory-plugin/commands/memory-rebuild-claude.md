---
description: "Ristruttura CLAUDE.md: sposta dettaglio in .claude/rules/, ottimizza per lavorare con la memoria"
argument-hint: ""
---

# /memory-rebuild-claude — Ristrutturazione CLAUDE.md + Rules

Equivalente a `/memory-init --rebuild-claude` ma senza il setup. Ristruttura solo CLAUDE.md e rules.

Vedi il STEP 4 di `/memory-init` per le istruzioni complete. In sintesi:

1. **Leggi** CLAUDE.md esistente e `.claude/rules/`
2. **Analizza** il codebase per verificare accuratezza
3. **Sposta** tutto il dettaglio (design system, mapping CSS, tabelle grandi, pattern modulo) in `.claude/rules/*.md`
4. **Riscrivi** CLAUDE.md con solo l'essenziale (regole critiche, stack, convenzioni, puntatori a rules)
5. **Target**: CLAUDE.md 20-25k char (max 35k). Le rules non hanno limite.
6. **Verifica**: `wc -c CLAUDE.md`
7. **Mostra**: dimensione prima/dopo, rules create, cosa spostato
