#!/bin/bash
# /usr/local/bin/mcp-index.sh
# Script per gestire l'indicizzazione del codebase via MCP
# Legge configurazione da .claude.json (struttura Claude Code)

set -e

# Cerca il file di configurazione
find_config() {
  local configs=(
    "$HOME/.claude.json"
    "$HOME/.config/Claude/claude_desktop_config.json"
    "/etc/claude/mcp.json"
  )
  
  for cfg in "${configs[@]}"; do
    if [ -f "$cfg" ]; then
      echo "$cfg"
      return 0
    fi
  done
  
  echo ""
  return 1
}

# Estrai variabili env dalla config MCP (supporta entrambe le strutture)
load_mcp_config() {
  local config_file="$1"
  local server_name="${2:-code-search}"
  local project_path="${3:-/srv/app}"
  
  if [ ! -f "$config_file" ]; then
    echo "❌ Config non trovata: $config_file" >&2
    return 1
  fi
  
  # Prova prima la struttura Claude Code: projects[path].mcpServers[name]
  local env_json=$(jq -r ".projects[\"$project_path\"].mcpServers[\"$server_name\"].env // empty" "$config_file" 2>/dev/null)
  
  # Se non trova, prova la struttura Claude Desktop: mcpServers[name]
  if [ -z "$env_json" ]; then
    env_json=$(jq -r ".mcpServers[\"$server_name\"].env // empty" "$config_file" 2>/dev/null)
  fi
  
  if [ -z "$env_json" ]; then
    echo "❌ Server MCP '$server_name' non trovato in $config_file" >&2
    echo "   Cercato in: projects[\"$project_path\"].mcpServers e mcpServers" >&2
    return 1
  fi
  
  # Esporta tutte le variabili
  while IFS="=" read -r key value; do
    [ -n "$key" ] && export "$key"="$value"
  done < <(echo "$env_json" | jq -r 'to_entries | .[] | "\(.key)=\(.value)"')
  
  # Estrai il comando node - prova entrambe le strutture
  MCP_NODE_SCRIPT=$(jq -r ".projects[\"$project_path\"].mcpServers[\"$server_name\"].args[0] // empty" "$config_file" 2>/dev/null)
  if [ -z "$MCP_NODE_SCRIPT" ]; then
    MCP_NODE_SCRIPT=$(jq -r ".mcpServers[\"$server_name\"].args[0] // empty" "$config_file" 2>/dev/null)
  fi
  export MCP_NODE_SCRIPT
  
  echo "✅ Configurazione caricata per server: $server_name"
}

# Avvia server MCP in background
start_mcp_server() {
  local port="${HTTP_PORT:-3100}"
  
  # Controlla se già in esecuzione
  if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
    echo "✅ Server MCP già in esecuzione su porta $port"
    return 0
  fi
  
  if [ -z "$MCP_NODE_SCRIPT" ]; then
    echo "❌ MCP_NODE_SCRIPT non configurato" >&2
    return 1
  fi
  
  echo "🚀 Avvio server MCP su porta $port..."
  
  export TRANSPORT_MODE="http"
  export HTTP_PORT="$port"
  
  # Avvia in background con log
  nohup node "$MCP_NODE_SCRIPT" > /tmp/mcp-server.log 2>&1 &
  MCP_PID=$!
  echo $MCP_PID > /tmp/mcp-server.pid
  
  # Aspetta che sia pronto
  for i in {1..30}; do
    if curl -s "http://localhost:$port/health" > /dev/null 2>&1; then
      echo "✅ Server MCP avviato (PID: $MCP_PID)"
      return 0
    fi
    sleep 1
  done
  
  echo "❌ Timeout avvio server MCP"
  cat /tmp/mcp-server.log
  return 1
}

# Ferma server MCP
stop_mcp_server() {
  if [ -f /tmp/mcp-server.pid ]; then
    local pid=$(cat /tmp/mcp-server.pid)
    if kill -0 "$pid" 2>/dev/null; then
      echo "🛑 Fermo server MCP (PID: $pid)..."
      kill "$pid"
      rm -f /tmp/mcp-server.pid
    fi
  fi
  # Cerca anche processi orfani
  pkill -f "qdrant-mcp-server" 2>/dev/null || true
}

# Chiama tool MCP
call_mcp() {
  local tool="$1"
  local args="$2"
  local port="${HTTP_PORT:-3100}"
  
  curl -s --max-time 1800 -X POST "http://localhost:$port/mcp" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "{
      \"jsonrpc\": \"2.0\",
      \"id\": 1,
      \"method\": \"tools/call\",
      \"params\": {
        \"name\": \"$tool\",
        \"arguments\": $args
      }
    }" 2>/dev/null || echo '{"error": "timeout or connection failed"}'
}

# Indicizza in background con progress
index_background() {
  local path="$1"
  local port="${HTTP_PORT:-3100}"
  
  echo "📚 Indicizzazione: $path"
  echo "⏳ Processo in background..."
  echo ""
  
  # Avvia curl in background
  nohup bash -c "
    curl -s --max-time 3600 -X POST 'http://localhost:$port/mcp' \
      -H 'Content-Type: application/json' \
      -H 'Accept: application/json, text/event-stream' \
      -d '{
        \"jsonrpc\": \"2.0\",
        \"id\": 1,
        \"method\": \"tools/call\",
        \"params\": {
          \"name\": \"index_codebase\",
          \"arguments\": {\"path\": \"$path\", \"forceReindex\": true}
        }
      }' > /tmp/mcp-index-result.json 2>&1
    echo ''
    echo '✅ Indicizzazione completata!' >> /tmp/mcp-index.log
    cat /tmp/mcp-index-result.json | jq -r '.result.content[0].text // .error.message // \"unknown result\"' >> /tmp/mcp-index.log
  " > /tmp/mcp-index.log 2>&1 &
  
  local bg_pid=$!
  echo "📋 PID processo: $bg_pid"
  echo ""
  echo "Comandi utili:"
  echo "  tail -f /tmp/mcp-index.log        # Segui il log"
  echo "  tail -f /tmp/mcp-server.log       # Log server MCP"
  echo "  cat /tmp/mcp-index-result.json    # Risultato finale"
  echo "  $0 status $path                   # Stato indice"
}

# Main
main() {
  local action="${1:-help}"
  local path="${2:-/srv/app}"
  local query="$3"
  local mcp_server="${MCP_SERVER:-code-search}"
  
  # Carica config
  CONFIG_FILE=$(find_config)
  if [ -z "$CONFIG_FILE" ]; then
    echo "❌ Nessun file di configurazione Claude trovato"
    echo "   Cercati: ~/.claude.json, ~/.config/Claude/claude_desktop_config.json"
    exit 1
  fi
  
  echo "📁 Config: $CONFIG_FILE"
  load_mcp_config "$CONFIG_FILE" "$mcp_server" "$path" || exit 1
  echo "📂 Node script: $MCP_NODE_SCRIPT"
  echo ""
  
  case "$action" in
    start)
      start_mcp_server
      ;;
    
    stop)
      stop_mcp_server
      ;;
    
    clear)
      start_mcp_server
      echo "🗑️  Cancellazione indice: $path"
      call_mcp "clear_index" "{\"path\": \"$path\"}" | jq .
      ;;
    
    index)
      start_mcp_server
      index_background "$path"
      ;;
    
    reindex)
      start_mcp_server
      echo "🗑️  Cancellazione indice: $path"
      call_mcp "clear_index" "{\"path\": \"$path\"}" | jq .
      echo ""
      index_background "$path"
      ;;
    
    status)
      start_mcp_server
      echo "📊 Stato indice: $path"
      call_mcp "get_index_status" "{\"path\": \"$path\"}" | jq .
      ;;
    
    search)
      if [ -z "$query" ]; then
        echo "❌ Specifica una query: $0 search /path \"query\""
        exit 1
      fi
      start_mcp_server
      echo "🔍 Ricerca: $query"
      call_mcp "search_code" "{\"path\": \"$path\", \"query\": \"$query\", \"limit\": 5}" | jq .
      ;;
    
    log)
      tail -f /tmp/mcp-server.log
      ;;

    changes)
      start_mcp_server
      echo "🔄 Re-indicizzazione incrementale: $path"
      call_mcp "reindex_changes" "{\"path\": \"$path\"}" | jq .
      ;;

    watch)
      # Daemon che monitora i file e re-indicizza automaticamente
      start_mcp_server

      # Verifica inotifywait
      if ! command -v inotifywait &> /dev/null; then
        echo "❌ inotifywait non trovato. Installa con: apt-get install inotify-tools"
        exit 1
      fi

      echo "👀 Avvio watch daemon su: $path"
      echo "   Monitoro: modify, create, delete, move"
      echo "   Escludo: .git, __pycache__, node_modules, *.pyc, .claude"
      echo ""
      echo "   Premi Ctrl+C per fermare"
      echo ""

      # File per debouncing - evita re-index multipli ravvicinati
      LAST_REINDEX=0
      DEBOUNCE_SECONDS=5

      inotifywait -m -r -e modify,create,delete,move \
        --exclude '(\.git|__pycache__|node_modules|\.pyc$|\.pyo$|\.claude|\.swp$|~$)' \
        --format '%w%f %e %T' --timefmt '%s' \
        "$path" 2>/dev/null | while read file event timestamp; do

        # Debounce: aspetta che passino N secondi dall'ultimo reindex
        current_time=$(date +%s)
        if (( current_time - LAST_REINDEX < DEBOUNCE_SECONDS )); then
          echo "⏳ [$(date '+%H:%M:%S')] Skip (debounce): $file"
          continue
        fi

        # Filtra file temporanei e non rilevanti
        case "$file" in
          *.swp|*~|*.tmp|*.log|*.pid)
            continue
            ;;
        esac

        echo "📝 [$(date '+%H:%M:%S')] $event: $file"

        # Re-indicizza incrementale
        result=$(call_mcp "reindex_changes" "{\"path\": \"$path\"}" 2>/dev/null)

        if echo "$result" | grep -q '"error"'; then
          echo "   ❌ Errore: $(echo "$result" | jq -r '.error.message // .error // "unknown"')"
        else
          # Estrai stats dal risultato
          stats=$(echo "$result" | jq -r '.result.content[0].text // "ok"' 2>/dev/null | head -1)
          echo "   ✅ $stats"
        fi

        LAST_REINDEX=$current_time
      done
      ;;

    daemon)
      # Avvia watch in background come servizio
      start_mcp_server

      if ! command -v inotifywait &> /dev/null; then
        echo "❌ inotifywait non trovato. Installa con: apt-get install inotify-tools"
        exit 1
      fi

      # Controlla se già in esecuzione
      if [ -f /tmp/mcp-watch.pid ]; then
        old_pid=$(cat /tmp/mcp-watch.pid)
        if kill -0 "$old_pid" 2>/dev/null; then
          echo "⚠️  Watch daemon già in esecuzione (PID: $old_pid)"
          echo "   Usa '$0 daemon-stop' per fermarlo"
          exit 1
        fi
      fi

      echo "🚀 Avvio watch daemon in background: $path"

      nohup "$0" watch "$path" > /tmp/mcp-watch.log 2>&1 &
      daemon_pid=$!
      echo $daemon_pid > /tmp/mcp-watch.pid

      sleep 2
      if kill -0 "$daemon_pid" 2>/dev/null; then
        echo "✅ Daemon avviato (PID: $daemon_pid)"
        echo ""
        echo "Comandi:"
        echo "  tail -f /tmp/mcp-watch.log   # Segui il log"
        echo "  $0 daemon-stop               # Ferma daemon"
        echo "  $0 daemon-status             # Stato daemon"
      else
        echo "❌ Daemon fallito. Controlla /tmp/mcp-watch.log"
        cat /tmp/mcp-watch.log
      fi
      ;;

    daemon-stop)
      if [ -f /tmp/mcp-watch.pid ]; then
        pid=$(cat /tmp/mcp-watch.pid)
        if kill -0 "$pid" 2>/dev/null; then
          echo "🛑 Fermo watch daemon (PID: $pid)..."
          kill "$pid"
          # Uccidi anche i processi figli (inotifywait)
          pkill -P "$pid" 2>/dev/null || true
          rm -f /tmp/mcp-watch.pid
          echo "✅ Daemon fermato"
        else
          echo "⚠️  Daemon non in esecuzione"
          rm -f /tmp/mcp-watch.pid
        fi
      else
        echo "⚠️  Nessun daemon attivo"
      fi
      ;;

    daemon-status)
      echo "📊 Stato daemon:"
      if [ -f /tmp/mcp-watch.pid ]; then
        pid=$(cat /tmp/mcp-watch.pid)
        if kill -0 "$pid" 2>/dev/null; then
          echo "   ✅ In esecuzione (PID: $pid)"
          echo ""
          echo "Ultime 10 righe del log:"
          tail -10 /tmp/mcp-watch.log 2>/dev/null || echo "   (log vuoto)"
        else
          echo "   ❌ Non in esecuzione (PID stale: $pid)"
        fi
      else
        echo "   ❌ Non attivo"
      fi
      ;;

    help|*)
      echo "Uso: $0 <azione> [path] [query]"
      echo ""
      echo "Azioni:"
      echo "  start           - Avvia server MCP"
      echo "  stop            - Ferma server MCP"
      echo "  index <path>    - Indicizza codebase (background)"
      echo "  clear <path>    - Cancella indice"
      echo "  reindex <path>  - Cancella e re-indicizza"
      echo "  changes <path>  - Re-indicizza solo file modificati"
      echo "  status <path>   - Stato indice"
      echo "  search <path> <query> - Cerca nel codice"
      echo "  log             - Mostra log server"
      echo ""
      echo "Watch/Daemon:"
      echo "  watch <path>    - Monitora file e re-indicizza (foreground)"
      echo "  daemon <path>   - Avvia watch in background"
      echo "  daemon-stop     - Ferma daemon"
      echo "  daemon-status   - Stato daemon"
      echo ""
      echo "Esempi:"
      echo "  $0 start"
      echo "  $0 index /srv/app"
      echo "  $0 reindex /srv/app"
      echo "  $0 search /srv/app \"gestione CSS\""
      echo "  $0 daemon /srv/app         # Monitora in background"
      echo "  tail -f /tmp/mcp-watch.log # Segui le modifiche"
      echo ""
      echo "Variabili ambiente:"
      echo "  MCP_SERVER=code-search  # Nome server MCP da usare"
      ;;
  esac
}

main "$@"