# 📊 DB Dashboard Plugin per Claude Code

Plugin multi-agente per generare dashboard HTML interattive da database PostgreSQL.

## ✨ Caratteristiche

- **🤖 Workflow Multi-Agente**: 
  - **Opus** (db-analyst) per analisi dati e generazione query
  - **Sonnet** (dashboard-builder) per creazione UI
  
- **📈 Grafici Avanzati**: 
  - Chart.js per grafici standard
  - Apache ECharts per visualizzazioni complesse
  
- **🎨 Design Moderno**:
  - Tailwind CSS v4
  - Dark mode integrato
  - Responsive design
  - Export PDF

- **🔒 Sicurezza**:
  - Query read-only
  - Validazione input

## 🚀 Installazione

### Opzione 1: Installazione locale

```bash
# Clona o scarica il plugin
cd ~/.claude/plugins/
unzip db-dashboard-plugin.zip

# Oppure clona da git
git clone <repo-url> db-dashboard
```

### Opzione 2: Da Claude Code

```
/plugin install <path-to-plugin>
```

## ⚙️ Configurazione

### 1. Setup Database

```bash
# Metodo interattivo
/db-dashboard:setup

# Oppure con URL diretto
/db-dashboard:setup postgresql://user:pass@localhost:5432/mydb
```

### 2. File di Configurazione

Il plugin crea automaticamente:

**`db.yaml`** - Configurazione database:
```yaml
connection:
  url: "postgresql://user:pass@localhost:5432/mydb"

options:
  schema: public
  read_only: true
  timeout: 30

schema_hints:
  important_tables:
    - users
    - orders
  relationships:
    - "orders.user_id -> users.id"
```

**`.mcp.json`** - Server MCP PostgreSQL:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres", "..."]
    }
  }
}
```

### 3. Riavvia Claude Code

Dopo la configurazione, riavvia Claude Code per caricare il server MCP.

## 📖 Utilizzo

### Comando Principale

```
/db-dashboard:dashboard <richiesta in linguaggio naturale>
```

### Esempi

```bash
# Vendite
/db-dashboard:dashboard mostrami le vendite mensili per categoria

# Utenti
/db-dashboard:dashboard analizza la distribuzione geografica degli utenti

# Performance
/db-dashboard:dashboard quali sono i prodotti più venduti nell'ultimo trimestre

# Trend
/db-dashboard:dashboard confronta le vendite 2023 vs 2024 per mese
```

### Altri Comandi

```bash
# Lista report generati
/db-dashboard:list

# Pulisci report vecchi (mantieni ultimi 5)
/db-dashboard:cleanup 5

# Riconfigura database
/db-dashboard:setup
```

## 📁 Struttura Output

```
output/
├── report_20240115_103000.json      # Dati e piano visualizzazione
└── dashboard_20240115_103000.html   # Dashboard HTML completa
```

### Formato Report JSON

```json
{
  "metadata": {
    "report_id": "uuid",
    "generated_at": "2024-01-15T10:30:00Z",
    "request": "mostrami le vendite mensili"
  },
  "analysis": {
    "summary": "Analisi vendite...",
    "key_findings": ["..."]
  },
  "data": {
    "queries_executed": [...],
    "results": {...},
    "aggregations": {...}
  },
  "visualization_plan": {
    "recommended_charts": [...]
  }
}
```

## 🎨 Tipi di Grafico Supportati

| Tipo | Uso Consigliato |
|------|-----------------|
| `bar` | Confronti tra categorie |
| `horizontal_bar` | Molte categorie o nomi lunghi |
| `line` | Trend temporali |
| `area` | Trend con enfasi sul volume |
| `pie` / `doughnut` | Distribuzioni percentuali |
| `scatter` | Correlazioni tra variabili |
| `heatmap` | Matrici di dati |
| `kpi_card` | Singoli valori importanti |
| `table` | Dati dettagliati |

## 🔧 Personalizzazione

### Schema Hints

Migliora i risultati aggiungendo hint nel `db.yaml`:

```yaml
schema_hints:
  important_tables:
    - orders
    - products
    - customers
  
  relationships:
    - "orders.customer_id -> customers.id"
    - "order_items.product_id -> products.id"
  
  date_fields:
    orders: created_at
    
  common_metrics:
    - name: "revenue"
      table: orders
      aggregation: "SUM(total)"
```

### Colori Dashboard

Il builder usa una palette blue-purple di default. Puoi suggerire alternative nella richiesta:

```
/db-dashboard:dashboard vendite per regione con colori verde-arancio
```

## ❓ Troubleshooting

### "MCP server not found"

1. Verifica che `.mcp.json` sia nella root del progetto
2. Riavvia Claude Code
3. Controlla `/mcp` per vedere i server attivi

### "Connection refused"

1. Verifica che PostgreSQL sia in esecuzione
2. Controlla le credenziali in `db.yaml`
3. Verifica firewall/network

### Query lente

1. Aggiungi indici alle colonne usate nei WHERE/JOIN
2. Riduci `row_limit` in `db.yaml`
3. Usa filtri temporali nelle richieste

## 📜 Licenza

MIT License

## 🤝 Contributing

Pull request benvenute! Per modifiche importanti, apri prima una issue.
