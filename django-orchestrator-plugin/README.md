# Django Orchestrator Plugin

Sistema di orchestrazione multi-agente per progetti Django. Opus pianifica, Sonnet esegue.

## 🎯 Cosa Fa

Questo plugin trasforma il tuo workflow di sviluppo Django in un sistema orchestrato:

1. **Tu fai la richiesta** → "Aggiungi sistema di notifiche email"
2. **Opus analizza e pianifica** → Crea piano dettagliato con task
3. **Tu approvi** → Confermi il piano
4. **Sonnet esegue** → Subagenti specializzati implementano ogni task
5. **Test automatici** → Verifica che tutto funzioni
6. **Code review** → Quality assurance finale

## 📦 Componenti

### Comandi

| Comando | Descrizione |
|---------|-------------|
| `/implement <desc>` | Workflow completo: pianifica → approva → esegui → testa |
| `/plan <desc>` | Solo pianificazione senza esecuzione |
| `/fix <bug>` | Workflow specializzato per bug fix |
| `/review <target>` | Code review standalone |

### Agenti

| Agente | Modello | Ruolo |
|--------|---------|-------|
| `django-developer` | Sonnet | Implementa codice backend Django |
| `frontend-developer` | Sonnet | Template, Tailwind CSS, JavaScript |
| `test-writer` | Sonnet | Scrive ed esegue test pytest/Django |
| `code-reviewer` | Sonnet | Quality assurance e sicurezza |

### Skill

- **orchestration** - Linee guida per coordinare i subagenti

## 🚀 Installazione

### Opzione 1: Installazione Locale

```bash
# Clona o copia la cartella del plugin
cp -r django-orchestrator-plugin ~/.claude/plugins/

# Riavvia Claude Code
```

### Opzione 2: Da Marketplace Locale

```bash
# Crea marketplace di test
mkdir -p ~/claude-marketplace
cp -r django-orchestrator-plugin ~/claude-marketplace/

# In Claude Code
/plugin marketplace add ~/claude-marketplace
/plugin install django-orchestrator
```

### Opzione 3: Da GitHub (dopo pubblicazione)

```bash
/plugin install your-username/django-orchestrator
```

## 💡 Utilizzo

### Implementare una Feature

```
/implement Aggiungi sistema di wishlist per i prodotti
```

Claude (Opus) creerà un piano dettagliato, aspetterà la tua approvazione, poi coordinerà i subagenti per l'implementazione.

### Solo Pianificazione

```
/plan Refactoring del sistema di autenticazione
```

Ottieni solo il piano senza eseguire modifiche.

### Fix di un Bug

```
/fix Gli ordini non calcolano correttamente lo sconto
```

Workflow ottimizzato per bug fix con root cause analysis.

### Code Review

```
/review vendite/views.py
/review recent
```

Review di file specifici o delle modifiche recenti.

## ⚙️ Configurazione

### Personalizzare gli Agenti

Modifica i file in `agents/` per adattarli al tuo progetto:

```markdown
# agents/django-developer.md

---
name: django-developer
model: sonnet  # Cambia in opus per task complessi
tools: Read, Write, Edit, Bash, Glob, Grep
---

[Istruzioni personalizzate...]
```

### Aggiungere MCP Server

Crea `.mcp.json` nella root del plugin:

```json
{
  "mcpServers": {
    "code-search": {
      "command": "your-mcp-server",
      "args": ["--path", "/srv/app"]
    }
  }
}
```

## 📁 Struttura

```
django-orchestrator-plugin/
├── .claude-plugin/
│   └── plugin.json          # Manifest
├── agents/
│   ├── django-developer.md  # Backend Django
│   ├── frontend-developer.md # Frontend
│   ├── test-writer.md       # Testing
│   └── code-reviewer.md     # QA
├── commands/
│   ├── implement.md         # /implement
│   ├── plan.md              # /plan
│   ├── fix.md               # /fix
│   └── review.md            # /review
├── skills/
│   └── orchestration/
│       └── SKILL.md         # Linee guida orchestrazione
└── README.md
```

## 🔧 Requisiti

- Claude Code v1.0+
- Progetto Django configurato
- (Opzionale) MCP server per ricerca codice

## 📝 Licenza

MIT

## 🤝 Contribuire

Pull request benvenute! Per modifiche importanti, apri prima una issue.
