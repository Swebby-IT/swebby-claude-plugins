---
description: "Rigenera CLAUDE.md: analizza codebase, preserva contenuto valido, compatta sotto 40k char"
argument-hint: ""
---

# /memory-rebuild-claude — Rigenerazione CLAUDE.md

Equivalente a `/memory-init --rebuild-claude` ma senza il setup. Rigenera solo il CLAUDE.md.

## REGOLA FONDAMENTALE

Il CLAUDE.md **DEVE** contenere TUTTA la documentazione necessaria per lavorare sul progetto. Se il CLAUDE.md esistente contiene informazioni valide, **DEVI preservarle e migliorarle**, non buttarle via. Non partire MAI da zero.

## Esecuzione

1. **Leggi il CLAUDE.md esistente** — questo è il punto di partenza
2. **Analizza il codebase** per verificare e completare (stack, rules, skills, memory, git log)
3. **Riscrivi** preservando tutto il contenuto valido, compattando la prosa, aggiungendo info mancanti
4. **MAX 39.000 char** — se sfora, sposta dettaglio in `.claude/rules/*.md` (NON eliminare)
5. **Verifica** con `wc -c CLAUDE.md`
6. **Mostra** dimensione prima/dopo e cosa è cambiato

Vedi `/memory-init` STEP 4 per le regole complete di scrittura.
