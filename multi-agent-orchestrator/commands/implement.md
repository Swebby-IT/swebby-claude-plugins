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

### 4.1 Delegazione ai Subagenti

Per ogni task nel piano approvato, **delega a code-modifier** con istruzioni precise.

Esempio di delegazione:
```
Delego a code-modifier:

**Task:** Aggiungere validazione input nella funzione processOrder
**File da modificare:** src/orders/processor.py linee 45-60
**Specifiche:**
- Aggiungere controllo null per parametro `items`
- Validare che `total` sia positivo
- Lanciare ValueError con messaggio descrittivo se invalido

**Contesto:**
[snippet del codice attuale]

**NON fare:**
- Non modificare altre funzioni
- Non aggiungere import non necessari
```

### 4.2 Task Paralleli vs Sequenziali

**Task INDIPENDENTI:** Lancia in PARALLELO
- Delega tutti i task indipendenti contemporaneamente
- Ogni task va a un'istanza separata di code-modifier

**Task con DIPENDENZE:** Lancia in SEQUENZA
- Attendi completamento del task precedente
- Verifica risultato
- Poi delega il successivo

### 4.3 Monitora Esecuzione

Per ogni task delegato:
1. Attendi il completamento
2. Verifica il risultato riportato dall'agente
3. Se errore, decidi se ri-delegare con istruzioni corrette

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

1. **MAI** saltare la fase di discovery MCP
2. **SEMPRE** verificare con grep anche dopo ricerca semantica
3. **MAI** procedere senza piano approvato
4. **SEMPRE** usare i subagenti (code-modifier) per l'esecuzione
5. **SEMPRE** verificare i risultati di ogni subagent
6. **SEMPRE** lanciare in parallelo task indipendenti
