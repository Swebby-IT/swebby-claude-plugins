# Architect Plugin

Plugin completo per pianificazione architetturale e implementazione. Analizza codebase, crea piani dettagliati, genera diagrammi Mermaid/PlantUML, ed esegue con agenti specializzati per Django, Vue 3 e Tailwind CSS.

## Caratteristiche

- **Pianificazione**: Crea piani dettagliati con task, dipendenze, rischi
- **Implementazione**: Esegue piani con agenti specializzati
- **Memory Bank**: Directory `.architect/` per documentazione persistente
- **Diagrammi Automatici**: Mermaid e PlantUML (C4, Sequence, ER, Class)
- **Template Architetturali**: Microservices, Monolith, Serverless, MVC
- **Review Automatica**: Validazione con scoring qualita'
- **Stack Supportato**: Django, Vue 3, Tailwind CSS
- **MCP Support**: Integrazione con code-search per ricerca semantica

## Comandi

### Pianificazione (Read-only)

| Comando | Descrizione |
|---------|-------------|
| `/architect:plan <requisiti>` | Crea piano di implementazione |
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

### Esecuzione

| Agente | Modello | Ruolo |
|--------|---------|-------|
| `django-developer` | Sonnet | Backend Django (models, views, API) |
| `vue-developer` | Sonnet | Frontend Vue 3 (components, stores) |
| `tailwind-developer` | Sonnet | Styling Tailwind CSS |
| `test-writer` | Sonnet | Test Django (pytest) e Vue (Vitest) |
| `code-reviewer` | Sonnet | Code review finale |

## Workflow Consigliato

```
1. /architect:plan <requisiti>     # Crea piano
2. Approva il piano                # Review e approvazione
3. /architect:implement            # Esegue con subagenti
```

## Cosa Viene Chiamato

Quando usi `/architect:implement` su modifiche Django + Vue + Tailwind:

```
Piano approvato
    │
    ├── Task Django (models, views, serializers)
    │   └── architect:django-developer
    │
    ├── Task Vue (components, stores)
    │   └── architect:vue-developer
    │
    ├── Task Tailwind (stili)
    │   └── architect:tailwind-developer
    │
    ├── Test
    │   └── architect:test-writer
    │
    └── Review finale
        └── architect:code-reviewer
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

## Esempi

### Pianifica e Implementa

```
/architect:plan Aggiungi filtro prodotti per categoria con Vue e Tailwind
```

Output piano:
- Task 1: Django FilterSet + ViewSet → `django-developer`
- Task 2: FilterComponent.vue → `vue-developer`
- Task 3: Stili filtro → `tailwind-developer`
- Task 4: Test → `test-writer`

Poi:
```
/architect:implement
```

Esegue tutti i task con i rispettivi agenti.

### Solo Design

```
/architect:design Sistema e-commerce completo
```

Output:
- Architettura C4 con diagrammi
- ADR per decisioni chiave
- Schema database
- API design
- Piano implementazione fasi

### Genera Diagrammi

```
/architect:diagram auth module
```

Output in `.architect/diagrams/`:
- Component diagram
- Sequence diagram login flow

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
│   ├── django-developer.md     # Django (Sonnet)
│   ├── vue-developer.md        # Vue 3 (Sonnet)
│   ├── tailwind-developer.md   # Tailwind (Sonnet)
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

## MCP Supportati

- `mcp__code-search__*` - Ricerca semantica (priorita' alta)
- `mcp__qdrant__*` - Ricerca vettoriale

## Versione

**1.1.0** - Aggiunta implementazione con agenti Django/Vue/Tailwind

## Changelog

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
