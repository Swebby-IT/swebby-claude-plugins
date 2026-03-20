---
description: "Configura Qdrant e il provider di embeddings per claude-memory (interattivo)"
argument-hint: "[ollama|openai|openrouter]"
---

# /configure-qdrant — Configurazione Interattiva Qdrant + Embeddings

Devi configurare il sistema di indicizzazione per claude-memory in modo **interattivo**, chiedendo all'utente ogni parametro necessario.

## Argomenti

$ARGUMENTS

---

## STEP 1: Verifica prerequisiti

1. Controlla che `.memory/config.yaml` esista. Se non esiste, dì di lanciare `/memory-init` prima.
2. Leggi la configurazione attuale da `.memory/config.yaml`.

---

## STEP 2: Chiedi il provider di embeddings

Se non specificato negli argomenti, **CHIEDI ALL'UTENTE**:

> Quale provider di embeddings vuoi usare?
> 1. **ollama** — locale, gratuito, richiede Ollama installato
> 2. **openai** — cloud, richiede API key, modello consigliato: `text-embedding-3-small`
> 3. **openrouter** — cloud, richiede API key, accesso a molti modelli

**ATTENDI la risposta dell'utente prima di procedere.**

---

## STEP 3: Chiedi i parametri in base al provider scelto

### Se **ollama**:

**Chiedi all'utente**: "Qual è l'URL di Ollama? (default: http://localhost:11434)"

- Verifica che Ollama sia raggiungibile all'URL indicato:
  ```bash
  curl -s <URL>/api/tags | head -5
  ```
- Chiedi quale modello di embedding: "Quale modello? (default: nomic-embed-text)"
- Se il modello non è presente, suggerisci: `ollama pull <modello>`

### Se **openai**:

**Chiedi all'utente**: "Inserisci la tua OpenAI API key (oppure conferma che hai impostato la env var OPENAI_API_KEY):"

- Se l'utente dà la key, salvala in config.yaml (campo `openai_api_key`)
- Se preferisce la env var, verifica che esista: `echo $OPENAI_API_KEY | head -c 10`
- Chiedi il modello: "Quale modello? (default: text-embedding-3-small, alternativa: text-embedding-3-large)"

### Se **openrouter**:

**Chiedi all'utente**: "Inserisci la tua OpenRouter API key (oppure conferma che hai impostato la env var OPENROUTER_API_KEY):"

- Se l'utente dà la key, salvala in config.yaml (campo `openrouter_api_key`)
- Se preferisce la env var, verifica che esista
- Chiedi il modello: "Quale modello embedding? (default: text-embedding-3-small)"

---

## STEP 4: Configura Qdrant

**Chiedi all'utente**: "Qdrant host e porta? (default: localhost:6333)"

Verifica connessione:
```bash
curl -s http://<host>:<port>/collections | head -5
```

**Chiedi**: "Nome della collection? (default: memory_<nome_directory_progetto>)"

---

## STEP 5: Scrivi la configurazione

Aggiorna `.memory/config.yaml` con i parametri raccolti. Aggiorna SOLO la sezione `embeddings` e `qdrant`, non toccare il resto.

---

## STEP 6: Testa e indicizza

1. Esegui:
   ```bash
   claude-memory status
   ```
2. Se tutto ok, chiedi: "Vuoi eseguire l'indicizzazione iniziale adesso? (sì/no)"
3. Se sì:
   ```bash
   claude-memory reindex
   ```

---

## STEP 7: Report

Mostra un riepilogo:
- Provider: [ollama/openai/openrouter]
- Modello: [nome]
- Qdrant: [host:port] / collection: [nome]
- Chunk indicizzati: [N]
