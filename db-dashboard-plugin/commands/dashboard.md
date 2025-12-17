---
description: Genera una dashboard HTML da query PostgreSQL usando workflow multi-agente (Opus analisi + Sonnet builder)
argument-hint: <richiesta report> es. "mostrami vendite mensili per categoria"
allowed-tools: Read, Write, Bash, mcp__postgres__query, Task
---

# DB Dashboard Generator

Sei il coordinatore del workflow **db-dashboard**. Quando l'utente invoca questo comando:

## Step 1: Verifica Configurazione

1. Cerca il file di configurazione DB nella root del progetto:
   - Prima cerca `db.yaml` 
   - Poi `db.toml`
   - Poi `db.txt` o `db.md`
   
2. Se non trovato, chiedi all'utente di crearlo con questo formato:

```yaml
# db.yaml - Configurazione connessione PostgreSQL
connection:
  url: "postgresql://user:password@host:port/database"
  # oppure componenti separati:
  # host: localhost
  # port: 5432
  # database: mydb
  # user: myuser
  # password: mypassword

options:
  schema: public
  read_only: true
  timeout: 30

# Opzionale: hint per l'agente analista
schema_hints:
  important_tables: []
  relationships: []
```

## Step 2: Delega all'Agente Analyst (Opus)

Usa il subagent **db-analyst** con modello Opus per:
- Analizzare la richiesta dell'utente: `$ARGUMENTS`
- Esplorare lo schema del database
- Generare le query SQL necessarie
- Eseguire le query e raccogliere i risultati
- Creare il file JSON di report in `output/report_<timestamp>.json`

Invoca così:
```
Usa il subagent db-analyst per analizzare questa richiesta: "$ARGUMENTS"
```

## Step 3: Delega all'Agente Builder (Sonnet)

Una volta che il report JSON è pronto, usa il subagent **dashboard-builder** con modello Sonnet per:
- Leggere il report JSON generato
- Creare la dashboard HTML + Tailwind CSS v4 + grafici JS
- Salvare in `output/dashboard_<timestamp>.html`

Invoca così:
```
Usa il subagent dashboard-builder per creare la dashboard dal report: output/report_<timestamp>.json
```

## Step 4: Presenta il Risultato

1. Mostra un riepilogo di cosa è stato generato
2. Indica i file creati:
   - Report JSON: `output/report_*.json`
   - Dashboard HTML: `output/dashboard_*.html`
3. Suggerisci come visualizzare la dashboard (aprire in browser)

## Note Importanti

- Tutte le query devono essere **READ-ONLY** (solo SELECT)
- I report sono **versionati** con timestamp nel nome file
- Se manca la configurazione MCP postgres, guida l'utente a configurarla
