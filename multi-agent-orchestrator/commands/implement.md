---
description: Implementa una feature con orchestrazione intelligente multi-agente (analisi MCP → piano → auto-scaling → esecuzione parallela)
argument-hint: "<descrizione della modifica da implementare> [--model=sonnet|opus|haiku]"
---

# Comando: Implementa con Multi-Agent Orchestration

Stai per implementare: **$ARGUMENTS**

## FASE 0: Parsing Parametri

### 0.1 Estrai il Modello

Analizza `$ARGUMENTS` per estrarre il parametro `--model`:

```
Cerca pattern: --model=sonnet | --model=opus | --model=haiku

Se trovato:
  MODELLO_AGENTI = [valore estratto]
  DESCRIZIONE_TASK = $ARGUMENTS senza --model=...

Se NON trovato:
  MODELLO_AGENTI = sonnet (default)
  DESCRIZIONE_TASK = $ARGUMENTS
```

**Modelli disponibili:**
| Modello | Uso Consigliato | Costo Relativo |
|---------|-----------------|----------------|
| `haiku` | Task semplici, economico | $ |
| `sonnet` | Task standard, bilanciato (DEFAULT) | $$ |
| `opus` | Task complessi, massima qualità | $$$ |

Registra:
```markdown
**Modello selezionato:** [sonnet/opus/haiku]
**Task da implementare:** [descrizione senza parametro]
```

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

**REGOLA CRITICA:** I subagenti Sonnet NON hanno il contesto della conversazione.
Devi fornire TUTTE le informazioni nel prompt. Se ometti dettagli, l'agente farà scelte arbitrarie.

**Campi OBBLIGATORI per ogni task:**

```markdown
## Task per [nome-agente]

**Obiettivo:** [descrizione COMPLETA di cosa deve fare]

**Razionale:** [PERCHÉ questa modifica - aiuta l'agente a fare scelte informate]

**File da modificare:**
- `path/file.py` linee X-Y

**Istruzioni PASSO-PASSO:**
1. [azione SPECIFICA con dettagli implementativi]
2. [azione SPECIFICA con dettagli implementativi]
3. [azione SPECIFICA con dettagli implementativi]

**Contesto codice ATTUALE (SEMPRE INCLUDERE):**
```[linguaggio]
[snippet del codice ESISTENTE che verrà modificato]
[includere anche contesto circostante se rilevante]
```

**Pattern e convenzioni del progetto:**
- Naming: [camelCase/snake_case/etc.]
- Import style: [pattern usato]
- Error handling: [come gestire errori]

**Output atteso:**
```[linguaggio]
[come dovrebbe apparire il codice DOPO la modifica]
```

**NON modificare:**
- [file/sezioni da non toccare]
- [comportamenti da preservare]

**Dipendenze:**
- Dipende da: [Task #X / nessuno]
- Bloccante per: [Task #Y / nessuno]
```

**ESEMPIO COMPLETO:**

```markdown
## Task per backend-developer-1

**Obiettivo:** Aggiungere rate limiting all'endpoint /api/users/login

**Razionale:** Prevenire attacchi brute-force. Attualmente non c'è limite ai tentativi
di login, permettendo attacchi automatizzati.

**File da modificare:**
- `src/api/auth.py` linee 45-70

**Istruzioni PASSO-PASSO:**
1. Importare `from django.core.cache import cache` dopo gli altri import Django
2. Creare costanti RATE_LIMIT_ATTEMPTS=5 e RATE_LIMIT_WINDOW=300 (5 min)
3. Creare funzione `check_rate_limit(ip: str) -> bool` che usa cache
4. In `login_view`, chiamare check_rate_limit PRIMA della validazione credenziali
5. Se rate limit superato, restituire Response 429 con header Retry-After

**Contesto codice ATTUALE (SEMPRE INCLUDERE):**
```python
# src/api/auth.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import authenticate

@api_view(['POST'])
def login_view(request):
    """Endpoint di login."""
    email = request.data.get('email')
    password = request.data.get('password')

    user = authenticate(email=email, password=password)
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=401)

    token = generate_token(user)
    return Response({'token': token})
```

**Pattern e convenzioni del progetto:**
- Naming: snake_case per funzioni, UPPER_CASE per costanti
- Import: Django imports first, then rest_framework, then local
- Error responses: sempre dict con key 'error'
- Cache keys: prefix con nome modulo, es. 'auth:rate_limit:{ip}'

**Output atteso:**
```python
from django.core.cache import cache  # aggiunto

RATE_LIMIT_ATTEMPTS = 5
RATE_LIMIT_WINDOW = 300  # 5 minuti

def check_rate_limit(ip: str) -> bool:
    """Verifica se IP ha superato rate limit."""
    key = f'auth:rate_limit:{ip}'
    attempts = cache.get(key, 0)
    return attempts < RATE_LIMIT_ATTEMPTS

@api_view(['POST'])
def login_view(request):
    """Endpoint di login con rate limiting."""
    ip = request.META.get('REMOTE_ADDR')

    if not check_rate_limit(ip):
        return Response(
            {'error': 'Too many attempts'},
            status=429,
            headers={'Retry-After': str(RATE_LIMIT_WINDOW)}
        )
    # ... resto della logica
```

**NON modificare:**
- La logica di authenticate()
- Il formato della response di successo
- Altri endpoint nel file

**Dipendenze:**
- Dipende da: nessuno
- Bloccante per: Task #4 (test rate limiting)
```

### 4.6 CHECKLIST VALIDAZIONE PRE-LANCIO (OBBLIGATORIA)

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

**RICORDA:** L'agente Sonnet NON ha il tuo contesto. Se il prompt è incompleto, farà scelte arbitrarie o fallirà.

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
