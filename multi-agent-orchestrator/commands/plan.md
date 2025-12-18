---
description: Crea un piano dettagliato con calcolo automatico agenti, senza eseguire modifiche
argument-hint: "<descrizione della modifica da pianificare> [--model=sonnet|opus|haiku]"
---

# Comando: Pianifica con Auto-Scaling

Stai pianificando: **$ARGUMENTS**

## Step 0: Parsing Parametri

Analizza `$ARGUMENTS` per estrarre il parametro `--model`:

```
Se trovato --model=sonnet|opus|haiku:
  MODELLO_AGENTI = [valore]
  DESCRIZIONE = $ARGUMENTS senza --model=...
Altrimenti:
  MODELLO_AGENTI = sonnet (default)
  DESCRIZIONE = $ARGUMENTS
```

**Modelli disponibili:**
| Modello | Uso | Costo |
|---------|-----|-------|
| haiku | Task semplici | $ |
| sonnet | Standard (DEFAULT) | $$ |
| opus | Task complessi | $$$ |

---

## Istruzioni

Crea un piano dettagliato SENZA eseguire modifiche, includendo il calcolo automatico del numero di agenti necessari.

---

## Step 1: Discovery MCP

### 1.1 Identifica Tool Disponibili

Verifica quali MCP semantici sono disponibili:

```
Cerca:
- mcp__code-search__*
- mcp__sourcegraph__*
- mcp__*search*
- mcp__*semantic*
```

Registra:
```markdown
**MCP Semantici trovati:** [lista o "Nessuno"]
```

---

## Step 2: Analisi Codebase

### 2.1 Con MCP Semantico

Se disponibile:
1. Query semantica principale per "$ARGUMENTS"
2. Query per dipendenze e file correlati
3. Verifica risultati con Grep

### 2.2 Senza MCP Semantico

Se non disponibile:
1. Grep con pattern specifici
2. Glob per mappare struttura file
3. Read dei file rilevanti

### 2.3 Documenta Analisi

```markdown
## Analisi Codebase

### Metodo Usato
- **Ricerca semantica:** [Si/No] - [MCP usato]
- **Grep patterns:** [lista pattern]
- **File esaminati:** [N]

### Risultati Ricerca Semantica (se applicabile)
| Query | Risultati | File Rilevanti |
|-------|-----------|----------------|
| "[query]" | N | file1.py, file2.py |

### Risultati Grep
| Pattern | Match | File |
|---------|-------|------|
| "[pattern]" | N | file1.py:45, file2.py:80 |

### File Identificati per Modifica
1. `path/file1.py` - [motivo]
2. `path/file2.py` - [motivo]
```

---

## Step 2.5: Analisi Dipendenze

### 2.5.1 Costruisci Grafo Dipendenze

Per ogni file identificato, analizza gli import:

```markdown
| File | Importa da | Importato da |
|------|------------|--------------|
| models/user.py | - | services/, routes/ |
| services/user.py | models/user.py | routes/user.py |
| routes/user.py | services/, models/ | - |
```

### 2.5.2 Determina Ordine Esecuzione

```
Ordine (topological sort):
1. models/user.py (foglia)
2. services/user.py (dipende da 1)
3. routes/user.py (dipende da 1, 2)

Implicazioni:
- Se modifichi models → devi modificare PRIMA di services
- Task con dipendenze = SEQUENZIALI (non paralleli)
```

### 2.5.3 Rileva Cicli

Se A importa B e B importa A → stesso agente per entrambi.

---

## Step 3: Definizione Modifiche

### 3.1 Mappa Ogni Modifica

Per ogni file da modificare:

```markdown
## Modifiche Dettagliate

### File: `path/file1.py`

**Sezione 1:** Linee 45-60
- **Tipo:** Modifica
- **Descrizione:** [cosa cambiare]
- **Dipendenze:** Nessuna

**Sezione 2:** Linee 150-170
- **Tipo:** Nuovo codice
- **Descrizione:** [cosa aggiungere]
- **Dipendenze:** Richiede sezione 1 completata

### File: `path/file2.py`

**Sezione 1:** Linee 10-25
- **Tipo:** Modifica
- **Descrizione:** [cosa cambiare]
- **Dipendenze:** Nessuna
```

### 3.2 Tabella Riassuntiva

```markdown
| # | File | Linee | Tipo | Descrizione | Dipende da |
|---|------|-------|------|-------------|------------|
| 1 | file1.py | 45-60 | Modifica | [desc] | - |
| 2 | file1.py | 150-170 | Nuovo | [desc] | #1 |
| 3 | file2.py | 10-25 | Modifica | [desc] | - |
| 4 | file3.py | nuovo | Nuovo file | [desc] | #1, #3 |
```

---

## Step 4: Calcolo Automatico Agenti

### 4.1 Identifica Gruppi

Applica le regole:

```markdown
## Analisi Raggruppamento

### Regola 1: Dipendenze Dirette
Modifiche con dipendenze → stesso agente
- #1 → #2 (dipendenza) → Gruppo A
- #1, #3 → #4 (dipendenza multipla) → Include in Gruppo A

### Regola 2: Prossimità
Stesso file, <50 linee di distanza → stesso agente
- #1 e #2 in file1.py, distanza >50 linee → Possono essere separati SE indipendenti

### Regola 3: Indipendenza
File diversi senza dipendenze → agenti separati
- #3 (file2.py) indipendente → Gruppo B
```

### 4.2 Definizione Gruppi Finali

```markdown
## Gruppi di Lavoro

### Gruppo A: [Nome descrittivo]
- **Modifiche:** #1, #2, #4
- **Motivo raggruppamento:** Catena di dipendenze
- **Esecuzione:** Sequenziale interna
- **Agenti:** 1

### Gruppo B: [Nome descrittivo]
- **Modifiche:** #3
- **Motivo raggruppamento:** Indipendente
- **Esecuzione:** Parallela con altri gruppi
- **Agenti:** 1

### Riepilogo
| Gruppo | Modifiche | Agenti | Parallelo con |
|--------|-----------|--------|---------------|
| A | #1, #2, #4 | 1 | B |
| B | #3 | 1 | A |

**TOTALE AGENTI: 2**
```

### 4.3 Scenari di Scaling

Mostra come cambierebbe con requisiti diversi:

```markdown
## Scenari Alternativi

### Se tutte le modifiche fossero indipendenti
→ **4 agenti** (1 per modifica)

### Se ci fossero 20+ file indipendenti
→ **20 agenti** (cap massimo, con raggruppamento)

### Con dipendenze strette
→ **1 agente** (tutto sequenziale)
```

---

## Step 5: Piano Finale

### 5.1 Output Completo

```markdown
## Piano: $ARGUMENTS

### Obiettivo
[Descrizione chiara di cosa verrà realizzato]

### Analisi Effettuata
- **MCP Semantico:** [Si/No] - [nome]
- **File analizzati:** [N]
- **Query/Pattern usati:** [lista]

### Modifiche Pianificate
| # | File | Linee | Tipo | Descrizione | Dipende da |
|---|------|-------|------|-------------|------------|
[tabella completa]

### Calcolo Agenti
| Gruppo | Modifiche | Agenti | Esecuzione |
|--------|-----------|--------|------------|
[tabella gruppi]

**TOTALE: N AGENTI**

### Modello Selezionato
**[MODELLO_AGENTI]** (default: sonnet)

### Stima Costi
| Task | Agente | Modello | Complessità | Costo |
|------|--------|---------|-------------|-------|
| #1 | backend-1 | [MODELLO] | Media | ~$X.XX |
| #2 | frontend-1 | [MODELLO] | Bassa | ~$X.XX |
| **Totale** | | | | **~$X.XX** |

*Costi: haiku=$0.01, sonnet=$0.05, opus=$0.25 × complessità (1x/2x/3x)*

### Strategia Esecuzione
```
Gruppo A ─────┐
              ├──► Verifica ──► Completato
Gruppo B ─────┘
(parallelo)
```

### Rischi
| Rischio | Probabilità | Mitigazione |
|---------|-------------|-------------|
[tabella rischi]

### Domande Aperte (se presenti)
1. [domanda che richiede input utente]
2. [altra domanda]

### Prossimi Passi
1. Approva questo piano
2. Esegui `/implement $ARGUMENTS` per procedere
```

---

## Step 6: Gestione Incertezza

### Se hai dubbi, CHIEDI

Prima di finalizzare il piano, se non sei sicuro di:
- Interpretazione dei requisiti
- Quale approccio scegliere
- Come raggruppare le modifiche
- Rischi potenziali

**USA AskUserQuestion** per chiedere chiarimenti.

Esempio:
```
"Ho identificato 2 possibili approcci per [X]:
1. [Approccio A] - [pro/contro]
2. [Approccio B] - [pro/contro]

Quale preferisci?"
```

---

## Output

Il piano verrà presentato all'utente che potrà:
1. **Approvare** → Eseguire `/implement` con lo stesso argomento
2. **Modificare** → Richiedere cambiamenti al piano
3. **Chiarire** → Rispondere alle domande aperte
4. **Rifiutare** → Chiedere approccio diverso

**NON eseguire nessuna modifica al codice con questo comando.**
