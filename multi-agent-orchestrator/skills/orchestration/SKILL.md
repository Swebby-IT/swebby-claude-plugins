# Multi-Agent Orchestration Skill

Questa skill fornisce orchestrazione intelligente multi-agente con auto-scaling basato sulla complessità del task.

## Quando Usare Questa Skill

Attiva questa skill quando:
- L'utente chiede modifiche al codice
- L'utente vuole implementare nuove feature
- L'utente vuole correggere bug
- È necessario coordinare modifiche su più file o sezioni di codice

## Principi di Orchestrazione

### 1. FASE DISCOVERY: Rilevamento MCP Disponibili

**PRIMA di qualsiasi ricerca**, identifica gli MCP disponibili nel sistema:

```
Controlla se sono disponibili:
- mcp__code-search__* → Ricerca semantica (PRIORITÀ ALTA)
- mcp__*search*       → Altri tool di ricerca semantica
- mcp__sourcegraph*   → Sourcegraph code intelligence
- mcp__github*        → GitHub code search
```

**Gerarchia di ricerca:**
1. **Ricerca Semantica (se MCP disponibile)** → Interroga PRIMA con query precise
2. **Grep/Glob** → Usa come VERIFICA o FALLBACK se semantica insufficiente
3. **Read** → Leggi i file identificati per contesto completo

### 2. FASE ANALISI: Raccolta Informazioni Intelligente

#### 2.1 Con MCP Semantico Disponibile

```markdown
STEP 1: Query semantica precisa
- Interroga l'MCP semantico con la query più specifica possibile
- Esempio: "function that handles user authentication"

STEP 2: Verifica con Grep
- Usa Grep per verificare i risultati
- Conferma che i file trovati siano corretti

STEP 3: Lettura approfondita
- Leggi i file rilevanti per contesto completo
```

#### 2.2 Senza MCP Semantico

```markdown
STEP 1: Grep pattern-based
- Cerca pattern specifici nel codebase
- Usa regex per query precise

STEP 2: Glob per struttura
- Mappa la struttura dei file rilevanti

STEP 3: Lettura file
- Leggi i file identificati
```

### 3. FASE PIANIFICAZIONE: Piano Dettagliato

**MAI** iniziare a scrivere codice senza un piano approvato.

#### 3.1 Struttura del Piano

```markdown
## Piano di Implementazione

### Obiettivo
[Descrizione chiara]

### Analisi Codebase
**Metodo usato:** [MCP semantico / Grep / Misto]
**File identificati:** [lista]
**Pattern trovati:** [descrizione]

### Modifiche Richieste

| # | File | Sezione/Linee | Tipo Modifica | Collegata a |
|---|------|---------------|---------------|-------------|
| 1 | path/file.py | 45-60 | Modifica | - |
| 2 | path/file.py | 120-130 | Modifica | #1 |
| 3 | path/other.py | 10-25 | Nuova | - |

### Valutazione Complessità
- Modifiche COLLEGATE (stesso contesto): [lista]
- Modifiche INDIPENDENTI: [lista]
- Complessità totale: [Bassa/Media/Alta]
```

#### 3.2 Gestione Incertezza

Se NON sei sicuro:
1. **Chiedi all'utente** prima di procedere
2. Presenta le opzioni disponibili
3. Spiega i trade-off di ogni approccio

### 4. FASE SCALING: Calcolo Automatico Agenti

#### 4.1 Regole di Scaling

```
REGOLA 1: Una sezione collegata → 1 AGENTE
- Modifiche nella stessa funzione/classe
- Modifiche che dipendono l'una dall'altra
- Modifiche consecutive nello stesso file

REGOLA 2: Sezioni scollegate → AGENTI MULTIPLI
- File diversi senza dipendenze → 1 agente per file
- Stesso file, sezioni distanti (>50 linee) → agenti separati se indipendenti
- Moduli/componenti diversi → agenti separati

REGOLA 3: Scaling massimo
- Minimo: 1 agente
- Massimo consigliato: 20 agenti
- Oltre 20: raggruppa task correlati
```

#### 4.2 Formula di Calcolo

```python
def calcola_agenti(modifiche):
    gruppi_indipendenti = raggruppa_per_indipendenza(modifiche)

    num_agenti = 0
    for gruppo in gruppi_indipendenti:
        if gruppo.stesso_contesto():
            num_agenti += 1
        else:
            num_agenti += len(gruppo.sezioni_indipendenti)

    return min(num_agenti, 20)  # Cap a 20
```

#### 4.3 Esempi Pratici

**Esempio 1: Modifica singola funzione**
```
File: utils.py, linee 10-30
→ 1 AGENTE
```

**Esempio 2: Modifica classe + test**
```
File: models.py, linee 50-80 (classe User)
File: test_models.py, linee 100-150 (test User)
→ 1 AGENTE (collegati logicamente)
```

**Esempio 3: Feature multi-file indipendenti**
```
File: api/users.py (nuovo endpoint)
File: api/products.py (nuovo endpoint)
File: api/orders.py (nuovo endpoint)
File: frontend/users.vue (nuova pagina)
File: frontend/products.vue (nuova pagina)
→ 5 AGENTI (tutti indipendenti)
```

**Esempio 4: Refactoring stesso file**
```
File: handlers.py
- Sezione 1: linee 20-50 (handler A)
- Sezione 2: linee 200-230 (handler B)
- Sezione 3: linee 400-450 (handler C)
→ 3 AGENTI (sezioni scollegate, >50 linee di distanza)
```

**Esempio 5: Refactoring massivo**
```
15 file diversi da modificare, tutti indipendenti
→ 15 AGENTI (uno per file)
```

### 5. FASE ESECUZIONE: Lancio Agenti

#### 5.1 Preparazione Task per Agente

Per ogni agente, fornisci:

```markdown
## Task per Agente #N

**Obiettivo:** [cosa deve fare]

**File da modificare:**
- `path/file.py` linee X-Y

**Specifiche dettagliate:**
1. [istruzione specifica 1]
2. [istruzione specifica 2]

**Contesto:**
[snippet di codice rilevante se necessario]

**Output atteso:**
[descrizione risultato]

**NON modificare:**
[file/sezioni da non toccare]
```

#### 5.2 Esecuzione Parallela

```
Task indipendenti → Lancia in PARALLELO (max efficienza)
Task con dipendenze → Lancia in SEQUENZA

Usa Task tool con run_in_background=true per parallelismo
```

### 6. FASE VERIFICA: Controllo Risultati

Dopo ogni batch di agenti:

1. **Verifica completamento** di ogni task
2. **Controlla conflitti** tra modifiche
3. **Valida sintassi** del codice modificato
4. **Se errori** → ri-delega con istruzioni corrette

### 7. Workflow Completo

```
[Utente] → Richiesta
    ↓
[Orchestratore] → Rileva MCP disponibili
    ↓
[Orchestratore] → Query semantica (se disponibile)
    ↓
[Orchestratore] → Verifica con Grep
    ↓
[Orchestratore] → Crea piano dettagliato
    ↓
[Orchestratore] → Calcola numero agenti
    ↓
[Utente] → Approva piano (o chiedi chiarimenti)
    ↓
[Orchestratore] → Lancia N agenti (parallelo/sequenza)
    ↓
[Agenti] → Eseguono modifiche
    ↓
[Orchestratore] → Verifica risultati
    ↓
[Orchestratore] → Report finale
```

## Best Practices

### DO
- Usa SEMPRE ricerca semantica se MCP disponibile
- Verifica SEMPRE con grep anche dopo ricerca semantica
- Calcola gli agenti PRIMA di procedere
- Chiedi conferma se incerto
- Lancia agenti in parallelo quando possibile
- Fornisci contesto completo ad ogni agente

### DON'T
- Non saltare la fase di discovery MCP
- Non fidarti ciecamente della ricerca semantica
- Non usare 1 solo agente per task complessi multi-file
- Non usare troppi agenti per modifiche collegate
- Non procedere senza piano approvato

## Comandi Disponibili

| Comando | Uso |
|---------|-----|
| `/implement <desc>` | Workflow completo: analisi → piano → scaling → esecuzione |
| `/plan <desc>` | Solo pianificazione con calcolo agenti |
| `/analyze <desc>` | Solo analisi codebase con MCP/grep |

## Output Piano Tipo

```markdown
## Piano di Implementazione

### Obiettivo
Implementare [feature]

### Analisi Effettuata
- **MCP Semantico:** [Si/No] - [nome MCP]
- **Query eseguite:** [lista]
- **File identificati:** [N file]

### Modifiche Pianificate

| # | File | Linee | Descrizione | Indipendente |
|---|------|-------|-------------|--------------|
| 1 | api/users.py | 45-80 | Nuovo endpoint | Si |
| 2 | api/users.py | 120-130 | Modifica validazione | No (#1) |
| 3 | models/user.py | 10-25 | Nuovo campo | Si |
| 4 | tests/test_users.py | nuovo | Test endpoint | No (#1) |

### Calcolo Agenti
- Gruppo 1: Modifiche #1, #2, #4 → **1 agente** (collegate)
- Gruppo 2: Modifica #3 → **1 agente** (indipendente)
- **TOTALE: 2 AGENTI**

### Conferma
Procedo con 2 agenti in parallelo?
```
