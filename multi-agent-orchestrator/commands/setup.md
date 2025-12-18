---
description: Configura MCP code-search con Qdrant per ricerca semantica nel codebase
argument-hint: ""
---

# Comando: Setup MCP Code-Search con Qdrant

Questo comando configura automaticamente l'MCP code-search con Qdrant per abilitare la ricerca semantica nel codebase.

---

## FASE 1: Verifica MCP Esistente

### 1.1 Controlla MCP Disponibili

Verifica se esiste già un MCP code-search o un MCP che usa Qdrant:

```
Cerca tra i tool disponibili:
- mcp__code-search__*
- mcp__qdrant__*
- mcp__*qdrant*
- mcp__*semantic*
```

**Se trovi un MCP code-search o qdrant funzionante:**

```markdown
## MCP Code-Search Già Configurato

Ho rilevato che hai già un MCP per la ricerca semantica configurato:
- **MCP trovato:** [nome]

Non è necessaria alcuna configurazione aggiuntiva.
Il plugin multi-agent-orchestrator utilizzerà automaticamente questo MCP.
```

**STOP** - Non procedere oltre se MCP già configurato.

---

**Se NON trovi MCP code-search/qdrant, procedi con FASE 2.**

---

## FASE 2: Verifica Docker

### 2.1 Controlla se Docker è Installato

Esegui:
```bash
docker --version
```

**Se Docker è installato:** Vai a FASE 3

**Se Docker NON è installato:** Procedi con 2.2

### 2.2 Installa Docker

Rileva il sistema operativo e installa Docker:

#### Per Debian/Ubuntu:

```bash
# Aggiorna e installa dipendenze
apt update
apt install -y ca-certificates curl

# Aggiungi chiave GPG Docker
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc
chmod a+r /etc/apt/keyrings/docker.asc

# Aggiungi repository Docker
tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/debian
Suites: $(. /etc/os-release && echo "$VERSION_CODENAME")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

# Installa Docker
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

#### Per macOS:

```markdown
Docker Desktop non è installato.

Per installare Docker su macOS:
1. Scarica Docker Desktop da https://www.docker.com/products/docker-desktop
2. Installa e avvia Docker Desktop
3. Riesegui `/setup` dopo l'installazione
```

**STOP** su macOS se Docker non installato - richiede installazione manuale.

### 2.3 Verifica Installazione Docker

```bash
docker --version
docker run hello-world
```

Se fallisce, mostra errore e chiedi all'utente di verificare l'installazione.

---

## FASE 3: Avvia Qdrant

### 3.1 Crea Directory Dati

```bash
mkdir -p /opt/qdrant/data
```

### 3.2 Avvia Container Qdrant

```bash
docker run -d \
    --name qdrant \
    --restart unless-stopped \
    -p 6333:6333 \
    -v /opt/qdrant/data:/qdrant/storage \
    qdrant/qdrant
```

### 3.3 Verifica Qdrant

```bash
# Attendi avvio
sleep 5

# Verifica che Qdrant risponda
curl -s http://127.0.0.1:6333/health
```

Se non risponde, mostra errore e log del container.

---

## FASE 4: Installa qdrant-mcp-server

### 4.1 Clona e Compila

```bash
# Crea directory
mkdir -p /opt/qdrant-mcp-server

# Clona repository
git clone https://github.com/anthropics/qdrant-mcp-server.git /opt/qdrant-mcp-server

# Installa dipendenze e compila
cd /opt/qdrant-mcp-server
npm install
npm run build
```

### 4.2 Verifica Installazione

```bash
ls -la /opt/qdrant-mcp-server/build/index.js
```

Se il file non esiste, mostra errore di compilazione.

---

## FASE 5: Configurazione MCP

### 5.1 Chiedi Configurazione all'Utente

Usa **AskUserQuestion** per raccogliere i parametri:

**Domanda 1: Provider Embedding**
```
Quale provider vuoi usare per gli embedding?
- OpenRouter (Recommended) - Supporta molti modelli, prezzi competitivi
- OpenAI - Provider originale, alta qualità
- Altro - Specifica manualmente
```

**Domanda 2: API Key**
```
Inserisci la tua API Key per il provider selezionato:
(Per OpenRouter: inizia con sk-or-v1-...)
```

**Domanda 3: Path da Indicizzare**
```
Quale directory vuoi indicizzare?
- Directory corrente: [pwd]
- /srv/app
- Altro path
```

### 5.2 Valori Default

Se l'utente non specifica, usa questi default:

```
EMBEDDING_PROVIDER: "openai"
EMBEDDING_BASE_URL: "https://openrouter.ai/api/v1"
EMBEDDING_MODEL: "qwen/qwen3-embedding-8b"
EMBEDDING_DIMENSIONS: "4096"
AUTO_INDEX_IGNORE: "node_modules,.git,*.lock,*.min.js,*.min.css,.env*,*.sqlite,.idea,.vscode,dist,build,static,__pycache__"
WATCH_FILES: "true"
COLLECTION_NAME: "code"
CODE_SEARCH_LIMIT: "5"
CODE_CHUNK_SIZE: "400"
```

### 5.3 Genera Configurazione MCP

Crea il blocco di configurazione per `~/.claude/settings.json`:

```json
{
  "mcpServers": {
    "code-search": {
      "type": "stdio",
      "command": "node",
      "args": [
        "/opt/qdrant-mcp-server/build/index.js"
      ],
      "env": {
        "QDRANT_URL": "http://127.0.0.1:6333",
        "EMBEDDING_PROVIDER": "[PROVIDER]",
        "EMBEDDING_BASE_URL": "[BASE_URL]",
        "EMBEDDING_MODEL": "[MODEL]",
        "OPENAI_API_KEY": "[API_KEY]",
        "AUTO_INDEX_PATH": "[PATH]",
        "AUTO_INDEX_IGNORE": "node_modules,.git,*.lock,*.min.js,*.min.css,.env*,*.sqlite,.idea,.vscode,dist,build,static,__pycache__",
        "WATCH_FILES": "true",
        "COLLECTION_NAME": "code",
        "CODE_SEARCH_LIMIT": "5",
        "CODE_CHUNK_SIZE": "400",
        "EMBEDDING_DIMENSIONS": "4096"
      }
    }
  }
}
```

### 5.4 Aggiungi a Settings

Leggi `~/.claude/settings.json` (o crea se non esiste) e aggiungi/aggiorna la sezione `mcpServers.code-search`.

```bash
# Backup settings esistenti
cp ~/.claude/settings.json ~/.claude/settings.json.backup 2>/dev/null || true
```

Poi usa Edit tool per aggiungere la configurazione.

---

## FASE 6: Verifica Finale

### 6.1 Test Connessione

```bash
# Verifica Qdrant
curl -s http://127.0.0.1:6333/collections

# Verifica MCP server può avviarsi
node /opt/qdrant-mcp-server/build/index.js --help 2>&1 | head -5
```

### 6.2 Report Finale

```markdown
## Setup Completato

### Componenti Installati
- [x] Docker: funzionante
- [x] Qdrant: running su http://127.0.0.1:6333
- [x] qdrant-mcp-server: /opt/qdrant-mcp-server/build/index.js
- [x] Configurazione MCP: ~/.claude/settings.json

### Configurazione
- **Provider:** [provider]
- **Modello:** [model]
- **Path indicizzato:** [path]

### Prossimi Passi
1. **Riavvia Claude Code** per caricare il nuovo MCP
2. L'indicizzazione inizierà automaticamente
3. Usa `/implement` - la ricerca semantica sarà attiva

### Comandi Utili
```bash
# Verifica stato Qdrant
docker ps | grep qdrant

# Log Qdrant
docker logs qdrant

# Riavvia Qdrant
docker restart qdrant

# Verifica collezioni
curl http://127.0.0.1:6333/collections
```
```

---

## Gestione Errori

### Se Docker non si installa
Mostra istruzioni manuali per il sistema operativo specifico.

### Se Qdrant non si avvia
```bash
# Controlla se porta già in uso
lsof -i :6333

# Controlla log
docker logs qdrant
```

### Se MCP server non compila
```bash
# Verifica Node.js versione
node --version  # Richiede >= 18

# Reinstalla dipendenze
cd /opt/qdrant-mcp-server
rm -rf node_modules
npm install
npm run build
```

### Se la configurazione non funziona
Verifica che `~/.claude/settings.json` sia JSON valido e che l'API key sia corretta.
