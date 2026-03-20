---
description: "Inizializza claude-memory: struttura .memory/, hook, e opzionalmente rigenera CLAUDE.md da codebase"
argument-hint: "[--project-name nome] [--no-index] [--rebuild-claude]"
---

# /memory-init — Setup Memoria Persistente

Devi inizializzare il sistema di memoria persistente `claude-memory` nel progetto corrente.

## Argomenti

$ARGUMENTS

---

## STEP 1: Installa il pacchetto Python

Verifica se `claude-memory` è già installato:
```bash
claude-memory --help 2>&1 | head -3
```

Se non trovato, cerca la directory del plugin e installa:
```bash
pip3 install --break-system-packages -e /path/to/claude-memory-plugin
```

---

## STEP 2: Esegui init

```bash
claude-memory init --project-name "$(basename $(pwd))"
```

Se l'utente ha passato `--no-index`, aggiungi `--no-index`.
Se l'utente ha passato `--project-name`, usa quel valore.

---

## STEP 3: Verifica

1. Controlla che esista `.memory/` con CONTEXT.md, DECISIONS.md, LEARNINGS.md, config.yaml, sessions/, checkpoints/
2. Controlla che `.claude/settings.json` contenga hook `claude_memory` con `python3`
3. Controlla che `CLAUDE.md` contenga `claude-memory:start`

---

## STEP 4: Rebuild CLAUDE.md (se --rebuild-claude)

**Se l'utente ha passato `--rebuild-claude`**, rigenera l'intero CLAUDE.md analizzando il codebase. Altrimenti salta questo step.

### 4.1 Analisi del Codebase

Analizza il progetto raccogliendo informazioni da queste fonti (usa Agent in parallelo):

1. **Struttura**: `ls` root, app principali, directory chiave
2. **Stack**: `requirements.txt` / `pyproject.toml` / `package.json`
3. **Framework e pattern**: Django/Flask/Node, pattern architetturali
4. **Database**: modelli, config DB
5. **Frontend**: template, framework JS, CSS/design system
6. **Config**: `settings.py` / `.env.example` / `docker-compose.yml`
7. **Git**: convenzioni commit (`git log --oneline -20`)
8. **Comandi**: `Makefile`, `scripts/`, `manage.py`
9. **CLAUDE.md esistente**: preserva informazioni ancora valide
10. **`.claude/rules/`**: regole esistenti per convenzioni specifiche
11. **`.memory/DECISIONS.md`**: decisioni architetturali
12. **`.memory/LEARNINGS.md`**: errori e pattern consolidati
13. **Skill disponibili**: identifica skill installate

### 4.2 Genera il nuovo CLAUDE.md

Scrivi seguendo questa struttura. **MAX 38.000 caratteri**. Tabelle > prose. Mai frasi superflue. Se un'info è in una skill o rule, punta lì.

```markdown
# {Nome Progetto}

{1 riga: cosa fa il progetto}

- **Versione**: {dove trovarla}
- **Repo**: {nome repo}

---

## REGOLE CRITICHE

{Errori frequenti, cose da NON fare MAI. Tabella mapping errori.
Prendi da LEARNINGS.md e rules esistenti. Solo regole davvero importanti.}

---

## Stack Tecnologico

{Tabella o lista compatta: backend, frontend, DB, cache, servizi esterni.
Comandi principali (dev, build, deploy, migrate).}

---

## Convenzioni

{Naming, pattern architetturali, struttura file.
Solo quello che non è ovvio dal codice.}

---

## App / Moduli

{Lista app con 1 riga ciascuna.
Se skill documentano i dettagli, menzionale.}

---

## Frontend / Design System

{Se esiste design system custom, documenta in modo compatto.
Componenti principali, classi, pattern. Usa tabelle.
Se molto grande, solo regole critiche + punta a file di riferimento.}

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

In fondo al file, aggiungi:

```markdown
<!-- claude-memory:start -->
## Memory System

Memoria persistente in `.memory/`. **CONTEXT.md** (stato progetto), **DECISIONS.md** (decisioni architetturali), **LEARNINGS.md** (errori/pattern). Decisioni: `## YYYY-MM-DD: Titolo` + Contesto/Decisione/Motivo/File. Learnings: `### Titolo (scoperto: YYYY-MM-DD)` + Errore/Correzione/Regola. Aggiorna CONTEXT.md dopo obiettivi significativi. Non toccare `.memory/sessions/`.
<!-- claude-memory:end -->
```

### 4.3 Scrivi e Verifica

1. Scrivi il nuovo `CLAUDE.md` con Write
2. Verifica: `wc -c CLAUDE.md` (deve essere < 40000)
3. Se sfora, comprimi sezioni più lunghe (tipicamente Frontend/Design System)
4. Mostra: dimensione finale, sezioni incluse, cosa tagliato vs vecchio

---

## STEP 5: Report

Mostra all'utente:
- Stato installazione
- File creati / aggiornati
- Hook configurati
- Se CLAUDE.md è stato rigenerato (e dimensione)
- Se Qdrant/Ollama raggiungibili (non bloccante)
