---
description: Implementa una feature con workflow Architect → Orchestrator → Debug (stile Kilo Code)
argument-hint: "<descrizione della modifica da implementare> [--model=sonnet|opus|haiku]"
---

# Comando: Implementa con Workflow Architect-Orchestrator-Debug

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   WORKFLOW A TRE RUOLI (stile Kilo Code)                                     ║
║                                                                              ║
║   ┌─────────────┐     ┌──────────────┐     ┌─────────────┐                   ║
║   │  ARCHITECT  │ ──▶ │ ORCHESTRATOR │ ──▶ │    DEBUG    │                   ║
║   │   (Opus)    │     │   (Coord.)   │     │   (Opus)    │                   ║
║   └─────────────┘     └──────────────┘     └─────────────┘                   ║
║         │                    │                    │                          ║
║    Analizza +           Lancia N            Verifica con                     ║
║    Pianifica            subagent            Playwright                       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
```

**Task da implementare:** $ARGUMENTS

---

## RUOLO 1: ARCHITECT (Tu - Opus)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🏗️  ARCHITECT - Analizza il codebase e crea il piano di implementazione     ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  PUOI USARE: Read, Grep, Glob, MCP semantici                                  ║
║  NON PUOI USARE: Edit, Write, Update (mai modificare direttamente!)           ║
║                                                                               ║
║  OUTPUT: Piano dettagliato con task atomici per ogni subagent                 ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### A.1 Parsing Parametri

Analizza `$ARGUMENTS` per estrarre `--model`:

```
Se "--model=opus" trovato   → MODELLO_AGENT = "opus"
Se "--model=haiku" trovato  → MODELLO_AGENT = "haiku"
Se "--model=sonnet" trovato → MODELLO_AGENT = "sonnet"
Se NON trovato              → MODELLO_AGENT = "sonnet" (default)
```

**Stampa subito:**
```markdown
## Configurazione
- **MODELLO AGENT:** [valore] ← per i subagent di modifica
- **Task:** [descrizione senza --model]
```

### A.2 Discovery MCP

Verifica quali MCP sono disponibili:
- `mcp__code-search__*` → Ricerca semantica
- `mcp__*__search*` → Altri tool di ricerca

### A.3 Ricerca e Analisi Codebase

**LEGGI i file rilevanti** usando Read, Grep, Glob:

1. Cerca file correlati al task
2. Analizza struttura e pattern esistenti
3. Identifica dipendenze tra file
4. **SALVA il contesto letto** (servirà per i subagent)

### A.4 Costruisci Grafo Dipendenze

```markdown
## Grafo Dipendenze

File A (foglia) → File B → File C
                         ↘ File D

Ordine esecuzione:
1. File A (nessuna dipendenza)
2. File B (dipende da A)
3. File C, D (dipendono da B) ← parallelizzabili
```

### A.5 Crea Piano Dettagliato

Per OGNI modifica necessaria, crea un **task atomico**:

```markdown
## Piano di Implementazione

### Task 1: [Nome descrittivo]
- **File:** path/to/file.py
- **Linee:** 45-60
- **Funzione:** nome_funzione()
- **Tipo:** Modifica/Nuovo/Elimina
- **Dipende da:** Task N / nessuno
- **Descrizione:** [cosa fare esattamente]
- **CODICE ATTUALE:**
  ```python
  [codice che hai letto con Read - COPIA QUI]
  ```
- **MODIFICA:**
  ```
  OLD: [codice da sostituire]
  NEW: [nuovo codice]
  ```

### Task 2: [Nome descrittivo]
...
```

### A.6 STOP - Chiedi Approvazione

```
╔═══════════════════════════════════════════════════════════════╗
║  ⚠️  STOP OBBLIGATORIO - ATTENDI APPROVAZIONE UTENTE  ⚠️      ║
╚═══════════════════════════════════════════════════════════════╝
```

Usa **AskUserQuestion**:

```
Piano pronto con N task. Procedo con l'implementazione?

- Sì, procedi
- No, modifica il piano
- Annulla
```

**NON procedere a RUOLO 2 senza approvazione esplicita.**

---

## RUOLO 2: ORCHESTRATOR (Tu - Coordinatore)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🎯  ORCHESTRATOR - Scompone e coordina i subagent                            ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  NON modificare MAI codice direttamente!                                      ║
║  USA SOLO: Task tool con subagent_type                                        ║
║                                                                               ║
║  Per OGNI task del piano → lancia un subagent specializzato                   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### O.1 Regole di Parallelismo

```
Task SENZA dipendenze reciproche → LANCIA IN PARALLELO (un messaggio, N Task tool)
Task CON dipendenze             → LANCIA IN SEQUENZA (attendi completamento)
```

### O.2 Agenti Disponibili

| Tipo Task | subagent_type |
|-----------|---------------|
| Frontend/UI | `multi-agent-orchestrator:frontend-developer-1` (fino a -20) |
| Backend/Logic | `multi-agent-orchestrator:backend-developer-1` (fino a -20) |
| Bug fix | `multi-agent-orchestrator:bug-fixer` |
| API | `multi-agent-orchestrator:api-developer` |
| Database | `multi-agent-orchestrator:database-specialist` |
| Test | `multi-agent-orchestrator:test-writer` |

### O.3 Formato Prompt per Subagent

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  REGOLA CRITICA: IL SUBAGENT NON DEVE RILEGGERE I FILE!                       ║
║  Passa TUTTO il contesto che hai già letto come Architect.                    ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

**Template OBBLIGATORIO:**

```markdown
## Task per [nome-agente]

**⚠️ NON leggere i file - tutto il contesto è già fornito sotto.**

**Obiettivo:** [descrizione completa]

**Razionale:** [PERCHÉ questa modifica]

**File e posizione ESATTA:**
- File: `path/file.py`
- Linee: 45-60
- Funzione: `nome_funzione()`

**CODICE ATTUALE (NON rileggere):**
```python
# path/file.py linee 45-60
45  def nome_funzione():
46      # codice esistente
47      ...
```

**MODIFICA DA APPLICARE:**
```
OLD:
[codice esatto da cercare]

NEW:
[codice esatto da inserire]
```

**Pattern del progetto:**
- Naming: snake_case
- Import: Django first

**NON toccare:**
- Altre funzioni nel file

**Verifica:**
- [ ] Sintassi corretta
- [ ] Pattern rispettati
```

### O.4 Lancia Subagent

**Task paralleli** (un messaggio con N Task tool):
```
Task tool 1: subagent_type="...-developer-1", model=MODELLO_AGENT, prompt="..."
Task tool 2: subagent_type="...-developer-2", model=MODELLO_AGENT, prompt="..."
Task tool 3: subagent_type="...-developer-3", model=MODELLO_AGENT, prompt="..."
```

**Task sequenziali** (con dipendenze):
1. Lancia Task 1
2. Attendi completamento
3. Estrai contesto condiviso (naming usati, strutture create)
4. Passa contesto a Task 2
5. Ripeti

### O.5 Gestione Errori Subagent

Se un subagent fallisce:
1. Analizza errore
2. Rilancia con istruzioni più chiare
3. Se persiste, segnala all'utente

### O.6 Passa a Debug

Dopo che TUTTI i subagent hanno completato → passa a RUOLO 3.

---

## RUOLO 3: DEBUG (Tu - Opus)

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║  🔍  DEBUG - Verifica le modifiche con Playwright (NON rileggere file!)       ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  NON usare Read per verificare le modifiche!                                  ║
║  USA: Playwright per testare che FUNZIONA                                     ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### D.1 Verifica Playwright Disponibile

```bash
npx playwright --version 2>/dev/null && echo "OK" || echo "NOT_INSTALLED"
```

### D.2 Test Frontend (se modifiche UI)

```bash
# Crea test temporaneo
cat > test-verify.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';

test('verifica modifica', async ({ page }) => {
  await page.goto('http://localhost:8000/[URL]');

  // Verifica elemento visibile
  await expect(page.locator('[SELETTORE]')).toBeVisible();

  // Verifica testo
  await expect(page.locator('[SELETTORE]')).toContainText('[TESTO]');

  // Verifica colore (es. bottone verde)
  await expect(page.locator('[SELETTORE]')).toHaveCSS('background-color', 'rgb(16, 185, 129)');

  // Screenshot
  await page.screenshot({ path: 'test-results/verifica.png' });
});
EOF

npx playwright test test-verify.spec.ts
```

### D.3 Test API (se modifiche backend)

```bash
cat > test-api.spec.ts << 'EOF'
import { test, expect } from '@playwright/test';

test('verifica API', async ({ request }) => {
  const response = await request.get('http://localhost:8000/api/[ENDPOINT]');
  expect(response.ok()).toBeTruthy();

  const json = await response.json();
  expect(json).toHaveProperty('[CAMPO]');
});
EOF

npx playwright test test-api.spec.ts
```

### D.4 Analisi Risultati

| Risultato | Azione |
|-----------|--------|
| ✅ Test passano | Procedi a Report Finale |
| ❌ Test falliscono | Torna a ORCHESTRATOR, rilancia subagent con fix |
| ⚠️ Playwright non disponibile | Chiedi all'utente se vuole verifica manuale |

### D.5 Cleanup Test Temporanei

```bash
rm -f test-verify.spec.ts test-api.spec.ts
```

---

## REPORT FINALE

```markdown
## Implementazione Completata

### Workflow Eseguito
| Ruolo | Stato | Note |
|-------|-------|------|
| ARCHITECT | ✅ | Piano approvato |
| ORCHESTRATOR | ✅ | N subagent lanciati |
| DEBUG | ✅ | Test Playwright passati |

### Modifiche Apportate
| File | Modifica | Agente | Test |
|------|----------|--------|------|
| path/file1.py | +20/-5 linee | backend-developer-1 | ✅ |
| path/file2.html | +15 linee | frontend-developer-1 | ✅ |

### Verifica Playwright
- **Test eseguiti:** X
- **Passati:** Y
- **Screenshot:** test-results/verifica.png

### Prossimi Passi
1. [Se necessario] Eseguire test completi: `npx playwright test`
2. [Se necessario] Review manuale dei file modificati
```

---

## RIEPILOGO RUOLI

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                                                                              ┃
┃  ARCHITECT (Tu - Opus)                                                       ┃
┃  ├── Legge file con Read, Grep, Glob                                         ┃
┃  ├── Analizza dipendenze                                                     ┃
┃  ├── Crea piano dettagliato con task atomici                                 ┃
┃  └── STOP: Chiede approvazione utente                                        ┃
┃                                                                              ┃
┃  ORCHESTRATOR (Tu - Coordinatore)                                            ┃
┃  ├── NON modifica mai direttamente (vietato Edit/Write)                      ┃
┃  ├── Lancia subagent con Task tool                                           ┃
┃  ├── Passa TUTTO il contesto (subagent non rilegge)                          ┃
┃  └── Coordina parallelo/sequenziale                                          ┃
┃                                                                              ┃
┃  DEBUG (Tu - Opus)                                                           ┃
┃  ├── NON rilegge file per verificare                                         ┃
┃  ├── Usa Playwright per testare                                              ┃
┃  ├── Se test fallisce → torna a ORCHESTRATOR                                 ┃
┃  └── Se test passa → Report finale                                           ┃
┃                                                                              ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

---

## REGOLE INVIOLABILI

1. **ARCHITECT:** Solo lettura, mai modifiche
2. **ORCHESTRATOR:** Solo Task tool, mai Edit/Write diretto
3. **DEBUG:** Solo Playwright, mai Read per verificare
4. **SEMPRE:** Approvazione utente prima di ORCHESTRATOR
5. **SEMPRE:** Passare contesto completo ai subagent
