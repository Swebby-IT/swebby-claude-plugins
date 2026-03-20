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

**Se l'utente ha passato `--rebuild-claude`**, ristruttura il CLAUDE.md e le rules. Altrimenti salta questo step.

### PRINCIPIO ARCHITETTURALE

Il contesto di Claude Code è diviso in **3 layer**. Il rebuild deve ottimizzare questa separazione:

| Layer | Cosa contiene | Dove |
|-------|--------------|------|
| **CLAUDE.md** | Solo l'essenziale: identità progetto, regole critiche (quelle che se violate rompono tutto), stack, convenzioni, comandi, puntatori a rules/skills/memory | `CLAUDE.md` (max 25.000 char) |
| **Rules** | Documentazione di dettaglio: componenti design system, tabelle mapping complete, pattern per modulo, regole specifiche per area | `.claude/rules/*.md` (auto-caricati per file) |
| **Memory** | Contesto dinamico: stato progetto, decisioni architetturali, learnings, sessioni passate | `.memory/` |

**CLAUDE.md DEVE essere snello (target 20-25k char)** perché condivide il contesto con la memoria. Se è troppo grande, la memoria non ha spazio per funzionare.

### 4.1 Leggi il CLAUDE.md esistente e le rules

```bash
cat CLAUDE.md
ls .claude/rules/
```

Leggi tutto. Identifica:
- Cosa è **critico** e deve restare nel CLAUDE.md (regole che se violate rompono il progetto)
- Cosa è **dettaglio** e va spostato in rules (tabelle componenti, mapping completi, design system reference)
- Cosa è **obsoleto** e va rimosso (verifica nel codebase)

### 4.2 Analisi del Codebase

Analizza per verificare e completare:

1. **Stack**: `requirements.txt` / `package.json`
2. **Framework**: Django/Flask/Node, pattern architetturali
3. **Frontend**: design system, CSS, JS
4. **Git**: `git log --oneline -20`
5. **`.claude/rules/`**: rules esistenti
6. **`.memory/DECISIONS.md`** e **`.memory/LEARNINGS.md`**
7. **Skill disponibili**

### 4.3 Crea/aggiorna le Rules

**SEMPRE** sposta in `.claude/rules/` il dettaglio che non serve avere sempre in contesto:

- **Tabelle componenti grandi** (es. design system completo) → `.claude/rules/design-system.md`
- **Mapping errori/classi CSS** → `.claude/rules/css-mapping.md`
- **Pattern specifici per modulo** → `.claude/rules/{modulo}.md`
- **Documentazione API/backend** → `.claude/rules/backend.md`
- **Regole frontend/template** → `.claude/rules/frontend.md`

Le rules si caricano automaticamente quando Claude lavora su file del modulo corrispondente. Non serve averle sempre in contesto.

Quando crei una rule:
- **Preserva integralmente** il contenuto che stai spostando — non riassumere, non tagliare
- **Aggiungi contesto**: se la rule era parte di una sezione più grande, aggiungi un header che spiega a cosa serve
- **Non duplicare**: se la rule esiste già, aggiornala invece di crearne una nuova

### 4.4 Riscrivi il CLAUDE.md

Il nuovo CLAUDE.md deve contenere SOLO:

```markdown
# {Nome Progetto}

{1 riga descrizione} — Versione: {dove trovarla}

---

## REGOLE CRITICHE

{SOLO le regole che se violate ROMPONO il progetto.
Tabella mapping errori frequenti se necessaria.
Max 20 regole. Se ce ne sono di più, le altre vanno in rules.}

---

## Stack e Comandi

{Stack tecnologico in tabella compatta.
Comandi principali: dev, build, deploy, migrate. Max 10 righe.}

---

## Convenzioni

{Naming, pattern architetturali. Solo quello non ovvio dal codice.}

---

## App / Moduli

{Lista app con max 1 riga ciascuna.}

---

## Frontend

{Solo regole critiche del design system.
Punta a `.claude/rules/design-system.md` per il dettaglio.}

Documentazione completa componenti: vedi `.claude/rules/design-system.md`

---

## Tool MCP

{1 riga per tool.}

---

## Git

{Regole commit, workflow. Max 5 righe.}

---

## Rules e Documentazione

Regole dettagliate per modulo in `.claude/rules/`:
{lista dei file .md con 1 riga di descrizione ciascuno}

Le rules si caricano automaticamente lavorando sui file del modulo.
```

Poi in fondo la sezione memory tra i marker `claude-memory:start/end`.

### 4.5 Scrivi e Verifica

1. **Prima** crea/aggiorna i file in `.claude/rules/` con il dettaglio spostato
2. **Poi** scrivi il nuovo `CLAUDE.md`
3. Verifica: `wc -c CLAUDE.md` — **target: 20-25k, max assoluto: 35k**
4. Se sfora: stai tenendo troppo dettaglio nel CLAUDE.md, sposta di più in rules
5. Mostra all'utente:
   - Dimensione CLAUDE.md: prima → dopo
   - File rules creati/aggiornati
   - Cosa spostato in rules
   - Cosa rimosso perché obsoleto

---

## STEP 5: Report

Mostra all'utente:
- Stato installazione
- File creati / aggiornati
- Hook configurati
- CLAUDE.md: dimensione e struttura
- Rules: file creati/aggiornati
- Qdrant/Ollama: raggiungibili o no (non bloccante)
