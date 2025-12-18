# Architect Plugin

Plugin per pianificazione architetturale e implementazione. Ispirato a Kilo Code Architect Mode.

**Stack-agnostic:** Legge `claude.md` per adattarsi automaticamente al progetto.

## Caratteristiche

- **Pianificazione Interattiva**: TodoWrite come output principale
- **Domande Chiarificatrici**: AskUserQuestion per disambiguare
- **Stack Agnostic**: Supporta qualsiasi linguaggio/framework
- **Memory Bank**: Directory `.architect/` per documentazione persistente
- **Diagrammi Mermaid**: Architettura, sequenze, ER
- **Multi-Agent**: Backend, frontend, styling developers generici

## Comandi

### Pianificazione (Read-only)

| Comando | Descrizione |
|---------|-------------|
| `/architect:plan <requisiti>` | Crea piano con todo list |
| `/architect:design <sistema>` | Design architetturale completo |
| `/architect:review <piano\|recent>` | Review e validazione piano |
| `/architect:diagram <componente>` | Genera diagrammi Mermaid |
| `/architect:init` | Inizializza Memory Bank |
| `/architect:export <formato>` | Esporta (markdown/mermaid/json/plantuml) |

### Esecuzione

| Comando | Descrizione |
|---------|-------------|
| `/architect:implement <piano\|descrizione>` | Esegue piano con subagenti |

## Agenti

### Pianificazione

| Agente | Modello | Ruolo |
|--------|---------|-------|
| `architect` | Opus | Pianificatore principale |
| `codebase-analyzer` | Sonnet | Analisi codebase |
| `diagram-generator` | Sonnet | Generazione diagrammi |
| `plan-reviewer` | Opus | Validazione piani |
| `documentation-writer` | Sonnet | Documentazione tecnica |

### Esecuzione (Generici)

| Agente | Modello | Ruolo |
|--------|---------|-------|
| `backend-developer` | Sonnet | Backend (Django, FastAPI, Express, etc.) |
| `frontend-developer` | Sonnet | Frontend (Vue, React, Angular, etc.) |
| `styling-developer` | Sonnet | Styling (Tailwind, Bootstrap, SCSS, etc.) |
| `test-writer` | Sonnet | Test (pytest, jest, vitest, etc.) |
| `code-reviewer` | Sonnet | Code review finale |

## Stack Supportati

### Backend
- Django, FastAPI, Flask (Python)
- Express, NestJS, Fastify (Node.js)
- Laravel (PHP)
- Rails (Ruby)
- Spring Boot (Java)
- Go (Gin, Echo)

### Frontend
- Vue 3 (Composition API, Pinia)
- React (Hooks, Redux, Zustand)
- Angular (NgRx)
- Svelte (SvelteKit)
- Vanilla JS / Web Components

### Styling
- Tailwind CSS
- Bootstrap
- Bulma
- CSS Modules
- Styled Components
- SCSS/Sass

## Come Funziona

### 1. Legge claude.md

Prima di ogni operazione, il plugin legge `claude.md` o `CLAUDE.md` nella root del progetto per identificare:
- Stack tecnologico
- Pattern architetturali
- Convenzioni del progetto

### 2. Pianificazione con TodoWrite

```
/architect:plan Aggiungi sistema di notifiche
```

Output:
- Todo list interattiva (non documenti lunghi)
- Diagrammi Mermaid se utili
- Domande chiarificatrici se ambiguo

### 3. Implementazione con Agenti

```
/architect:implement
```

Delega ai subagenti appropriati basandosi sullo stack rilevato:
- `backend-developer` per codice server
- `frontend-developer` per componenti UI
- `styling-developer` per CSS/styling
- `test-writer` per test
- `code-reviewer` per review finale

## Workflow Consigliato

```
1. /architect:plan <requisiti>     # Crea piano con todo list
2. Rispondi a domande             # Se ambiguita'
3. Approva il piano               # Review e approvazione
4. /architect:implement           # Esegue con subagenti
```

## Memory Bank

```
.architect/
├── architecture.md      # Overview architettura
├── dependencies.md      # Grafo dipendenze
├── decisions.md         # Architecture Decision Records
├── patterns.md          # Pattern e convenzioni
├── tech-debt.md         # Technical debt
├── plans/               # Piani generati
├── diagrams/            # Diagrammi generati
└── reviews/             # Review dei piani
```

Inizializza con `/architect:init`.

## Differenze da Kilo Code

| Aspetto | Kilo Code | Nostro Plugin |
|---------|-----------|---------------|
| Output | Markdown lungo | TodoWrite (conciso) |
| Domande | Limitate | AskUserQuestion attivo |
| Stack | Generico | Generico + claude.md |
| Agenti | N/A | Multi-agent delegation |
| Review | Manuale | Automatica con scoring |

## Esempio: Piano con TodoWrite

```
/architect:plan Aggiungi filtro prodotti per categoria
```

1. Legge claude.md → Django + Vue + Tailwind
2. Chiede: "Filtro lato server o client?"
3. Crea TodoWrite:
   - Aggiungere FilterSet a Product
   - Modificare ProductViewSet
   - Creare FilterComponent.vue
   - Aggiungere stili filtro
   - Scrivere test
4. Mostra diagramma sequenza
5. Chiede approvazione

## Struttura Plugin

```
architect-plugin/
├── .claude-plugin/
│   └── plugin.json
├── agents/
│   ├── architect.md            # Pianificatore (Opus)
│   ├── codebase-analyzer.md    # Analisi (Sonnet)
│   ├── diagram-generator.md    # Diagrammi (Sonnet)
│   ├── plan-reviewer.md        # Review piani (Opus)
│   ├── documentation-writer.md # Docs (Sonnet)
│   ├── backend-developer.md    # Backend generico (Sonnet)
│   ├── frontend-developer.md   # Frontend generico (Sonnet)
│   ├── styling-developer.md    # Styling generico (Sonnet)
│   ├── test-writer.md          # Test (Sonnet)
│   └── code-reviewer.md        # Code review (Sonnet)
├── commands/
│   ├── plan.md
│   ├── design.md
│   ├── review.md
│   ├── diagram.md
│   ├── init.md
│   ├── export.md
│   └── implement.md
├── templates/
│   ├── microservices.md
│   ├── monolith.md
│   ├── serverless.md
│   ├── mvc.md
│   └── plan-schema.json
├── memory-bank/
│   └── README.md
├── hooks/
│   └── hooks.json
├── skills/
│   └── architecture/
│       └── SKILL.md
└── README.md
```

## Versione

**2.0.0** - Refactoring completo: agenti generici, TodoWrite, AskUserQuestion

## Changelog

### 2.0.0 (Breaking Change)
- Agenti rinominati: django→backend, vue→frontend, tailwind→styling
- Agenti leggono stack da claude.md
- plan.md usa TodoWrite come output principale
- Aggiunta fase domande chiarificatrici (AskUserQuestion)
- Diagrammi Mermaid integrati nel flusso
- Ispirato a Kilo Code Architect Mode

### 1.1.2
- Enforce agent delegation in implement

### 1.1.1
- Fix plugin.json manifest format

### 1.1.0
- Aggiunto comando `/architect:implement`
- Aggiunti agenti: django-developer, vue-developer, tailwind-developer
- Aggiunti agenti: test-writer, code-reviewer
- Workflow completo pianificazione + esecuzione

### 1.0.0
- Release iniziale (solo pianificazione)

## Autore

Maurizio Stabile

## Licenza

MIT
