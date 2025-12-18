---
description: Implementa una feature con orchestrazione intelligente multi-agente (analisi MCP → piano → auto-scaling → esecuzione parallela)
argument-hint: "<descrizione della modifica da implementare> [--model=sonnet|opus|haiku]"
---

# Comando: Implementa con Multi-Agent Orchestration

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   🚨🚨🚨  REGOLE ASSOLUTE - LEGGI PRIMA DI FARE QUALSIASI COSA  🚨🚨🚨      ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║   TU (orchestratore) NON DEVI MAI MODIFICARE CODICE DIRETTAMENTE.            ║
║                                                                              ║
║   ❌ VIETATO USARE: Edit, Write, Update, NotebookEdit                        ║
║   ❌ VIETATO: Modificare file senza passare da un subagent                   ║
║   ❌ VIETATO: Procedere senza approvazione utente (FASE 3.2)                 ║
║                                                                              ║
║   ✅ OBBLIGATORIO: Usare SOLO Task tool con subagent_type                    ║
║   ✅ OBBLIGATORIO: Fermarsi a FASE 3.2 e chiedere approvazione               ║
║   ✅ OBBLIGATORIO: Delegare OGNI modifica a un agente specializzato          ║
║                                                                              ║
║   IL TUO RUOLO È:                                                            ║
║   - Analizzare e pianificare                                                 ║
║   - Leggere file (Read, Grep, Glob) per capire il contesto                   ║
║   - Creare il piano e chiedere approvazione                                  ║
║   - Lanciare subagent tramite Task tool per OGNI modifica                    ║
║   - Verificare i risultati                                                   ║
║                                                                              ║
║   IL TUO RUOLO NON È:                                                        ║
║   - Scrivere codice direttamente                                             ║
║   - Usare Edit/Write/Update                                                  ║
║   - Bypassare i subagent "per semplicità"                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

Stai per implementare: **$ARGUMENTS**

## FASE 0: Parsing Parametri (OBBLIGATORIA)

### 0.1 Estrai il Modello da $ARGUMENTS

**PRIMA DI TUTTO**, analizza `$ARGUMENTS` per estrarre `--model`:

```
INPUT: $ARGUMENTS

STEP 1: Cerca pattern --model=sonnet | --model=opus | --model=haiku

STEP 2: Estrai valore
  Se "--model=opus" trovato   → MODELLO = "opus"
  Se "--model=haiku" trovato  → MODELLO = "haiku"
  Se "--model=sonnet" trovato → MODELLO = "sonnet"
  Se NON trovato              → MODELLO = "sonnet" (default)

STEP 3: Rimuovi --model=xxx da $ARGUMENTS per ottenere DESCRIZIONE_TASK
```

**Modelli disponibili:**
| Modello | Uso Consigliato | Costo Relativo |
|---------|-----------------|----------------|
| `haiku` | Task semplici, economico | $ |
| `sonnet` | Task standard, bilanciato (DEFAULT) | $$ |
| `opus` | Task complessi, massima qualità | $$$ |

### 0.2 REGISTRA E RICORDA

**STAMPA subito questi valori** (li userai in FASE 4):

```markdown
## Configurazione Estratta
- **MODELLO:** [opus/sonnet/haiku]  ← USARE IN OGNI Task tool!
- **Task da implementare:** [descrizione senza --model]
```

⚠️ **RICORDA:** Questo MODELLO deve essere passato come parametro `model` in OGNI chiamata Task tool nella FASE 4!

---

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

## FASE 1.5: Analisi Dipendenze (CRITICA)

### 1.5.1 Costruisci il Grafo delle Dipendenze

**PRIMA di pianificare**, analizza le dipendenze tra i file identificati:

1. **Estrai Import** per ogni file:
   ```
   Python: from X import Y, import X
   JS/TS: import { } from '...', require('...')
   ```

2. **Mappa le Dipendenze**:
   ```markdown
   | File | Importa da | Importato da |
   |------|------------|--------------|
   | models/user.py | - | services/user.py, routes/user.py |
   | services/user.py | models/user.py | routes/user.py |
   | routes/user.py | services/user.py, models/user.py | - |
   ```

3. **Identifica Ordine di Modifica** (Topological Sort):
   - File "foglia" (senza dipendenze) → modificare PRIMA
   - File che dipendono da altri → modificare DOPO

   ```
   Ordine corretto:
   1. models/user.py (foglia - nessuna dipendenza)
   2. services/user.py (dipende da models)
   3. routes/user.py (dipende da services + models)
   ```

4. **Rileva Dipendenze Circolari**:
   - Se A importa B e B importa A → **STESSO AGENTE** per entrambi
   - Cicli complessi → raggruppa tutto il ciclo in UN agente

### 1.5.2 Output Analisi Dipendenze

```markdown
## Grafo Dipendenze

### Visualizzazione
```
models/user.py (foglia)
    ↓
services/user.py
    ↓
routes/user.py
    ↓
tests/test_user.py
```

### Implicazioni per Parallelismo
- **NON parallelizzabili:** modifiche su file con dipendenze dirette
- **Parallelizzabili:** modifiche su file senza dipendenze reciproche

### Ordine Esecuzione Consigliato
1. models/user.py → 2. services/user.py → 3. routes/user.py → 4. tests/
   (SEQUENZIALE per catena dipendenze)

oppure:

frontend/component.vue | backend/api.py | utils/helper.py
   (PARALLELO - nessuna dipendenza reciproca)
```

**REGOLA CRITICA:** Se il grafo mostra dipendenze, rispetta l'ordine.
NON lanciare in parallelo file che hanno dipendenze tra loro.

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

### 2.3.1 REGOLA TASK ATOMICI (CRITICA)

**Ogni task assegnato a un agente deve essere ATOMICO.**

Un task atomico ha:
- **UNA SOLA responsabilità** chiara
- **Nessuna decisione ambigua** da prendere
- **Input e output ben definiti** con esempi concreti

```
❌ NON ATOMICO: "Implementa validazione form"
✅ ATOMICO: "Aggiungi validazione email in LoginForm.tsx linee 23-45
            usando regex ^[a-z]+@[a-z]+\.[a-z]+$ già in utils/regex.ts"

❌ NON ATOMICO: "Refactoring modulo auth"
✅ ATOMICO: "Rinomina checkAuth() in validateSession() in auth.py:67"
```

**Decomposizione:**
```
Task complesso → Decomponi in N task atomici → N agenti paralleli

"Aggiungi endpoint users" diventa:
├── Task 1: Schema Pydantic (1 agente)
├── Task 2: Service function (1 agente)
├── Task 3: Route endpoint (1 agente)
└── Task 4: Test (1 agente)
```

**Test atomicità:** Un junior developer potrebbe completarlo senza chiedere?
- Sì → Task atomico, procedi
- No → Decomponi ulteriormente

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

```
╔═══════════════════════════════════════════════════════════════╗
║  ⚠️  STOP OBBLIGATORIO - NON PROCEDERE SENZA APPROVAZIONE   ⚠️ ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  1. Mostra il piano completo all'utente                       ║
║  2. USA AskUserQuestion per chiedere conferma                 ║
║  3. ATTENDI risposta PRIMA di passare a FASE 4                ║
║                                                               ║
║  Se l'utente NON approva esplicitamente → NON procedere       ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
```

Chiedi usando **AskUserQuestion**:
> "Piano pronto con **X agenti**. Vuoi che proceda con l'implementazione?"

Opzioni:
- "Sì, procedi con l'implementazione"
- "No, modifica il piano"
- "Annulla"

---

## FASE 4: Esecuzione Multi-Agente

```
╔═══════════════════════════════════════════════════════════════════════╗
║  🚨 REGOLA INVIOLABILE: USA SEMPRE IL TASK TOOL CON SUBAGENT 🚨       ║
╠═══════════════════════════════════════════════════════════════════════╣
║                                                                       ║
║  ❌ VIETATO: Edit, Write, Update diretto sui file                     ║
║  ❌ VIETATO: Modificare codice senza Task tool                        ║
║                                                                       ║
║  ✅ OBBLIGATORIO: Task tool + subagent_type per OGNI modifica         ║
║                                                                       ║
║  Se NON usi Task tool → stai violando le regole del comando           ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
```

**Per OGNI modifica devi:**
1. Usare il **Task tool**
2. Con `subagent_type` appropriato (vedi lista agenti sotto)
3. Il subagent eseguirà la modifica (NON tu direttamente)

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
- model: MODELLO_AGENTI  ← USA IL MODELLO ESTRATTO IN FASE 0
- prompt: "Task: [descrizione]\nFile: [path]\nIstruzioni: [dettagli]\nContesto: [codice]"
```

**IMPORTANTE:** Passa SEMPRE il parametro `model` con il valore estratto dalla FASE 0:
- Se utente ha specificato `--model=opus` → `model: "opus"`
- Se utente ha specificato `--model=haiku` → `model: "haiku"`
- Se nessun parametro (default) → `model: "sonnet"`

### 4.3 Task Paralleli (IMPORTANTE)

Per task INDIPENDENTI, lancia TUTTI gli agenti in UN SINGOLO messaggio:

```
Messaggio con 3 Task tool simultanei (MODELLO = valore estratto in FASE 0):

Task 1: subagent_type="multi-agent-orchestrator:backend-developer-1", model=MODELLO, prompt="..."
Task 2: subagent_type="multi-agent-orchestrator:backend-developer-2", model=MODELLO, prompt="..."
Task 3: subagent_type="multi-agent-orchestrator:frontend-developer-1", model=MODELLO, prompt="..."
```

**USA agenti numerati diversi** per task paralleli (backend-developer-1, backend-developer-2, ecc.)

⚠️ **NON DIMENTICARE `model=MODELLO`** in ogni Task tool!

### 4.4 Task Sequenziali

Per task con DIPENDENZE:
1. Lancia il primo agente
2. Attendi completamento con TaskOutput
3. Verifica risultato
4. **Estrai contesto condiviso** (vedi 4.4.1)
5. Poi lancia il successivo con contesto

### 4.4.1 Shared Context Buffer (IMPORTANTE)

Quando esegui task SEQUENZIALI (con dipendenze), passa il contesto tra agenti:

**Dopo che Agente N completa, estrai:**
- Naming usati (es. `user_id` non `userId`)
- Pattern implementati (es. come gestisce errori)
- Strutture dati create (es. nuovi campi, tipi)
- Costanti/configurazioni aggiunte

**Aggiungi al prompt di Agente N+1:**

```markdown
**Contesto da task precedenti:**
- Task #1 ha creato: `class UserSchema` con campo `email_verified: bool`
- Naming convention usata: snake_case
- Pattern errori: `raise HTTPException(status_code=X, detail=Y)`
- Import aggiunti: `from pydantic import BaseModel`
```

**Per task PARALLELI:**
- NON puoi passare contesto (eseguono insieme)
- Quindi specifica **pattern e convenzioni IDENTICI** in tutti i prompt
- Usa la sezione "Pattern e convenzioni" per garantire coerenza

**Esempio flusso con context buffer:**
```
Task #1 (models/user.py) → Completa
    ↓
Estrai: "creato campo 'status: UserStatus' enum con ACTIVE, INACTIVE, BANNED"
    ↓
Task #2 (services/user.py) → Riceve contesto: "usa UserStatus.ACTIVE etc."
    ↓
Estrai: "creato metodo 'change_status(user_id, new_status)'"
    ↓
Task #3 (routes/user.py) → Riceve contesto completo da #1 e #2
```

### 4.5 Formato Prompt per Agente

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  REGOLA CRITICA: PASSA TUTTO IL CONTESTO - IL SUBAGENT NON DEVE RILEGGERE!   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  Tu (Opus) hai GIÀ LETTO i file. Il subagent NON deve rileggerli.            ║
║  DEVI includere nel prompt:                                                   ║
║                                                                               ║
║  1. Il CODICE ATTUALE (copia-incolla dal tuo Read)                           ║
║  2. Le RIGHE ESATTE da modificare (es. linee 45-60)                          ║
║  3. La MODIFICA PRECISA (old_string → new_string)                            ║
║  4. Il RISULTATO ATTESO (come deve apparire DOPO)                            ║
║                                                                               ║
║  Se il prompt è completo, il subagent può usare Edit DIRETTAMENTE            ║
║  senza dover prima fare Read.                                                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Campi OBBLIGATORI per ogni task:**

```markdown
## Task per [nome-agente]

**⚠️ ISTRUZIONE: NON leggere i file - tutto il contesto è già fornito sotto.**

**Obiettivo:** [descrizione COMPLETA di cosa deve fare]

**Razionale:** [PERCHÉ questa modifica]

**File e posizione ESATTA:**
- File: `path/file.py`
- Linee da modificare: 45-60
- Funzione/classe: `login_view()` dentro classe `AuthController`

**CODICE ATTUALE (già letto, NON rileggere):**
```[linguaggio]
# path/file.py linee 45-60
[COPIA-INCOLLA ESATTO del codice che hai letto con Read]
[Includi numeri di riga se utile]
```

**MODIFICA DA APPLICARE:**
```
OLD (da sostituire):
[codice esatto da cercare]

NEW (nuovo codice):
[codice esatto da inserire]
```

**RISULTATO FINALE ATTESO:**
```[linguaggio]
[come deve apparire il codice DOPO la modifica]
```

**Pattern del progetto:**
- Naming: [snake_case/camelCase]
- Import: [stile usato nel file]
- Error handling: [pattern usato]

**NON toccare:**
- [altre funzioni/sezioni]

**Verifica finale:**
- [ ] La modifica è sintatticamente corretta
- [ ] Segue i pattern del progetto
```

**ESEMPIO COMPLETO:**

```markdown
## Task per backend-developer-1

**⚠️ ISTRUZIONE: NON leggere i file - tutto il contesto è già fornito sotto.**

**Obiettivo:** Aggiungere rate limiting all'endpoint /api/users/login

**Razionale:** Prevenire attacchi brute-force. Attualmente non c'è limite ai tentativi
di login, permettendo attacchi automatizzati.

**File e posizione ESATTA:**
- File: `src/api/auth.py`
- Linee da modificare: 1-15 (import e inizio file) + 17-28 (funzione login_view)
- Funzione: `login_view(request)`

**CODICE ATTUALE (già letto, NON rileggere):**
```python
# src/api/auth.py linee 1-28
1  from rest_framework.decorators import api_view
2  from rest_framework.response import Response
3  from django.contrib.auth import authenticate
4
5  @api_view(['POST'])
6  def login_view(request):
7      """Endpoint di login."""
8      email = request.data.get('email')
9      password = request.data.get('password')
10
11     user = authenticate(email=email, password=password)
12     if user is None:
13         return Response({'error': 'Invalid credentials'}, status=401)
14
15     token = generate_token(user)
16     return Response({'token': token})
```

**MODIFICA DA APPLICARE:**

Modifica 1 - Aggiungere import:
```
OLD:
from django.contrib.auth import authenticate

NEW:
from django.contrib.auth import authenticate
from django.core.cache import cache

RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 300

def check_rate_limit(ip: str) -> bool:
    key = f'auth:rate_limit:{ip}'
    attempts = cache.get(key, 0)
    return attempts < RATE_LIMIT_ATTEMPTS
```

Modifica 2 - Aggiornare login_view:
```
OLD:
def login_view(request):
    """Endpoint di login."""
    email = request.data.get('email')

NEW:
def login_view(request):
    """Endpoint di login con rate limiting."""
    ip = request.META.get('REMOTE_ADDR')
    if not check_rate_limit(ip):
        return Response({'error': 'Too many attempts'}, status=429)
    email = request.data.get('email')
```

**Pattern del progetto:**
- Naming: snake_case per funzioni, UPPER_CASE per costanti
- Import: Django first, then rest_framework
- Error responses: dict con key 'error'

**NON toccare:**
- La logica di authenticate()
- Altri endpoint nel file

**Verifica finale:**
- [ ] Sintassi corretta
- [ ] Import in ordine corretto
- [ ] Rate limit applicato PRIMA di authenticate
```

### 4.6 CHECKLIST VALIDAZIONE PRE-LANCIO (OBBLIGATORIA)

**PRIMA di lanciare OGNI agente**, verifica che il tuo prompt contenga TUTTI questi elementi:

```
┌──────────────────────────────────────────────────────────────────────┐
│  CHECKLIST VALIDAZIONE PROMPT - NON LANCIARE SE INCOMPLETO           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [ ] ISTRUZIONE "NON LEGGERE": Presente all'inizio?                  │
│      ❌ mancante                                                     │
│      ✅ "⚠️ NON leggere i file - contesto già fornito"              │
│                                                                      │
│  [ ] OBIETTIVO: Descrizione chiara e completa?                       │
│      ❌ "Modifica il file" → troppo vago                             │
│      ✅ "Aggiungi validazione email nella funzione X"                │
│                                                                      │
│  [ ] FILE + LINEE + FUNZIONE: Posizione esatta?                      │
│      ❌ "modifica services.py"                                       │
│      ✅ "src/services.py linee 45-60, funzione validate_user()"     │
│                                                                      │
│  [ ] CODICE ATTUALE: Hai COPIATO il codice dal tuo Read?             │
│      ❌ mancante o "leggi il file"                                   │
│      ✅ Codice con numeri di riga copiato nel prompt                 │
│                                                                      │
│  [ ] MODIFICA ESATTA: Hai specificato OLD → NEW?                     │
│      ❌ "aggiungi validazione"                                       │
│      ✅ "OLD: [codice da sostituire]  NEW: [nuovo codice]"          │
│                                                                      │
│  [ ] PATTERN PROGETTO: Naming, import, error handling?               │
│      ❌ mancante                                                     │
│      ✅ "snake_case, Django imports first"                          │
│                                                                      │
│  [ ] VINCOLI: Specificato cosa NON modificare?                       │
│      ❌ mancante                                                     │
│      ✅ "NON toccare altre funzioni nel file"                       │
│                                                                      │
└──────────────────────────────────────────────────────────────────────┘
```

**SE MANCA ANCHE UN SOLO ELEMENTO:**
1. **NON lanciare l'agente**
2. TU completa le informazioni mancanti
3. Poi lancia

**OBIETTIVO:** Il subagent deve poter usare Edit DIRETTAMENTE senza fare Read.

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

### 5.4 Verifica con Playwright (SE DISPONIBILE)

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  VERIFICA AUTOMATICA - NON RILEGGERE I FILE, USA PLAYWRIGHT!              ║
╠═══════════════════════════════════════════════════════════════════════════╣
║                                                                           ║
║  Invece di rileggere il codice per verificare le modifiche:               ║
║  → Esegui test Playwright per confermare che FUNZIONA                     ║
║                                                                           ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

**Prima verifica se Playwright è disponibile:**
```bash
npx playwright --version 2>/dev/null || echo "NOT_INSTALLED"
```

**Se disponibile, esegui verifiche appropriate:**

#### 5.4.1 Verifiche Frontend (UI)

Per modifiche a template, CSS, JavaScript:

```bash
# Test esistenti
npx playwright test --grep "nome-feature"

# Oppure smoke test rapido
npx playwright test --project=chromium --timeout=10000
```

**Se non ci sono test specifici**, crea un test temporaneo:

```javascript
// test-temp.spec.js
import { test, expect } from '@playwright/test';

test('verifica modifica [NOME]', async ({ page }) => {
  await page.goto('http://localhost:8000/[URL_PAGINA]');

  // Verifica elemento esiste
  await expect(page.locator('[SELETTORE]')).toBeVisible();

  // Verifica testo
  await expect(page.locator('[SELETTORE]')).toContainText('[TESTO_ATTESO]');

  // Verifica colore (per CTA verdi etc.)
  const button = page.locator('[SELETTORE_BOTTONE]');
  await expect(button).toHaveCSS('background-color', 'rgb(16, 185, 129)'); // emerald-500

  // Screenshot per confronto visivo
  await page.screenshot({ path: 'test-results/verifica-[NOME].png' });
});
```

```bash
npx playwright test test-temp.spec.js
```

#### 5.4.2 Verifiche API (Backend)

Per modifiche a endpoint, view, serializer:

```javascript
// test-api-temp.spec.js
import { test, expect } from '@playwright/test';

test('verifica API [ENDPOINT]', async ({ request }) => {
  // GET
  const response = await request.get('http://localhost:8000/api/[ENDPOINT]');
  expect(response.ok()).toBeTruthy();

  // POST con dati
  const postResponse = await request.post('http://localhost:8000/api/[ENDPOINT]', {
    data: { /* payload */ }
  });
  expect(postResponse.status()).toBe(201);

  // Verifica struttura risposta
  const json = await response.json();
  expect(json).toHaveProperty('[CAMPO_ATTESO]');
});
```

#### 5.4.3 Verifica Visiva (Screenshot Diff)

```bash
# Cattura screenshot prima (se possibile)
# Dopo modifica, confronta

npx playwright test --update-snapshots  # Prima volta
npx playwright test                      # Confronto
```

#### 5.4.4 Cosa fare con i risultati

| Risultato | Azione |
|-----------|--------|
| ✅ Test passano | Procedi a FASE 6 |
| ❌ Test falliscono | Analizza errore, rilancia agente con fix |
| ⚠️ Playwright non disponibile | Chiedi all'utente se vuole test manuale |

**Report verifica:**
```markdown
### Verifica Playwright
- **Test eseguiti:** X
- **Passati:** Y
- **Falliti:** Z
- **Screenshot:** [path se generati]
```

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

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🚨 REGOLE INVIOLABILI - LEGGI PRIMA DI OGNI AZIONE 🚨                    ┃
┣━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┫
┃                                                                          ┃
┃  1. ❌ MAI usare Edit/Write/Update direttamente                          ┃
┃     ✅ USA SEMPRE Task tool con subagent_type                            ┃
┃                                                                          ┃
┃  2. ❌ MAI procedere senza approvazione del piano                        ┃
┃     ✅ FERMATI alla FASE 3.2 e usa AskUserQuestion                       ┃
┃                                                                          ┃
┃  3. ❌ MAI saltare discovery MCP e analisi dipendenze                    ┃
┃     ✅ ESEGUI SEMPRE FASE 1 e FASE 1.5                                   ┃
┃                                                                          ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Checklist comportamento corretto:**
1. **MAI** modificare codice direttamente - USA SEMPRE Task tool con subagent_type
2. **MAI** saltare la fase di discovery MCP
3. **SEMPRE** verificare con grep anche dopo ricerca semantica
4. **MAI** procedere senza piano approvato dall'utente
5. **SEMPRE** usare Task tool per delegare a subagenti
6. **SEMPRE** verificare i risultati di ogni subagent
7. **SEMPRE** lanciare in parallelo task indipendenti (multipli Task tool in un messaggio)
