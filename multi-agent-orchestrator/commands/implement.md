---
description: Implementa una feature con orchestrazione intelligente multi-agente (analisi MCP → piano → auto-scaling → esecuzione parallela)
argument-hint: "<descrizione della modifica da implementare>"
---

# Comando: Implementa con Multi-Agent Orchestration

Stai per implementare: **$ARGUMENTS**

## FASE 1: Discovery MCP

### 1.1 Rileva Tool Semantici Disponibili

Prima di tutto, verifica quali MCP sono disponibili nel sistema:

```
Cerca tra i tool disponibili:
- mcp__code-search__*     → Ricerca semantica codice
- mcp__sourcegraph__*     → Sourcegraph intelligence
- mcp__github__search*    → GitHub code search
- mcp__*__semantic*       → Altri tool semantici
- mcp__*__search*         → Tool di ricerca generici
```

**Se trovi MCP semantici:** Procedi con Step 1.2
**Se NON trovi MCP semantici:** Salta a Step 1.3 (solo Grep)

### 1.2 Query Semantica (se MCP disponibile)

Esegui query precise con l'MCP semantico trovato:

1. **Query principale:** Cerca codice correlato a "$ARGUMENTS"
2. **Query di contesto:** Cerca file/funzioni che potrebbero essere impattati
3. **Query dipendenze:** Cerca import/export correlati

Registra i risultati:
```markdown
**MCP usato:** [nome]
**Query eseguite:**
1. "[query 1]" → [N risultati]
2. "[query 2]" → [N risultati]
**File rilevanti trovati:** [lista]
```

### 1.3 Verifica con Grep

**SEMPRE esegui questa verifica**, anche dopo ricerca semantica:

1. Usa Grep per confermare i file trovati
2. Cerca pattern specifici correlati alla feature
3. Identifica eventuali file mancati dalla ricerca semantica

```markdown
**Pattern cercati:**
1. "[pattern 1]" → [N match in M file]
2. "[pattern 2]" → [N match in M file]
**File aggiuntivi trovati:** [lista]
**Discrepanze con ricerca semantica:** [se presenti]
```

### 1.4 Lettura File Rilevanti

Leggi i file identificati per comprendere:
- Struttura esistente del codice
- Pattern e convenzioni usate
- Dipendenze e import
- Punti di modifica necessari

---

## FASE 2: Pianificazione Dettagliata

### 2.1 Analizza le Modifiche Necessarie

Per ogni file identificato, determina:
- **Sezioni da modificare** (linee specifiche)
- **Tipo di modifica** (nuovo/modifica/elimina)
- **Dipendenze** con altre modifiche

### 2.2 Crea Tabella Modifiche

```markdown
## Modifiche Pianificate

| # | File | Sezione | Tipo | Descrizione | Dipende da |
|---|------|---------|------|-------------|------------|
| 1 | path/file1.py | 45-60 | Modifica | [desc] | - |
| 2 | path/file1.py | 150-170 | Modifica | [desc] | - |
| 3 | path/file2.py | 10-40 | Nuovo | [desc] | #1 |
| 4 | path/file3.py | 80-100 | Modifica | [desc] | - |
```

### 2.3 Calcola Gruppi e Agenti

Applica le regole di scaling:

```markdown
## Calcolo Agenti

### Analisi Dipendenze
- Modifiche #1 e #3 → COLLEGATE (dipendenza)
- Modifiche #2 e #4 → INDIPENDENTI

### Raggruppamento
| Gruppo | Modifiche | Motivo | Agenti |
|--------|-----------|--------|--------|
| A | #1, #3 | Dipendenza diretta | 1 |
| B | #2 | Indipendente, stesso file ma >50 linee | 1 |
| C | #4 | File diverso, indipendente | 1 |

### Totale Agenti: 3
- Agente 1: Gruppo A (modifiche collegate)
- Agente 2: Gruppo B (sezione indipendente)
- Agente 3: Gruppo C (file indipendente)
```

### 2.4 Se Incerto, CHIEDI

Se hai dubbi su:
- Quale approccio usare
- Come raggruppare le modifiche
- Interpretazione dei requisiti

**USA AskUserQuestion** per chiedere conferma PRIMA di procedere.

---

## FASE 3: Presentazione Piano (OBBLIGATORIA)

### 3.1 Presenta il Piano Completo

```markdown
## Piano di Implementazione: $ARGUMENTS

### Obiettivo
[Descrizione chiara di cosa verrà realizzato]

### Analisi Effettuata
- **MCP Semantico:** [Si/No] - [nome se presente]
- **File analizzati:** [N]
- **Pattern identificati:** [lista breve]

### Modifiche Pianificate
[Tabella modifiche da 2.2]

### Strategia di Esecuzione
[Calcolo agenti da 2.3]

### Rischi Identificati
| Rischio | Probabilità | Mitigazione |
|---------|-------------|-------------|
| [rischio] | Alta/Media/Bassa | [come gestire] |

### Riepilogo
- **File da modificare:** N
- **Sezioni totali:** M
- **Agenti necessari:** X
- **Esecuzione:** Parallela/Mista/Sequenziale
```

### 3.2 FERMATI E ASPETTA APPROVAZIONE

**NON procedere senza conferma esplicita dell'utente.**

Chiedi:
> "Piano pronto con **X agenti**. Vuoi che proceda con l'implementazione?"

---

## FASE 4: Esecuzione Multi-Agente

### REGOLA CRITICA: USA SEMPRE IL TASK TOOL

**NON modificare MAI il codice direttamente.** Per OGNI modifica devi:
1. Usare il **Task tool**
2. Con `subagent_type` appropriato (vedi lista agenti sotto)
3. Il subagent Sonnet eseguirà la modifica

### 4.1 Agenti Disponibili

Scegli l'agente appropriato per ogni task:

| Tipo Task | subagent_type |
|-----------|---------------|
| Modifiche frontend/UI | `multi-agent-orchestrator:frontend-developer-1` (fino a -20) |
| Modifiche backend/logic | `multi-agent-orchestrator:backend-developer-1` (fino a -20) |
| Modifiche generiche | `multi-agent-orchestrator:code-modifier` |
| Bug fix | `multi-agent-orchestrator:bug-fixer` |
| Refactoring | `multi-agent-orchestrator:refactorer` |
| Test | `multi-agent-orchestrator:test-writer` |
| Review | `multi-agent-orchestrator:code-reviewer` |
| API | `multi-agent-orchestrator:api-developer` |
| Database | `multi-agent-orchestrator:database-specialist` |

### 4.2 Come Lanciare un Agente

Per OGNI task, usa il Task tool così:

```
Task tool:
- subagent_type: "multi-agent-orchestrator:backend-developer-1"
- prompt: "Task: [descrizione]\nFile: [path]\nIstruzioni: [dettagli]\nContesto: [codice]"
```

### 4.3 Task Paralleli (IMPORTANTE)

Per task INDIPENDENTI, lancia TUTTI gli agenti in UN SINGOLO messaggio:

```
Messaggio con 3 Task tool simultanei:

Task 1: subagent_type="multi-agent-orchestrator:backend-developer-1", prompt="..."
Task 2: subagent_type="multi-agent-orchestrator:backend-developer-2", prompt="..."
Task 3: subagent_type="multi-agent-orchestrator:frontend-developer-1", prompt="..."
```

**USA agenti numerati diversi** per task paralleli (backend-developer-1, backend-developer-2, ecc.)

### 4.4 Task Sequenziali

Per task con DIPENDENZE:
1. Lancia il primo agente
2. Attendi completamento con TaskOutput
3. Verifica risultato
4. Poi lancia il successivo

### 4.5 Formato Prompt per Agente

```
## Task per [nome-agente]

**Obiettivo:** [cosa deve fare]

**File da modificare:**
- `path/file.py` linee X-Y

**Istruzioni dettagliate:**
1. [passo 1]
2. [passo 2]

**Contesto codice attuale:**
[snippet rilevante]

**NON fare:**
- [vincolo 1]
- [vincolo 2]
```

---

## FASE 5: Verifica e Consolidamento

### 5.1 Verifica Ogni Risultato

Per ogni agente completato:
- [ ] Task completato come richiesto
- [ ] Nessun errore di sintassi
- [ ] Nessun conflitto con altri agenti
- [ ] Output conforme alle specifiche

### 5.2 Gestione Errori

Se un agente fallisce:
1. **Analizza** l'errore
2. **Decidi:** ri-lancia con istruzioni migliori o fix manuale
3. **Comunica** all'utente

### 5.3 Risolvi Conflitti

Se ci sono conflitti tra modifiche:
1. Identifica il conflitto
2. Determina la risoluzione corretta
3. Applica manualmente o ri-delega

---

## FASE 6: Report Finale

```markdown
## Implementazione Completata

### Riepilogo Esecuzione
- **Agenti lanciati:** X
- **Completati con successo:** Y
- **Errori gestiti:** Z

### Modifiche Apportate
| File | Modifiche | Agente | Status |
|------|-----------|--------|--------|
| path/file1.py | +20/-5 linee | #1 | OK |
| path/file2.py | +15/-0 linee | #2 | OK |

### Verifica
- [ ] Codice sintatticamente corretto
- [ ] Nessun conflitto
- [ ] Pattern consistenti

### Prossimi Passi Consigliati
1. Eseguire test: `[comando test]`
2. Review manuale dei file: [lista]
3. [Altri step se necessari]

### Note
[Osservazioni rilevanti per l'utente]
```

---

## Regole Fondamentali

1. **MAI** modificare codice direttamente - USA SEMPRE Task tool con subagent_type
2. **MAI** saltare la fase di discovery MCP
3. **SEMPRE** verificare con grep anche dopo ricerca semantica
4. **MAI** procedere senza piano approvato
5. **SEMPRE** usare Task tool per delegare a subagenti Sonnet
6. **SEMPRE** verificare i risultati di ogni subagent
7. **SEMPRE** lanciare in parallelo task indipendenti (multipli Task tool in un messaggio)
