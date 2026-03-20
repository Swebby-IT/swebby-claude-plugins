# claude-memory configuration
version: 1

# Qdrant connection (per indicizzazione diretta)
qdrant:
  host: localhost
  port: 6333
  collection: {collection_name}

# Embeddings — provider: ollama | openai | openrouter
embeddings:
  provider: ollama                 # cambia in "openai" o "openrouter" se preferisci
  model: nomic-embed-text          # modello embedding

  # Ollama (locale, gratuito)
  ollama_host: http://localhost:11434

  # OpenAI (richiede API key)
  # openai_api_key: ""             # oppure export OPENAI_API_KEY
  # openai_base_url: https://api.openai.com/v1
  # model: text-embedding-3-small  # 1536 dim, economico

  # OpenRouter (richiede API key)
  # openrouter_api_key: ""         # oppure export OPENROUTER_API_KEY
  # openrouter_base_url: https://openrouter.ai/api/v1

# Comportamento memoria
memory:
  # Quanti learnings caricare al SessionStart
  max_learnings_on_start: 10
  # Quante sessioni passate indicizzare (in giorni)
  session_retention_days: 60
  # Cercare contesto in Qdrant al SessionStart (richiede embedding)
  semantic_search_on_start: true
  # Numero massimo di risultati Qdrant al SessionStart
  max_search_results: 5

# Comportamento sessione
session:
  # Generare automaticamente session log al Stop
  auto_session_log: true
  # Includere git diff nel session log
  include_git_diff: true
  # Max lunghezza git diff da salvare (caratteri)
  max_diff_length: 5000
  # Slug del session log: "git" (dall'ultimo commit) o "timestamp"
  slug_strategy: git

# Comportamento flush (PreCompact)
flush:
  # Abilitare il pre-compaction flush
  enabled: true
  # Aggiornare CONTEXT.md durante il flush
  update_context_on_flush: true

# File da indicizzare in Qdrant (oltre ai .memory/)
extra_index_paths:
  - docs/
  # - README.md
  # - CHANGELOG.md

# Git
git:
  # Quanti commit indietro guardare per il session log
  log_depth: 20
  # Includere .memory/ nei commit (raccomandato: sì)
  track_memory_files: true
