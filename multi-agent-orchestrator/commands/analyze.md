---
description: Analizza il codebase usando MCP semantici (se disponibili) e grep per comprendere struttura e dipendenze
argument-hint: "<cosa cercare o analizzare>"
---

# Comando: Analizza Codebase

Target analisi: **$ARGUMENTS**

## Obiettivo

Eseguire un'analisi approfondita del codebase per comprendere:
- Dove si trova il codice rilevante
- Come è strutturato
- Quali dipendenze esistono
- Quali pattern vengono usati

**NESSUNA modifica verrà eseguita** - solo raccolta informazioni.

---

## Step 1: Discovery MCP Semantici

### 1.1 Identifica Tool Disponibili

Cerca tra i tool disponibili:

```
MCP da cercare:
- mcp__code-search__*         → Ricerca semantica primaria
- mcp__sourcegraph__*         → Code intelligence
- mcp__github__search*        → GitHub search
- mcp__*__semantic*           → Altri tool semantici
- mcp__*__search*             → Tool ricerca generici
- mcp__*__find*               → Tool di discovery
```

### 1.2 Registra Risultati

```markdown
## MCP Discovery

### Tool Semantici Trovati
| Tool | Tipo | Disponibile |
|------|------|-------------|
| mcp__code-search__query | Semantico | Si/No |
| mcp__sourcegraph__search | Code Intel | Si/No |
| [altro] | [tipo] | Si/No |

### Tool Selezionato per Analisi
**Primario:** [nome tool] - [motivo]
**Fallback:** Grep + Glob
```

---

## Step 2: Ricerca Semantica (se disponibile)

### 2.1 Costruisci Query

Crea query precise basate su "$ARGUMENTS":

```markdown
## Query Semantiche

### Query Principale
"[query che cerca direttamente $ARGUMENTS]"

### Query di Contesto
1. "[query per funzioni correlate]"
2. "[query per import/dipendenze]"
3. "[query per test correlati]"

### Query di Pattern
1. "[cerca pattern architetturali simili]"
2. "[cerca convenzioni di naming]"
```

### 2.2 Esegui Query

Per ogni query:
1. Esegui con l'MCP semantico
2. Registra i risultati
3. Identifica file rilevanti

```markdown
## Risultati Ricerca Semantica

### Query: "[query]"
**Risultati:** N match

| File | Linea | Snippet | Rilevanza |
|------|-------|---------|-----------|
| path/file1.py | 45 | `def func...` | Alta |
| path/file2.py | 120 | `class X...` | Media |

### Query: "[altra query]"
...
```

---

## Step 3: Verifica con Grep (SEMPRE)

### 3.1 Pattern da Cercare

Anche se hai usato ricerca semantica, verifica con grep:

```markdown
## Pattern Grep

### Pattern Esatti
1. `[nome_funzione]` → Trova definizione e usi
2. `class [NomeClasse]` → Trova classe
3. `import.*[modulo]` → Trova import

### Pattern Regex
1. `def.*$ARGUMENTS` → Funzioni correlate
2. `[A-Z][a-z]+$ARGUMENTS` → Naming patterns
```

### 3.2 Esegui Grep

```markdown
## Risultati Grep

### Pattern: `[pattern]`
**Match:** N in M file

| File | Linea | Contenuto |
|------|-------|-----------|
| path/file.py | 45 | `[linea]` |

### Confronto con Ricerca Semantica
- **File trovati da entrambi:** [lista]
- **Solo semantica:** [lista]
- **Solo grep:** [lista]
- **Discrepanze:** [analisi]
```

---

## Step 4: Esplorazione Struttura

### 4.1 Mappa Directory

Usa Glob per capire la struttura:

```markdown
## Struttura Rilevante

### Directory Coinvolte
```
project/
├── src/
│   ├── [modulo1]/      ← [descrizione]
│   └── [modulo2]/      ← [descrizione]
├── tests/
│   └── [test correlati]
└── [altri]
```

### File Chiave Identificati
| File | Ruolo | Priorità Analisi |
|------|-------|------------------|
| path/file1.py | [ruolo] | Alta |
| path/file2.py | [ruolo] | Media |
```

### 4.2 Leggi File Rilevanti

Per i file identificati, leggi e analizza:

```markdown
## Analisi File

### `path/file1.py`

**Struttura:**
- Linee 1-20: Import
- Linee 25-80: Classe X
- Linee 85-150: Funzioni helper

**Elementi Rilevanti per $ARGUMENTS:**
- `def function_name()` (linea 45) - [descrizione]
- `class ClassName` (linea 25) - [descrizione]

**Dipendenze:**
- Import: `from module import X`
- Usato da: `other_file.py`

### `path/file2.py`
...
```

---

## Step 5: Analisi Dipendenze

### 5.1 Grafo Dipendenze

```markdown
## Mappa Dipendenze

### Import Chain
```
file1.py ──imports──► module_a
    │
    └──imports──► module_b ──imports──► module_c

file2.py ──imports──► file1.py
```

### Chi Usa Cosa
| Elemento | Definito in | Usato da |
|----------|-------------|----------|
| `function_x` | file1.py | file2.py, file3.py |
| `ClassY` | models.py | views.py, api.py |
```

### 5.2 Impatto Potenziale

```markdown
## Analisi Impatto

Se modifico `$ARGUMENTS`:

### Impatto Diretto
- `file1.py` - Deve essere modificato

### Impatto Indiretto (Dipendenze)
- `file2.py` - Usa funzioni da file1.py, potrebbe necessitare aggiornamenti
- `test_file1.py` - Test da aggiornare

### Nessun Impatto
- `file3.py` - Non correlato
```

---

## Step 6: Report Finale

```markdown
## Report Analisi: $ARGUMENTS

### Sommario Esecutivo
[2-3 frasi che riassumono i findings principali]

### Metodologia
- **MCP Semantico:** [Si/No] - [nome]
- **Query eseguite:** [N]
- **Pattern grep:** [N]
- **File letti:** [N]

### Risultati Principali

#### Localizzazione Codice
Il codice relativo a "$ARGUMENTS" si trova in:
1. `path/file1.py` - [descrizione] - Linee X-Y
2. `path/file2.py` - [descrizione] - Linee X-Y

#### Struttura Identificata
[Descrizione della struttura/architettura]

#### Dipendenze Chiave
- Dipende da: [lista]
- Usato da: [lista]

#### Pattern Osservati
- [Pattern 1] - [dove e come]
- [Pattern 2] - [dove e come]

### Raccomandazioni

#### Per Modifiche
Se vuoi modificare questo codice:
- Modifica principale: `[file]`
- Aggiorna anche: `[file dipendenti]`
- Test da verificare: `[test files]`

#### Complessità Stimata
- **Modifiche dirette:** N file
- **Modifiche indirette:** M file
- **Test impattati:** X file
- **Agenti stimati:** Y (se implementato con /implement)

### Domande per Approfondimento
1. [Area che potrebbe richiedere ulteriore analisi]
2. [Aspetto non chiaro dai risultati]

### Prossimi Passi
1. `/plan $ARGUMENTS` - Per creare piano dettagliato
2. `/implement $ARGUMENTS` - Per implementare (dopo piano)
```

---

## Note

- Questo comando è **solo analisi**, non modifica nulla
- Usa i risultati per informare decisioni di implementazione
- Se l'analisi non è sufficiente, ripeti con query più specifiche
