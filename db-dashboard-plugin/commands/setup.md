---
description: Configura la connessione al database PostgreSQL per il plugin db-dashboard
argument-hint: [connection_url] es. postgresql://user:pass@localhost:5432/mydb
allowed-tools: Read, Write, Bash
---

# Setup Database Connection

Configura la connessione al database PostgreSQL.

## Se viene fornito un URL di connessione

URL fornito: `$ARGUMENTS`

1. Valida il formato dell'URL (deve iniziare con `postgresql://`)
2. Crea il file `db.yaml` con l'URL fornito
3. Aggiorna `.mcp.json` con la configurazione MCP
4. Crea la directory `output/` se non esiste

## Se non viene fornito un URL

Guida l'utente nella configurazione:

1. Chiedi i parametri di connessione:
   - Host (default: localhost)
   - Porta (default: 5432)
   - Nome database (obbligatorio)
   - Username (obbligatorio)
   - Password (obbligatorio)
   - Schema (default: public)

2. Costruisci l'URL: `postgresql://user:password@host:port/database`

3. Crea i file di configurazione

## File da creare

### db.yaml
```yaml
connection:
  url: "[URL_CONNESSIONE]"

options:
  schema: public
  read_only: true
  timeout: 30
  row_limit: 1000

schema_hints:
  important_tables: []
  relationships: []
```

### .mcp.json
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "[URL_CONNESSIONE]"
      ]
    }
  }
}
```

## Istruzioni finali

Dopo aver creato i file:
1. Informa l'utente di riavviare Claude Code per caricare il server MCP
2. Suggerisci di testare con: `/db-dashboard:dashboard mostrami le tabelle disponibili`
3. Ricorda di popolare `schema_hints` in db.yaml per risultati migliori
