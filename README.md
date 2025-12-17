# Swebby Claude Plugins

Marketplace di plugin per Claude Code, focalizzato su orchestrazione multi-agente intelligente con auto-scaling.

## 🚀 Installazione

```bash
# Aggiungi il marketplace
/plugin marketplace add mauriziostabile/swebby-claude-plugins

# Visualizza i plugin disponibili
/plugin

# Installa un plugin
/plugin install multi-agent-orchestrator@swebby-plugins
/plugin install django-orchestrator@swebby-plugins
```

## 📦 Plugin Disponibili

| Plugin | Descrizione | Categoria |
|--------|-------------|-----------|
| [multi-agent-orchestrator](#multi-agent-orchestrator) | Orchestrazione generica con auto-scaling 1-20 agenti | Development |
| [django-orchestrator](#django-orchestrator) | Sistema multi-agente specifico per Django | Development |

---

## Multi-Agent Orchestrator

Sistema di orchestrazione multi-agente **generico** con auto-scaling intelligente. Funziona con qualsiasi codebase e scala automaticamente da 1 a 20 agenti in base alla complessità del task.

### Caratteristiche Principali

- **Discovery MCP Automatico**: Rileva MCP semantici (code-search, sourcegraph) e li usa per ricerche precise
- **Ricerca Intelligente**: Prima semantica, poi verifica con grep
- **Auto-Scaling**: Calcola automaticamente quanti agenti servono (1-20)
- **Esecuzione Parallela**: Massimizza efficienza con agenti indipendenti

### Workflow

```
[Tu] → Richiesta
      ↓
[Orchestratore] → Discovery MCP disponibili
      ↓
[Orchestratore] → Ricerca semantica + grep
      ↓
[Orchestratore] → Piano con calcolo agenti
      ↓
[Tu] → Approva il piano
      ↓
[N Agenti] → Eseguono in parallelo (se indipendenti)
      ↓
[Orchestratore] → Verifica + Report finale
```

### Comandi

| Comando | Descrizione |
|---------|-------------|
| `/implement <desc>` | Workflow completo: discovery → piano → scaling → esecuzione |
| `/plan <desc>` | Solo pianificazione con calcolo agenti |
| `/analyze <desc>` | Solo analisi codebase con MCP/grep |

### Regole di Scaling

| Scenario | Agenti |
|----------|--------|
| Modifiche collegate (stessa sezione/dipendenze) | 1 |
| File diversi indipendenti | 1 per file |
| Stesso file, sezioni distanti (>50 linee) | Separati |
| Massimo | 20 |

### Esempio d'Uso

```bash
# Implementa una feature
/implement Aggiungi sistema di notifiche push

# Claude:
# 1. Cerca MCP semantici disponibili
# 2. Esegue ricerca semantica + grep
# 3. Crea piano: "5 file indipendenti → 5 agenti"
# 4. Aspetta approvazione
# 5. Lancia 5 agenti in parallelo
# 6. Verifica e report
```

---

## Django Orchestrator

Sistema di orchestrazione multi-agente **specifico per Django**. Trasforma il tuo workflow in un processo strutturato dove Opus analizza e pianifica, mentre subagenti Sonnet eseguono i task in parallelo.

### Workflow

```
[Tu] → Richiesta
      ↓
[Opus] → Analisi + Piano dettagliato
      ↓
[Tu] → Approva il piano
      ↓
[Sonnet] → Subagenti eseguono in parallelo
      ↓
[Opus] → Verifica + Report finale
```

### Comandi

| Comando | Descrizione |
|---------|-------------|
| `/implement <desc>` | Workflow completo: pianifica → approva → esegui → testa → review |
| `/plan <desc>` | Solo pianificazione, senza esecuzione |
| `/fix <bug>` | Workflow ottimizzato per bug fix |
| `/review <target>` | Code review su file o modifiche recenti |

### Agenti Inclusi

| Agente | Modello | Specializzazione |
|--------|---------|------------------|
| `django-developer` | Sonnet | Backend Django (models, views, API) |
| `frontend-developer` | Sonnet | Template, Tailwind CSS, JavaScript |
| `test-writer` | Sonnet | Test pytest/Django, coverage |
| `code-reviewer` | Sonnet | QA, sicurezza, best practices |

### Esempio d'Uso

```bash
# Avvia Claude Code con Opus
claude --model opus

# Implementa una feature
/implement Aggiungi sistema di wishlist per i prodotti

# Claude creerà un piano dettagliato e aspetterà la tua approvazione
# Dopo l'ok, coordinerà i subagenti per l'implementazione
```

---

## 🛠️ Per Sviluppatori

### Struttura del Marketplace

```
swebby-claude-plugins/
├── .claude-plugin/
│   └── marketplace.json      # Manifest del marketplace
├── multi-agent-orchestrator/
│   ├── .claude-plugin/
│   │   └── plugin.json       # Manifest del plugin
│   ├── agents/               # Agente generico code-modifier
│   ├── commands/             # implement, plan, analyze
│   ├── skills/               # Logica orchestrazione con auto-scaling
│   └── hooks/                # Enforcement workflow
├── django-orchestrator-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json       # Manifest del plugin
│   ├── agents/               # Subagenti Django specializzati
│   ├── commands/             # Comandi slash
│   └── skills/               # Skill di orchestrazione Django
└── README.md
```

### Contribuire

1. Fork del repository
2. Crea un branch (`git checkout -b feature/nuovo-plugin`)
3. Commit (`git commit -m 'Aggiunge nuovo plugin'`)
4. Push (`git push origin feature/nuovo-plugin`)
5. Apri una Pull Request

---

## 📄 Licenza

MIT

## 👤 Autore

**Maurizio Stabile**

---

## 🔗 Link Utili

- [Documentazione Plugin Claude Code](https://code.claude.com/docs/en/plugins)
- [Documentazione Marketplace](https://code.claude.com/docs/en/plugin-marketplaces)