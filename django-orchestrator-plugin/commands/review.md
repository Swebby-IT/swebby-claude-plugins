---
description: Esegui code review sui file specificati o sulle modifiche recenti
argument-hint: "<file o cartella da revisionare> oppure 'recent' per ultime modifiche"
---

# Comando: Code Review

Target review: **$ARGUMENTS**

## Istruzioni

### Se argomento è un file/cartella:
Revisiona i file specificati.

### Se argomento è "recent":
Usa `git diff` per trovare le modifiche recenti e revisionarle.

### Se nessun argomento:
Chiedi all'utente cosa vuole revisionare.

## Workflow

### Step 1: Identifica File

```bash
# Per modifiche recenti
git diff --name-only HEAD~1

# Oppure file specificato
ls -la <path>
```

### Step 2: Delega Review

Delega a `code-reviewer` con istruzioni:

```
Revisiona i seguenti file per:
1. Sicurezza
2. Performance
3. Best practices Django
4. Qualità codice

File da revisionare:
- [lista file]
```

### Step 3: Presenta Report

Mostra il report del code-reviewer all'utente con:
- Sommario problemi
- Dettagli per ogni issue
- Suggerimenti di fix
- Verdetto finale

### Step 4: Azioni Consigliate

Se ci sono problemi critici/alti:
- Suggerisci di usare `/fix <problema>` per risolverli
- Oppure offri di delegare le fix ai subagenti

---

## Output Atteso

Il code-reviewer produrrà un report nel formato standard con classificazione dei problemi per severità.
