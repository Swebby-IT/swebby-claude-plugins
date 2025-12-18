---
description: Esegue un piano di implementazione delegando ai subagenti specializzati (backend, frontend, styling)
argument-hint: "<descrizione> oppure 'recent' per ultimo piano approvato"
---

# Comando: /architect:implement

Stai per implementare: **$ARGUMENTS**

---

## REGOLA FONDAMENTALE - DELEGA OBBLIGATORIA

**NON MODIFICARE MAI CODICE DIRETTAMENTE.**

Questo comando e' un ORCHESTRATORE. Il tuo ruolo e':
1. Analizzare e pianificare
2. Delegare OGNI modifica ai subagenti specializzati
3. Coordinare e verificare

**Per OGNI modifica di codice, DEVI usare il Task tool:**

| Tipo Modifica | Subagent |
|---------------|----------|
| Backend (models, views, API, services, database) | `architect:backend-developer` |
| Frontend (components, stores, routing, UI logic) | `architect:frontend-developer` |
| Styling (CSS, Tailwind, SCSS, UI appearance) | `architect:styling-developer` |
| Test (unit, integration, e2e) | `architect:test-writer` |
| Review finale | `architect:code-reviewer` |

**Esempio CORRETTO:**
```
Task tool con subagent_type: architect:styling-developer
prompt: "Aggiungi mb-2 ai label nel file X linee Y-Z"
```

**Esempio SBAGLIATO:**
```
Edit tool direttamente sul file  <-- MAI FARE QUESTO
```

Se fai modifiche dirette senza delegare, stai violando il principio del plugin.

---

## FASE 0: Leggi Contesto Progetto

**PRIMA DI TUTTO**, leggi il contesto:

```
1. Cerca `claude.md` o `CLAUDE.md` nella root
2. Identifica lo stack:
   - Backend: Django, FastAPI, Express, NestJS, Laravel, Rails, etc.
   - Frontend: Vue, React, Angular, Svelte, Vanilla JS, etc.
   - Styling: Tailwind, Bootstrap, SCSS, CSS Modules, etc.
   - Database: PostgreSQL, MySQL, SQLite, MongoDB, etc.
3. Passa questa info agli agenti
```

---

## FASE 1: Identificazione Piano

### 1.1 Se $ARGUMENTS = "recent" o path piano

```
1. Cerca piano in .architect/plans/
2. Verifica che sia approvato (status: approved)
3. Carica task e dipendenze
```

### 1.2 Se $ARGUMENTS = descrizione nuova

```
1. Prima esegui /architect:plan per creare piano
2. Attendi approvazione utente
3. Poi procedi con implementazione
```

**FERMATI** se il piano non e' approvato:
```
Il piano non e' stato ancora approvato.

Vuoi:
1. Approvare e procedere
2. Revisionare prima (/architect:review)
3. Annullare

[usa AskUserQuestion]
```

---

## FASE 2: Analisi Piano

### 2.1 Parsing Task

Estrai dal piano (o dalla todo list):
- Lista task con dipendenze
- File da modificare
- Tipo di modifica per ogni task

### 2.2 Classificazione per Agente

| Tipo File/Modifica | Agente |
|-------------------|--------|
| models, views, API, serializers, services, routes backend | `backend-developer` |
| components, stores, composables, hooks, pages frontend | `frontend-developer` |
| CSS, stili, classi Tailwind/Bootstrap/SCSS | `styling-developer` |
| test files (*.test.*, *.spec.*, test_*.py) | `test-writer` |
| Review finale | `code-reviewer` |

### 2.3 Calcolo Ordine Esecuzione

```
1. Analizza dipendenze tra task
2. Topological sort
3. Identifica task parallelizzabili
4. Crea batch di esecuzione
```

**Regole:**
- Task con dipendenze → sequenziali
- Task indipendenti → paralleli (max 3)
- Backend models/schema PRIMA di API/views
- Frontend components PRIMA di stores che li usano
- Styling DOPO che la struttura HTML esiste

---

## FASE 3: Esecuzione

### 3.1 Per ogni Batch di Task

```
Per ogni task nel batch:

1. Seleziona agente appropriato
2. Prepara prompt con:
   - Stack del progetto (da claude.md)
   - Obiettivo task
   - File e linee
   - Codice esistente (Read prima)
   - Pattern da seguire
   - Dipendenze da task precedenti
3. Lancia Task tool con subagent_type
4. Attendi completamento
5. Verifica output
```

### 3.2 Formato Prompt per Agente

```markdown
## Task #[N]: [Titolo]

**Stack progetto:** [da claude.md]

**Obiettivo:** [descrizione chiara]

**File:** `[path/file.ext]`
**Linee:** [XX-YY]

**Contesto codice attuale:**
```[linguaggio]
[codice esistente letto con Read]
```

**Istruzioni:**
1. [istruzione specifica 1]
2. [istruzione specifica 2]
...

**Pattern da seguire:**
- [pattern 1 dal progetto]
- [pattern 2 dal progetto]

**NON modificare:**
- [file/sezioni da non toccare]

**Dipendenze da task precedenti:**
- Task #X ha creato: [cosa]
```

### 3.3 Lancia Agenti

**Backend:**
```
Task tool con subagent_type: architect:backend-developer

[prompt task]
```

**Frontend:**
```
Task tool con subagent_type: architect:frontend-developer

[prompt task]
```

**Styling:**
```
Task tool con subagent_type: architect:styling-developer

[prompt task]
```

### 3.4 Verifica Dopo Ogni Task

```
1. Verifica che l'agente abbia completato
2. Controlla output per errori
3. Se errore:
   - Analizza causa
   - Ri-delega con istruzioni corrette
   - Max 2 retry per task
4. Se successo:
   - Passa al task successivo
   - Passa contesto rilevante
```

---

## FASE 4: Testing

### 4.1 Lancia Test Writer

Dopo tutti i task di implementazione:

```
Task tool con subagent_type: architect:test-writer

Prompt:
"Scrivi test per le modifiche implementate:

Stack: [da claude.md]

File modificati:
[lista file]

Modifiche:
[riassunto modifiche]

Crea test appropriati per lo stack:
- Backend: pytest, jest, mocha, phpunit, rspec, etc.
- Frontend: vitest, jest, testing-library, cypress, etc.

Esegui test e riporta risultati.

Output: File test + risultati esecuzione"
```

### 4.2 Verifica Test

```
1. Tutti i test devono passare
2. Se falliscono:
   - Analizza errore
   - Correggi codice o test
   - Ri-esegui
```

---

## FASE 5: Code Review

### 5.1 Lancia Code Reviewer

```
Task tool con subagent_type: architect:code-reviewer

Prompt:
"Esegui code review delle modifiche implementate:

Stack: [da claude.md]

File modificati:
[lista file con diff]

Valuta:
- Code quality
- Security
- Performance
- Best practices per lo stack usato
- Test coverage

Output: Review con score e feedback"
```

### 5.2 Gestione Feedback

```
Se score >= 7: Procedi
Se score 5-6: Mostra warning, chiedi se procedere
Se score < 5: Richiedi fix prima di completare
```

---

## FASE 6: Completamento

### 6.1 Report Finale

```markdown
## Implementazione Completata

**Piano:** [titolo piano]
**Stack:** [backend] + [frontend] + [styling]
**Data:** [YYYY-MM-DD HH:MM]

---

### Task Eseguiti

| # | Task | Agente | Status |
|---|------|--------|--------|
| 1 | [titolo] | backend-developer | ✅ |
| 2 | [titolo] | frontend-developer | ✅ |
| 3 | [titolo] | styling-developer | ✅ |

---

### File Modificati

| File | Azione | Agente |
|------|--------|--------|
| models.py | Modificato | backend-developer |
| ProductCard.vue | Creato | frontend-developer |

---

### Test

- Test scritti: X
- Test passati: X/X

---

### Code Review

**Score:** [X.X]/10
**Verdetto:** [APPROVED/...]

---

### Comandi Post-Implementazione

[comandi specifici per lo stack rilevato]

---

### Prossimi Passi

1. [suggerimento 1]
2. [suggerimento 2]
```

### 6.2 Aggiorna Piano

Se il piano era in .architect/plans/:
```
1. Aggiorna status: completed
2. Aggiungi timestamp completamento
3. Link a review
```

---

## REGOLE IMPORTANTI

1. **Leggi claude.md** - Per capire lo stack del progetto
2. **Piano approvato obbligatorio** - Non implementare senza piano
3. **Ordine corretto** - Rispetta dipendenze tra task
4. **Verifica ogni step** - Non procedere se errori
5. **Test obbligatori** - Scrivi e esegui test
6. **Review finale** - Code review prima di completare
7. **Report dettagliato** - Documenta tutto

---

## GESTIONE ERRORI

| Errore | Azione |
|--------|--------|
| Piano non trovato | Crea con /architect:plan |
| Piano non approvato | Chiedi approvazione |
| Stack non identificato | Chiedi chiarimenti |
| Task fallito | Retry max 2 volte, poi segnala |
| Test falliti | Fix e ri-esegui |
| Review negativa | Applica fix suggeriti |

---

## ESEMPIO WORKFLOW

```
1. Utente: /architect:implement Aggiungi filtro prodotti

2. Orchestrator:
   - Legge claude.md (trova: Django + Vue + Tailwind)
   - Crea piano con /architect:plan
   - Mostra piano
   - Chiede approvazione

3. Utente: "Approva"

4. Orchestrator:
   - Task 1: backend-developer → Aggiunge FilterSet (Django)
   - Task 2: backend-developer → Modifica ViewSet (Django)
   - Task 3: frontend-developer → Crea FilterComponent.vue (Vue)
   - Task 4: styling-developer → Stili filtro (Tailwind)
   - Task 5: test-writer → Test backend + frontend
   - Task 6: code-reviewer → Review finale

5. Output: Report completamento
```
