# Multi-Agent Orchestrator Plugin

Sistema di orchestrazione multi-agente generico con auto-scaling intelligente per Claude Code.

## Caratteristiche

- **Discovery MCP Automatico**: Rileva automaticamente MCP semantici disponibili (code-search, sourcegraph, ecc.)
- **Ricerca Intelligente**: Prima ricerca semantica, poi verifica con grep
- **Pianificazione Dettagliata**: Crea piani completi con approvazione utente
- **Auto-Scaling Agenti**: Calcola automaticamente il numero ottimale di agenti (1-20)
- **Esecuzione Parallela**: Massimizza efficienza lanciando agenti indipendenti in parallelo

## Installazione

```bash
# Clona o copia nella directory dei plugin
cp -r multi-agent-orchestrator ~/.claude/plugins/
```

## Comandi Disponibili

| Comando | Descrizione |
|---------|-------------|
| `/implement <desc>` | Workflow completo: discovery → analisi → piano → scaling → esecuzione |
| `/plan <desc>` | Solo pianificazione con calcolo agenti, senza esecuzione |
| `/analyze <desc>` | Solo analisi codebase con MCP/grep |

## Come Funziona

### 1. Discovery MCP

Il plugin verifica quali tool semantici sono disponibili:
- `mcp__code-search__*` - Ricerca semantica
- `mcp__sourcegraph__*` - Code intelligence
- Altri MCP di ricerca

### 2. Ricerca Intelligente

```
┌─────────────────────┐
│ MCP Semantico       │ ← Se disponibile, usa per primo
│ (code-search, ecc.) │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Verifica Grep       │ ← SEMPRE eseguita come verifica
│                     │
└─────────┬───────────┘
          │
          ▼
┌─────────────────────┐
│ Lettura File        │ ← Contesto completo
└─────────────────────┘
```

### 3. Calcolo Automatico Agenti

**Regole di scaling:**

| Scenario | Agenti |
|----------|--------|
| Modifiche nella stessa sezione | 1 |
| Modifiche con dipendenze | 1 (stesso agente) |
| File diversi indipendenti | 1 per file |
| Stesso file, sezioni distanti (>50 linee) e indipendenti | Separati |
| Massimo | 20 |

**Esempi:**

```
# 1 agente - modifiche collegate
file.py linee 10-30 (funzione A che chiama B)
file.py linee 35-50 (funzione B chiamata da A)

# 3 agenti - modifiche indipendenti
api/users.py (nuovo endpoint)
api/products.py (nuovo endpoint)
api/orders.py (nuovo endpoint)

# 5 agenti - stesso file, sezioni scollegate
handlers.py linee 20-40
handlers.py linee 150-170
handlers.py linee 300-320
handlers.py linee 450-480
handlers.py linee 600-630
```

### 4. Workflow Completo

```
[Richiesta Utente]
       │
       ▼
[Discovery MCP] → Identifica tool disponibili
       │
       ▼
[Ricerca Semantica] → Se MCP disponibile
       │
       ▼
[Verifica Grep] → Sempre eseguita
       │
       ▼
[Crea Piano] → Con calcolo agenti
       │
       ▼
[Chiedi Approvazione] → STOP se incerto
       │
       ▼
[Lancia N Agenti] → Parallelo se indipendenti
       │
       ▼
[Verifica Risultati]
       │
       ▼
[Report Finale]
```

## Struttura Plugin

```
multi-agent-orchestrator/
├── .claude-plugin/
│   └── plugin.json          # Metadata plugin
├── skills/
│   └── orchestration/
│       └── SKILL.md         # Logica orchestrazione
├── commands/
│   ├── implement.md         # Workflow completo
│   ├── plan.md              # Solo pianificazione
│   └── analyze.md           # Solo analisi
├── agents/
│   └── code-modifier.md     # Agente modifiche
├── hooks/
│   └── hooks.json           # Enforcement workflow
└── README.md
```

## Configurazione

Il plugin funziona out-of-the-box. Per risultati ottimali:

1. **Installa MCP semantici** (opzionale ma consigliato):
   - code-search
   - sourcegraph

2. **Il plugin si adatta** automaticamente agli MCP disponibili

## Differenze da django-orchestrator

| Feature | django-orchestrator | multi-agent-orchestrator |
|---------|---------------------|--------------------------|
| Target | Progetti Django | Qualsiasi codebase |
| MCP Discovery | No | Si, automatico |
| Ricerca | Solo grep | Semantica + grep |
| Scaling | Fisso per ruolo | Automatico 1-20 |
| Agenti | Ruoli specifici | Generico code-modifier |

## Best Practices

### Per l'Utente

1. **Descrivi chiaramente** cosa vuoi fare
2. **Approva** il piano prima dell'esecuzione
3. **Rispondi** alle domande se l'orchestratore è incerto

### Per Modifiche Complesse

1. Usa `/analyze` prima per capire la struttura
2. Poi `/plan` per vedere il piano
3. Infine `/implement` per eseguire

## Licenza

MIT
