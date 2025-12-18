# Multi-Agent Orchestration Skill

Questa skill fornisce orchestrazione intelligente multi-agente con auto-scaling basato sulla complessità del task.

## Scelta del Modello per gli Agenti

I comandi `/implement` e `/plan` supportano il parametro `--model`:

```
/implement <task> --model=sonnet    # Default - bilanciato
/implement <task> --model=opus      # Massima qualità
/implement <task> --model=haiku     # Economico
```

| Modello | Quando Usare | Costo Relativo |
|---------|--------------|----------------|
| **haiku** | Task semplici, rename, fix minori | $ |
| **sonnet** | Task standard, feature medie (DEFAULT) | $$ |
| **opus** | Task complessi, refactoring critici, decisioni architetturali | $$$ |

Il modello selezionato viene passato a TUTTI gli agenti lanciati.

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

### 2.5 FASE DIPENDENZE: Analisi Grafo (CRITICA)

**PRIMA di pianificare**, costruisci il grafo delle dipendenze tra i file identificati:

#### 2.5.1 Estrazione Import

Per ogni file da modificare, identifica:
- **Python:** `from X import Y`, `import X`
- **JS/TS:** `import { } from '...'`, `require('...')`
- **Altri:** pattern di import specifici del linguaggio

#### 2.5.2 Costruzione Grafo

```markdown
| File | Importa da | Importato da |
|------|------------|--------------|
| models/user.py | - | services/, routes/ |
| services/user.py | models/user.py | routes/user.py |
| routes/user.py | services/, models/ | - |
```

#### 2.5.3 Topological Sort

Ordina i file per ordine di modifica:
1. **File foglia** (nessuna dipendenza) → modificare PRIMA
2. **File intermedi** (dipendono da foglie) → modificare DOPO
3. **File radice** (dipendono da tutti) → modificare ULTIMO

```
Esempio:
models/ → services/ → routes/ → tests/
   1          2           3         4
```

#### 2.5.4 Rilevamento Cicli

Se `A importa B` e `B importa A`:
- **Dipendenza circolare** rilevata
- Entrambi i file devono essere modificati dallo **STESSO agente**
- NON possono essere parallelizzati

#### 2.5.5 Implicazioni per Parallelismo

```
File con dipendenze dirette  → SEQUENZIALE (rispetta ordine)
File senza dipendenze        → PARALLELO (massima efficienza)
File in ciclo               → STESSO AGENTE
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

#### 4.1.1 REGOLA TASK ATOMICI (CRITICA)

**I subagenti Sonnet funzionano meglio con task ATOMICI.**

Un task è atomico quando:
- Ha **UNA SOLA responsabilità** chiara
- Può essere completato **senza decisioni ambigue**
- Ha **input e output ben definiti**
- **Non richiede conoscenza** di altri task in parallelo

```
┌─────────────────────────────────────────────────────────────────┐
│                    TASK ATOMICO vs NON ATOMICO                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ NON ATOMICO (troppo vago/complesso):                        │
│  "Implementa l'autenticazione utente"                           │
│  → Troppe decisioni da prendere, troppi file                    │
│                                                                 │
│  ✅ ATOMICO (specifico):                                        │
│  "Aggiungi funzione validate_password() in auth/validators.py   │
│   che verifica lunghezza >= 8 e almeno un numero"               │
│  → Una funzione, un file, criteri chiari                        │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ NON ATOMICO:                                                 │
│  "Refactoring del modulo users"                                 │
│                                                                 │
│  ✅ ATOMICO:                                                     │
│  "Rinomina la funzione get_user() in fetch_user_by_id()         │
│   nel file users/queries.py, linee 45-60"                       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ❌ NON ATOMICO:                                                 │
│  "Aggiungi validazione ai form"                                 │
│                                                                 │
│  ✅ ATOMICO:                                                     │
│  "Nel componente LoginForm.tsx, aggiungi validazione email      │
│   usando il pattern regex già presente in utils/validators.ts"  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Decomposizione Task Complessi:**

Se hai un task complesso, DECOMPONILO in task atomici:

```
Task complesso: "Aggiungi endpoint REST per creare utenti"

Decomposto in task atomici:
├── Task 1: Crea schema Pydantic UserCreate in schemas/user.py
├── Task 2: Crea funzione create_user() in services/user.py
├── Task 3: Crea endpoint POST /users in routes/user.py
└── Task 4: Aggiungi test per endpoint in tests/test_user.py

Ogni task → 1 agente con istruzioni specifiche
```

**Checklist Task Atomico:**

Prima di assegnare un task a un agente, verifica:
- [ ] Il task ha UNA SOLA responsabilità?
- [ ] Le istruzioni sono così specifiche che non servono decisioni?
- [ ] L'output atteso è un esempio concreto di codice?
- [ ] Un developer junior potrebbe completarlo senza chiedere?

Se qualsiasi risposta è NO → decomponi ulteriormente.

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

**REGOLA CRITICA:** I subagenti Sonnet NON hanno accesso al contesto della conversazione.
Devi fornire TUTTE le informazioni necessarie nel prompt del task.

Per ogni agente, fornisci **OBBLIGATORIAMENTE** tutti questi campi:

```markdown
## Task per Agente #N

**Obiettivo:** [descrizione chiara e completa di cosa deve fare]

**Razionale:** [PERCHÉ questa modifica è necessaria - aiuta l'agente a fare scelte migliori]

**File da modificare:**
- `path/file.py` linee X-Y

**Istruzioni PASSO-PASSO:**
1. [azione specifica con dettagli implementativi]
2. [azione specifica con dettagli implementativi]
3. [azione specifica con dettagli implementativi]

**Contesto codice ATTUALE (OBBLIGATORIO):**
```[linguaggio]
[SEMPRE includere lo snippet di codice esistente che verrà modificato]
[Includere anche codice circostante rilevante per capire il contesto]
```

**Pattern e convenzioni da seguire:**
- Naming: [camelCase/snake_case/etc.]
- Import style: [esempio da seguire]
- Error handling: [pattern usato nel progetto]
- [Altri pattern rilevanti del codebase]

**Output atteso:**
[descrizione PRECISA del risultato, con esempio di come dovrebbe apparire il codice]

**NON modificare:**
- [file/sezioni specifiche da non toccare]
- [funzionalità da preservare]

**Dipendenze:**
- Questo task dipende da: [nessuno / Task #X]
- Altri task dipendono da questo: [nessuno / Task #Y]
```

**ESEMPIO CONCRETO:**

```markdown
## Task per Agente #3

**Obiettivo:** Aggiungere validazione email nella funzione create_user

**Razionale:** Gli utenti possono attualmente registrarsi con email malformate,
causando errori nei sistemi di notifica downstream. Serve validazione frontend+backend.

**File da modificare:**
- `src/users/services.py` linee 45-55

**Istruzioni PASSO-PASSO:**
1. Aggiungere `import re` in cima al file (dopo gli altri import standard)
2. Creare funzione `is_valid_email(email: str) -> bool` PRIMA di create_user
3. Usare regex pattern RFC 5322 semplificato: `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
4. In create_user, aggiungere validazione come PRIMA riga della funzione
5. Lanciare `ValueError` con messaggio che include l'email invalida

**Contesto codice ATTUALE (OBBLIGATORIO):**
```python
# src/users/services.py
from typing import Optional
from .models import User
from .exceptions import UserExistsError

def create_user(email: str, name: str) -> User:
    """Crea un nuovo utente nel sistema."""
    if User.objects.filter(email=email).exists():
        raise UserExistsError(f"User {email} already exists")
    user = User(email=email, name=name)
    user.save()
    return user
```

**Pattern e convenzioni da seguire:**
- Naming: snake_case per funzioni
- Import: standard library first, then local imports
- Docstring: già presente, mantenere stile Google
- Exceptions: usare ValueError per input invalidi (pattern esistente)

**Output atteso:**
```python
import re  # aggiunto

def is_valid_email(email: str) -> bool:
    """Valida formato email."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def create_user(email: str, name: str) -> User:
    """Crea un nuovo utente nel sistema."""
    if not is_valid_email(email):
        raise ValueError(f"Invalid email format: {email}")
    # resto invariato...
```

**NON modificare:**
- La firma della funzione create_user
- La logica di controllo UserExistsError
- Altri file

**Dipendenze:**
- Questo task dipende da: nessuno
- Altri task dipendono da questo: Task #5 (test)
```

#### 5.1.1 CHECKLIST VALIDAZIONE PRE-LANCIO (OBBLIGATORIA)

**PRIMA di lanciare OGNI agente**, verifica che il tuo prompt contenga TUTTI questi elementi:

```
┌─────────────────────────────────────────────────────────────────┐
│  CHECKLIST VALIDAZIONE PROMPT - NON LANCIARE SE INCOMPLETO     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  [ ] OBIETTIVO: Descrizione chiara e completa?                 │
│      ❌ "Modifica il file" → troppo vago                        │
│      ✅ "Aggiungi validazione email nella funzione X"          │
│                                                                 │
│  [ ] RAZIONALE: Spiegato PERCHÉ serve questa modifica?         │
│      ❌ mancante                                                │
│      ✅ "Per prevenire registrazioni con email malformate"     │
│                                                                 │
│  [ ] FILE + LINEE: Path esatto e range linee specifico?        │
│      ❌ "modifica services.py"                                  │
│      ✅ "src/users/services.py linee 45-60"                    │
│                                                                 │
│  [ ] CONTESTO CODICE: Hai incluso lo snippet ESISTENTE?        │
│      ❌ mancante o "vedi file"                                  │
│      ✅ Codice attuale copiato nel prompt                      │
│                                                                 │
│  [ ] ISTRUZIONI PASSO-PASSO: Azioni specifiche numerate?       │
│      ❌ "implementa la validazione"                             │
│      ✅ "1. Importa re  2. Crea funzione X  3. Chiama in Y"    │
│                                                                 │
│  [ ] PATTERN PROGETTO: Naming, import style, error handling?   │
│      ❌ mancante                                                │
│      ✅ "snake_case, import stdlib first, raise ValueError"    │
│                                                                 │
│  [ ] OUTPUT ATTESO: Esempio di come deve apparire il codice?   │
│      ❌ mancante o descrizione testuale                         │
│      ✅ Snippet di codice con risultato finale                 │
│                                                                 │
│  [ ] VINCOLI: Specificato cosa NON modificare?                 │
│      ❌ mancante                                                │
│      ✅ "NON modificare firma funzione, altri file"            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**SE MANCA ANCHE UN SOLO ELEMENTO:**
1. **NON lanciare l'agente**
2. Prima raccogli l'informazione mancante (leggi il file, analizza il contesto)
3. Completa il prompt
4. Poi lancia

**RICORDA:** L'agente Sonnet NON ha il tuo contesto. Se il prompt è incompleto, farà scelte arbitrarie o fallirà. È sempre meglio spendere 30 secondi a completare il prompt che sprecare un intero ciclo agente.

#### 5.2 Esecuzione Parallela

```
Task indipendenti → Lancia in PARALLELO (max efficienza)
Task con dipendenze → Lancia in SEQUENZA

Usa Task tool con run_in_background=true per parallelismo
```

#### 5.3 Shared Context Buffer (per Task Sequenziali)

Quando esegui task con DIPENDENZE (sequenziali), mantieni un buffer di contesto condiviso:

##### Dopo che Agente N completa:

1. **Estrai decisioni chiave:**
   - Naming usati (es. `user_id` non `userId`)
   - Pattern implementati (es. error handling)
   - Strutture dati create (es. nuovi campi, enum)
   - Import aggiunti

2. **Aggiungi al prompt di Agente N+1:**

```markdown
**Contesto da task precedenti:**
- Task #1 ha creato: `class UserSchema` con campo `email_verified: bool`
- Naming: snake_case
- Pattern errori: `raise HTTPException(status_code=X, detail=Y)`
- Import: `from pydantic import BaseModel`
```

##### Per Task Paralleli:

- NON puoi passare contesto (eseguono insieme)
- Specifica pattern e convenzioni **IDENTICI** in tutti i prompt
- Usa la sezione "Pattern e convenzioni" per garantire coerenza

##### Esempio Flusso

```
Task #1 (models/) → Completa
    ↓
Estrai: "creato enum UserStatus con ACTIVE, INACTIVE"
    ↓
Task #2 (services/) → Riceve: "usa UserStatus.ACTIVE"
    ↓
Estrai: "creato change_status(user_id, status)"
    ↓
Task #3 (routes/) → Riceve contesto completo
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
