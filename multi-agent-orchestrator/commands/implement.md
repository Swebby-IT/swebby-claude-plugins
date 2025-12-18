---
description: Implementa una feature con workflow Architect → Orchestrator → Debug (contesto ottimizzato)
argument-hint: "<descrizione della modifica da implementare> [--model=sonnet|opus|haiku]"
---

# Comando: Implementa con Workflow Architect-Orchestrator-Debug

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   WORKFLOW A TRE RUOLI (contesto ottimizzato)                                ║
║                                                                              ║
║   ┌─────────────┐     ┌──────────────┐     ┌─────────────┐                   ║
║   │  ARCHITECT  │ ──▶ │ ORCHESTRATOR │ ──▶ │    DEBUG    │                   ║
║   │ (subagent)  │     │    (tu)      │     │ (Playwright)│                   ║
║   └─────────────┘     └──────────────┘     └─────────────┘                   ║
║         │                    │                    │                          ║
║   Legge file,          Riceve SOLO           Verifica con                    ║
║   crea piano           piano compatto        test automatici                 ║
║   COMPATTO             (contesto pulito!)                                    ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Task da implementare:** $ARGUMENTS

---

## STEP 0: Parsing Parametri

```
Se "--model=opus" trovato   → MODELLO_AGENT = "opus"
Se "--model=haiku" trovato  → MODELLO_AGENT = "haiku"
Se "--model=sonnet" trovato → MODELLO_AGENT = "sonnet"
Se NON trovato              → MODELLO_AGENT = "sonnet" (default)
```

**Stampa:**
```markdown
## Configurazione
- **MODELLO AGENT:** [valore]
- **Task:** [descrizione senza --model]
```

---

## STEP 1: Lancia ARCHITECT (subagent Opus)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🏗️  ARCHITECT come SUBAGENT - Il suo contesto verrà SCARTATO                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  L'Architect legge i file, analizza, e ritorna SOLO il piano compatto.       ║
║  Tu (Orchestrator) ricevi solo il piano, non tutto il codice letto.          ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Lancia Task tool:**

```
Task tool:
  subagent_type: "multi-agent-orchestrator:architect"
  model: "opus"
  prompt: |
    ## Richiesta Analisi e Piano

    **Task da implementare:** [DESCRIZIONE_TASK]

    **Istruzioni:**
    1. Cerca i file rilevanti con Grep
    2. Leggi SOLO le sezioni necessarie (usa offset/limit per file grandi)
    3. Analizza le modifiche necessarie
    4. Crea piano COMPATTO con:
       - File e linee esatte
       - Snippet OLD/NEW minimi (max 20 righe ciascuno)
       - Dipendenze tra task
       - Pattern del progetto

    **IMPORTANTE:**
    - NON includere file interi
    - SOLO le righe da modificare
    - Il tuo output deve essere passabile ai subagent
```

**Attendi completamento e ricevi il piano.**

---

## STEP 2: Mostra Piano e Chiedi Approvazione

```
╔═══════════════════════════════════════════════════════════════════════════╗
║  ⚠️  STOP OBBLIGATORIO - MOSTRA PIANO E ATTENDI APPROVAZIONE  ⚠️          ║
╚═══════════════════════════════════════════════════════════════════════════╝
```

Mostra all'utente il piano ricevuto dall'Architect.

Usa **AskUserQuestion**:
```
Piano ricevuto dall'Architect con N task. Procedo?
- Sì, procedi
- No, modifica
- Annulla
```

**NON procedere senza approvazione.**

---

## STEP 3: ORCHESTRATOR - Lancia Subagent

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🎯  ORCHESTRATOR - Lancia subagent con il piano ricevuto                     ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  NON modificare MAI codice direttamente!                                      ║
║  USA SOLO: Task tool con subagent_type                                        ║
║                                                                               ║
║  Il piano dell'Architect contiene già OLD/NEW per ogni task.                  ║
║  Passa questi direttamente ai subagent.                                       ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 3.1 Agenti Disponibili

| Tipo | subagent_type |
|------|---------------|
| Frontend | `multi-agent-orchestrator:frontend-developer-1` (fino a -20) |
| Backend | `multi-agent-orchestrator:backend-developer-1` (fino a -20) |
| Bug fix | `multi-agent-orchestrator:bug-fixer` |
| API | `multi-agent-orchestrator:api-developer` |
| Database | `multi-agent-orchestrator:database-specialist` |

### 3.2 Formato Prompt per Subagent

**Copia il task dal piano dell'Architect:**

```markdown
## Task per [nome-agente]

**⚠️ NON leggere i file - usa direttamente OLD/NEW forniti.**

**Obiettivo:** [dal piano Architect]

**File:** `[path]`
**Linee:** [range]

**OLD:**
```
[codice da piano Architect]
```

**NEW:**
```
[codice da piano Architect]
```

**Pattern:** [dal piano Architect]
```

### 3.3 Parallelismo

```
Task SENZA dipendenze → LANCIA IN PARALLELO (un messaggio, N Task tool)
Task CON dipendenze   → LANCIA IN SEQUENZA
```

**Task paralleli:**
```
Task tool 1: subagent_type="...-developer-1", model=MODELLO_AGENT, prompt="..."
Task tool 2: subagent_type="...-developer-2", model=MODELLO_AGENT, prompt="..."
```

---

## STEP 4: DEBUG - Verifica con Playwright

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🔍  DEBUG - Verifica con Playwright (NON rileggere file!)                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### 4.1 Verifica Playwright

```bash
npx playwright --version 2>/dev/null && echo "OK" || echo "NOT_INSTALLED"
```

### 4.2 Test Automatico

**Frontend:**
```bash
cat > test-verify.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';
test('verifica', async ({ page }) => {
  await page.goto('http://localhost:8000/[URL]');
  await expect(page.locator('[SELETTORE]')).toBeVisible();
});
EOF
npx playwright test test-verify.spec.ts
rm test-verify.spec.ts
```

**API:**
```bash
cat > test-api.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';
test('verifica API', async ({ request }) => {
  const r = await request.get('http://localhost:8000/api/[ENDPOINT]');
  expect(r.ok()).toBeTruthy();
});
EOF
npx playwright test test-api.spec.ts
rm test-api.spec.ts
```

### 4.3 Risultati

| Risultato | Azione |
|-----------|--------|
| ✅ Test OK | Report finale |
| ❌ Test FAIL | Torna a STEP 3, rilancia subagent con fix |
| ⚠️ No Playwright | Chiedi verifica manuale |

---

## STEP 5: Report Finale

```markdown
## Implementazione Completata

### Workflow
| Step | Stato |
|------|-------|
| ARCHITECT (subagent) | ✅ Piano creato |
| ORCHESTRATOR | ✅ N subagent lanciati |
| DEBUG | ✅ Test passati |

### Modifiche
| File | Agente | Test |
|------|--------|------|
| path/file.py | backend-1 | ✅ |

### Verifica
- Test Playwright: ✅ Passati
```

---

## RIEPILOGO WORKFLOW

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                              ┃
┃  STEP 1: ARCHITECT (subagent Opus)                                           ┃
┃  ├── Legge file con Grep + Read(offset/limit)                                ┃
┃  ├── Crea piano COMPATTO (max 20 righe per snippet)                          ┃
┃  └── RITORNA piano → suo contesto viene SCARTATO                             ┃
┃                                                                              ┃
┃  STEP 2: APPROVAZIONE                                                        ┃
┃  └── Mostra piano, chiedi conferma utente                                    ┃
┃                                                                              ┃
┃  STEP 3: ORCHESTRATOR (tu - contesto pulito!)                                ┃
┃  ├── Ricevi SOLO il piano compatto                                           ┃
┃  ├── Lancia subagent con Task tool                                           ┃
┃  └── Passa OLD/NEW dal piano ai subagent                                     ┃
┃                                                                              ┃
┃  STEP 4: DEBUG                                                               ┃
┃  ├── Verifica con Playwright                                                 ┃
┃  └── Se fallisce → torna a STEP 3                                            ┃
┃                                                                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## REGOLE INVIOLABILI

1. **ARCHITECT** è un subagent - il suo contesto viene scartato
2. **ORCHESTRATOR** riceve SOLO il piano compatto
3. **MAI** Edit/Write diretto - solo Task tool
4. **SEMPRE** approvazione prima di STEP 3
5. **DEBUG** usa Playwright, non Read
