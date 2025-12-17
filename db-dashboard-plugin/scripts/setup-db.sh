#!/bin/bash
# setup-db.sh - Script interattivo per configurare la connessione PostgreSQL
# Uso: ./scripts/setup-db.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║         DB Dashboard Plugin - Setup Database                 ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Verifica se esiste già db.yaml
if [ -f "db.yaml" ]; then
    echo "⚠️  File db.yaml già presente."
    read -p "Vuoi sovrascriverlo? (s/N): " overwrite
    if [[ ! "$overwrite" =~ ^[sS]$ ]]; then
        echo "Setup annullato."
        exit 0
    fi
fi

echo ""
echo "Inserisci i dati di connessione PostgreSQL:"
echo "─────────────────────────────────────────────"

read -p "Host [localhost]: " db_host
db_host=${db_host:-localhost}

read -p "Porta [5432]: " db_port
db_port=${db_port:-5432}

read -p "Database: " db_name
if [ -z "$db_name" ]; then
    echo "❌ Il nome del database è obbligatorio!"
    exit 1
fi

read -p "Username: " db_user
if [ -z "$db_user" ]; then
    echo "❌ L'username è obbligatorio!"
    exit 1
fi

read -sp "Password: " db_password
echo ""

read -p "Schema [public]: " db_schema
db_schema=${db_schema:-public}

# Costruisci URL di connessione
CONNECTION_URL="postgresql://${db_user}:${db_password}@${db_host}:${db_port}/${db_name}"

echo ""
echo "─────────────────────────────────────────────"
echo "📝 Creazione file di configurazione..."

# Crea db.yaml
cat > db.yaml << EOF
# db.yaml - Configurazione Database PostgreSQL
# Generato automaticamente il $(date +"%Y-%m-%d %H:%M:%S")

connection:
  url: "${CONNECTION_URL}"

options:
  schema: ${db_schema}
  read_only: true
  timeout: 30
  row_limit: 1000

schema_hints:
  important_tables: []
  relationships: []
EOF

echo "✅ File db.yaml creato!"

# Aggiorna .mcp.json nella directory corrente
echo ""
echo "📝 Aggiornamento configurazione MCP..."

cat > .mcp.json << EOF
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "${CONNECTION_URL}"
      ]
    }
  }
}
EOF

echo "✅ File .mcp.json creato!"

# Test connessione (opzionale)
echo ""
read -p "Vuoi testare la connessione? (s/N): " test_conn
if [[ "$test_conn" =~ ^[sS]$ ]]; then
    echo "🔄 Test connessione in corso..."
    
    if command -v psql &> /dev/null; then
        if PGPASSWORD="$db_password" psql -h "$db_host" -p "$db_port" -U "$db_user" -d "$db_name" -c "SELECT 1;" &> /dev/null; then
            echo "✅ Connessione riuscita!"
        else
            echo "❌ Connessione fallita. Verifica i parametri."
        fi
    else
        echo "⚠️  psql non trovato. Installa postgresql-client per testare."
    fi
fi

# Crea directory output se non esiste
mkdir -p output

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Setup completato! 🎉                      ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║                                                              ║"
echo "║  File creati:                                                ║"
echo "║  • db.yaml      - Configurazione database                    ║"
echo "║  • .mcp.json    - Configurazione MCP server                  ║"
echo "║  • output/      - Directory per i report                     ║"
echo "║                                                              ║"
echo "║  Prossimi passi:                                             ║"
echo "║  1. Riavvia Claude Code per caricare MCP                     ║"
echo "║  2. Usa: /db-dashboard:dashboard <richiesta>                 ║"
echo "║                                                              ║"
echo "╚══════════════════════════════════════════════════════════════╝"
