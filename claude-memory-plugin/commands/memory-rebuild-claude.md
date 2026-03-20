---
description: "Rigenera l'intero CLAUDE.md analizzando il codebase del progetto"
argument-hint: "[--full]"
---

# /memory-rebuild-claude — Rigenerazione Completa CLAUDE.md

Devi rigenerare l'intero `CLAUDE.md` del progetto analizzando il codebase. Il risultato deve essere un file completo, accurato e **sotto i 40.000 caratteri** (limite performance Claude Code).

## Argomenti

$ARGUMENTS

---

## FASE 1: Analisi del Codebase

Analizza il progetto raccogliendo informazioni da queste fonti (usa Agent in parallelo per velocizzare):

1. **Struttura progetto**: `ls` della root, app principali, directory chiave
2. **Stack tecnologico**: leggi `requirements.txt` / `pyproject.toml` / `package.json` / `Pipfile`
3. **Framework e pattern**: identifica Django/Flask/Node/etc, pattern architetturali
4. **Database**: cerca modelli, migration, config DB
5. **Frontend**: cerca template, framework JS, CSS/design system
6. **Config**: leggi `settings.py` / `.env.example` / `docker-compose.yml`
7. **Git**: branch strategy, convenzioni commit (`git log --oneline -20`)
8. **Comandi**: cerca `Makefile`, `scripts/`, `manage.py`, comandi custom
9. **CLAUDE.md esistente**: leggi quello attuale per preservare informazioni valide
10. **`.claude/rules/`**: leggi le rules esistenti per capire convenzioni specifiche
11. **`.memory/DECISIONS.md`**: leggi decisioni architetturali prese
12. **`.memory/LEARNINGS.md`**: leggi errori e pattern consolidati
13. **Skill disponibili**: identifica skill installate e cosa documentano

---

## FASE 2: Genera il CLAUDE.md

Scrivi il nuovo CLAUDE.md seguendo questa struttura. **OGNI sezione deve essere concisa e densa** — mai ripetere info, mai frasi superflue. Target: **sotto 38.000 char** per lasciare margine.

### Struttura obbligatoria

```markdown
# {Nome Progetto}

{1 riga: cosa fa il progetto}

- **Versione**: {dove trovarla}
- **Repo**: {nome repo}

---

## REGOLE CRITICHE

{Errori frequenti, cose da NON fare MAI. Tabella mapping errori se necessario.
Prendi da LEARNINGS.md e dalle rules esistenti. Solo le regole davvero importanti.}

---

## Stack Tecnologico

{Tabella o lista compatta: backend, frontend, DB, cache, servizi esterni.
Include comandi principali (dev, build, deploy, migrate).}

---

## Convenzioni

{Naming, pattern architetturali, struttura file.
Solo quello che non è ovvio dal codice.}

---

## App / Moduli

{Lista app con 1 riga di descrizione ciascuna.
Se ci sono skill che documentano i dettagli, menzionale qui.}

---

## Frontend / Design System

{Se esiste un design system custom, documentalo in modo compatto.
Componenti principali, classi, pattern. Usa tabelle.
Se è molto grande, metti solo le regole critiche e punta a file di riferimento.}

---

## Tool MCP

{Lista tool disponibili con 1 riga ciascuno.}

---

## Versioning e Git

{Regole commit, workflow, branch strategy.}

---

## Regole per Modulo

{Punta a `.claude/rules/` se esistono.}
```

### In fondo al file, aggiungi la sezione memory:

```markdown
<!-- claude-memory:start -->
## Memory System

Memoria persistente in `.memory/`. **CONTEXT.md** (stato progetto), **DECISIONS.md** (decisioni architetturali), **LEARNINGS.md** (errori/pattern). Decisioni: `## YYYY-MM-DD: Titolo` + Contesto/Decisione/Motivo/File. Learnings: `### Titolo (scoperto: YYYY-MM-DD)` + Errore/Correzione/Regola. Aggiorna CONTEXT.md dopo obiettivi significativi. Non toccare `.memory/sessions/`.
<!-- claude-memory:end -->
```

---

## FASE 3: Regole di Scrittura

1. **MAX 38.000 caratteri** — controlla con `wc -c CLAUDE.md` prima di scrivere
2. **Mai frasi introduttive** — vai dritto al contenuto
3. **Tabelle > prose** — usa tabelle per mapping, liste per elenchi
4. **No duplicazioni** — se un'info è in una skill o rule, punta lì invece di ripeterla
5. **Preserva regole critiche** — le regole dal vecchio CLAUDE.md che sono ancora valide vanno mantenute
6. **Verifica accuratezza** — ogni path, classe, comando deve esistere davvero nel codebase

---

## FASE 4: Scrivi e Verifica

1. Scrivi il nuovo `CLAUDE.md` con il tool Write
2. Verifica dimensione: `wc -c CLAUDE.md` (deve essere < 40000)
3. Se sfora, comprimi le sezioni più lunghe (tipicamente Frontend/Design System)
4. Mostra all'utente: dimensione finale, sezioni incluse, cosa è stato tagliato vs il vecchio
