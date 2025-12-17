---
description: Correggi un bug con workflow orchestrato (analizza → pianifica → fix → testa)
argument-hint: "<descrizione del bug o errore>"
---

# Comando: Fix Bug

Bug da risolvere: **$ARGUMENTS**

## FASE 1: Investigazione

### 1.1 Raccogli Informazioni

1. **Leggi** l'errore/bug descritto
2. **Cerca** nel codebase i file correlati
3. **Analizza** i log se disponibili
4. **Riproduci** mentalmente il flusso che causa il bug

### 1.2 Root Cause Analysis

Usa il ragionamento esteso per:
- Identificare la **causa root** del problema
- Distinguere tra **sintomo** e **causa**
- Valutare se ci sono **problemi correlati**

### 1.3 Genera Piano di Fix

```markdown
## 🐛 Bug Fix Plan

### Problema Riscontrato
[Descrizione del bug]

### Root Cause
[Causa identificata con spiegazione]

### File Coinvolti
| File | Linea | Problema |
|------|-------|----------|
| `path/file.py` | ~45 | [descrizione] |

### Soluzione Proposta
[Descrizione della fix]

### Task
1. **Fix principale** → django-developer
   - [cosa modificare]
   
2. **Test regressione** → test-writer
   - [test da aggiungere per prevenire recidiva]

### Rischio Regressione
🟢 Basso / 🟡 Medio / 🔴 Alto
[Spiegazione]
```

### 1.4 FERMATI E ASPETTA

**⏸️ Conferma il piano prima di procedere.**

---

## FASE 2: Implementazione Fix

Solo dopo approvazione:

1. **Delega** il fix al subagent appropriato
2. **Verifica** che la fix sia corretta
3. **Delega** la scrittura del test di regressione

---

## FASE 3: Verifica

1. **Esegui** tutti i test
2. **Verifica** che il bug sia risolto
3. **Controlla** che non ci siano regressioni

---

## FASE 4: Report

```markdown
## ✅ Bug Risolto

### Causa
[Root cause]

### Fix Applicata
- File: `path/file.py`
- Modifica: [descrizione]

### Test Aggiunto
- `test_<nome>` - Previene recidiva del bug

### Verifica
- Test suite: ✅ Passa
- Bug riprodotto: ❌ Non più riproducibile
```
