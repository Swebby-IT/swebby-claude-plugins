# Swebby Claude Plugins

Marketplace di plugin per Claude Code, focalizzato su sviluppo Django e workflow orchestrati multi-agente.

## 🚀 Installazione

```bash
# Aggiungi il marketplace
/plugin marketplace add mauriziostabile/swebby-claude-plugins

# Visualizza i plugin disponibili
/plugin

# Installa un plugin
/plugin install django-orchestrator@swebby-plugins
```

## 📦 Plugin Disponibili

| Plugin | Descrizione | Categoria |
|--------|-------------|-----------|
| [django-orchestrator](#django-orchestrator) | Sistema multi-agente: Opus pianifica, Sonnet esegue | Development |

---

## Django Orchestrator

Sistema di orchestrazione multi-agente per progetti Django. Trasforma il tuo workflow in un processo strutturato dove Opus analizza e pianifica, mentre subagenti Sonnet eseguono i task in parallelo.

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
├── django-orchestrator-plugin/
│   ├── .claude-plugin/
│   │   └── plugin.json       # Manifest del plugin
│   ├── agents/               # Subagenti specializzati
│   ├── commands/             # Comandi slash
│   └── skills/               # Skill di orchestrazione
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