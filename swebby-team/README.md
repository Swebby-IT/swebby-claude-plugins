# 🎯 Swebby Team v2 — Agent Teams

Orchestratore multi-agente per Claude Code con **Agent Teams (TeammateTool)**. Opus 4.6 come team leader che orchestra teammate Researcher e Developer che **comunicano tra loro** via inbox.

```
┌─────────────────────────────────────────────────┐
│        TEAM LEAD (Opus 4.6)                      │
│   Pianifica · Spawna · Coordina · Verifica       │
│      ⛔ Zero lavoro diretto                      │
│      ✅ Usa TeammateTool (NON Task)              │
└──────────┬──────────┬───────────┬───────────────┘
           │          │           │
    ┌──────▼──┐  ┌────▼─────┐  ┌─▼──────────┐
    │RESEARCHER│  │DEVELOPER │  │DEVELOPER   │
    │(teammate)│◄►│(teammate)│◄►│(teammate)  │
    │          │  │          │  │            │
    │• Analisi │  │• Codice  │  │• Codice    │
    │• Ricerca │  │• Fix     │  │• Feature   │
    │• Review  │  │• Feature │  │• Arch.     │
    └──────────┘  └──────────┘  └────────────┘
         ◄──── comunicano via inbox ────►
```

## Differenza dalla v1

| Aspetto | v1 (Task/Subagent) | v2 (Agent Teams) |
|---------|-------------------|------------------|
| Tool | `Task()` | `Teammate()` / `TeammateTool` |
| Comunicazione | Solo verso orchestratore | Tra TUTTI i teammate |
| Task list | Nessuna condivisa | `TaskCreate/TaskUpdate/TaskList` |
| Coordinamento | Sequenziale tramite lead | Peer-to-peer via inbox |
| Shutdown | Automatico | Controllato (`requestShutdown` + `cleanup`) |

## Prerequisiti

- Claude Code
- Accesso ai modelli Opus 4.6 e Sonnet
- **Agent Teams abilitato**:

```bash
claude settings set env.CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS 1
```

## Installazione

### Da GitHub (plugin marketplace)

```bash
/plugin marketplace add Swebby-IT/swebby-claude-plugins
/plugin install swebby-team
```

### Manuale

```bash
git clone https://github.com/Swebby-IT/swebby-claude-plugins.git
cd swebby-claude-plugins/swebby-team
bash install.sh /path/to/your/project
```

## Comandi

| Comando | Uso | Esempio |
|---------|-----|---------|
| `/run` | Task completo con Agent Team | `/run Aggiungi autenticazione OAuth2` |

## Come Funziona

1. **Tu dai un task** → Il team lead analizza e scompone
2. **Piano di esecuzione** → Mostra fasi, teammate, modelli, dipendenze
3. **Conferma** → Chiede ok prima di creare il team
4. **`spawnTeam`** → Crea il team
5. **`TaskCreate`** → Crea task list condivisa
6. **`spawn`** → Spawna teammate con brief e istruzioni di comunicazione
7. **Teammate lavorano** → Si coordinano via inbox, aggiornano task list
8. **Team lead monitora** → Legge inbox, valida, coordina
9. **Verifica** → Reviewer teammate controlla il tutto
10. **`requestShutdown` + `cleanup`** → Chiude ordinatamente
11. **Report finale**

## Regole Chiave

- **Zero lavoro diretto**: il team lead NON tocca mai file, codice, terminale
- **TeammateTool ONLY**: NON usa mai il tool `Task`, SOLO `Teammate`
- **Comunicazione reale**: i teammate comunicano tra loro via inbox
- **Task list condivisa**: ogni teammate fa claim e aggiorna i task
- **Scaling automatico**: da 2 a 8 teammate in base alla complessità
- **Modello adattivo**: Sonnet per default, Opus per task critici
- **Escalation**: se Sonnet fallisce 2x → shutdown e respawn con Opus

## Licenza

MIT
