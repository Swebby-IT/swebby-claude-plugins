---
description: "Inizializza il sistema di memoria persistente claude-memory nel progetto corrente"
argument-hint: "[--project-name nome] [--no-index]"
---

# /memory-init — Setup Memoria Persistente

Devi inizializzare il sistema di memoria persistente `claude-memory` nel progetto corrente.

## Argomenti

$ARGUMENTS

---

## STEP 1: Installa il pacchetto Python

Cerca la directory del plugin claude-memory-plugin (dovrebbe essere nella directory dei plugin installati). Poi installa con pip:

```bash
pip3 install -e /path/to/claude-memory-plugin
```

Se pip3 non funziona, prova con `pip` o `python3 -m pip install -e`.

Se l'installazione fallisce per pip troppo vecchio, aggiorna prima pip:
```bash
python3 -m pip install --upgrade pip
```

**Verifica** che il comando funzioni:
```bash
claude-memory --help
```

---

## STEP 2: Esegui init

Lancia il comando CLI per creare la struttura `.memory/` e configurare gli hook:

```bash
claude-memory init --project-name "$(basename $(pwd))"
```

Se l'utente ha passato `--no-index` negli argomenti, aggiungi `--no-index`.
Se l'utente ha passato `--project-name`, usa quel valore.

---

## STEP 3: Verifica

1. Controlla che esista `.memory/` con i file:
   - `.memory/CONTEXT.md`
   - `.memory/DECISIONS.md`
   - `.memory/LEARNINGS.md`
   - `.memory/config.yaml`
   - `.memory/sessions/`
   - `.memory/checkpoints/`

2. Controlla che `.claude/settings.json` contenga gli hook `claude_memory`

3. Controlla che `CLAUDE.md` contenga la sezione `claude-memory:start`

---

## STEP 4: Report

Mostra all'utente:
- Stato installazione
- File creati
- Hook configurati
- Se Qdrant/Ollama sono raggiungibili o meno (non bloccante)

Se qualcosa fallisce, spiega come risolvere.
