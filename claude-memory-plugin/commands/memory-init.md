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

**Se l'utente ha passato `--rebuild-claude`**, rigenera il CLAUDE.md. Altrimenti salta questo step.

### REGOLA FONDAMENTALE

Il CLAUDE.md **DEVE** contenere TUTTA la documentazione necessaria per lavorare sul progetto. Non è un riassuntino — è il documento di riferimento completo. Se il CLAUDE.md esistente contiene informazioni valide, **DEVI preservarle e migliorarle**, non buttarle via.

### 4.1 Leggi PRIMA il CLAUDE.md esistente

```bash
cat CLAUDE.md
```

Questo è il punto di partenza. **Non partire mai da zero.** Analizza:
- Quali sezioni sono ancora valide e accurate?
- Quali mancano o sono obsolete?
- Quali possono essere compattate senza perdere informazioni?

### 4.2 Analisi del Codebase (per integrare/aggiornare)

Analizza il progetto per verificare e completare il CLAUDE.md esistente:

1. **Struttura**: `ls` root, app principali, directory chiave
2. **Stack**: `requirements.txt` / `pyproject.toml` / `package.json`
3. **Framework e pattern**: Django/Flask/Node, pattern architetturali
4. **Frontend**: template, framework JS, CSS/design system
5. **Config**: `settings.py` / `.env.example`
6. **Git**: convenzioni commit (`git log --oneline -20`)
7. **`.claude/rules/`**: regole esistenti
8. **`.memory/DECISIONS.md`**: decisioni architetturali
9. **`.memory/LEARNINGS.md`**: errori e pattern consolidati
10. **Skill disponibili**: identifica skill installate

### 4.3 Riscrivi il CLAUDE.md

**Regole di scrittura:**

1. **MAX 39.000 caratteri** — verifica con `wc -c CLAUDE.md`
2. **Preserva TUTTO il contenuto valido** del CLAUDE.md esistente — regole critiche, mapping errori, tabelle componenti, convenzioni
3. **Compatta la prosa**, mai il contenuto tecnico — le tabelle di mapping CSS, i componenti, le regole vanno mantenute integrali
4. **Se una sezione del vecchio è troppo lunga**, sposta il dettaglio in un file separato (es. `.claude/rules/swcss-components.md`) e punta lì dal CLAUDE.md. NON cancellare l'informazione
5. **Tabelle > prose** — converti paragrafi in tabelle dove possibile
6. **Se l'info è in una skill o rule**, punta lì invece di duplicare
7. **Ogni path, classe, comando citato deve esistere davvero** — verifica nel codebase
8. **Aggiungi info mancanti** trovate nell'analisi del codebase
9. **Rimuovi info obsolete** che non corrispondono più al codice attuale

**Struttura del CLAUDE.md** (adatta al progetto, queste sono le sezioni tipiche):

- Header progetto (nome, versione, repo)
- Regole critiche / errori da non fare
- Stack tecnologico + comandi principali
- Convenzioni naming e pattern
- App / Moduli (lista con descrizione)
- Frontend / Design System (se presente — questa è spesso la sezione più grande e più importante, NON tagliarla)
- Tool MCP
- Versioning e Git
- Regole per modulo (punta a `.claude/rules/`)
- Sezione memory (tra i marker `claude-memory:start/end`)

**In fondo al file**, mantieni la sezione memory tra i marker.

### 4.4 Scrivi e Verifica

1. Scrivi il nuovo `CLAUDE.md` con Write
2. Verifica: `wc -c CLAUDE.md` — deve essere < 40000
3. Se sfora: sposta sezioni di dettaglio in `.claude/rules/*.md` (NON eliminarle)
4. Mostra all'utente: dimensione finale, cosa è cambiato rispetto al vecchio, eventuali sezioni spostate in rules

---

## STEP 5: Report

Mostra all'utente:
- Stato installazione
- File creati / aggiornati
- Hook configurati
- Se CLAUDE.md è stato rigenerato (dimensione prima → dopo)
- Se Qdrant/Ollama raggiungibili (non bloccante)
