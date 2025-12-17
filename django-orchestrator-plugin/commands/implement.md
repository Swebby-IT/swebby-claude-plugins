---
description: Implementa una feature con workflow orchestrato (pianifica → approva → esegui → testa → review)
argument-hint: "<descrizione della modifica da implementare>"
---

# Comando: Implementa Feature

Stai per implementare: **$ARGUMENTS**

## FASE 1: Pianificazione (OBBLIGATORIA)

Prima di qualsiasi modifica, devi:

### 1.1 Analisi Approfondita

Usa il ragionamento esteso (`ultrathink`) per:

1. **Comprendere** la richiesta in profondità
2. **Cercare** nel codebase pattern simili e file correlati
3. **Identificare** tutte le dipendenze e impatti
4. **Valutare** rischi e complessità

### 1.2 Crea il Piano

Genera un piano strutturato in questo formato:

```markdown
## 📋 Piano di Implementazione

### 🎯 Obiettivo
[Descrizione chiara di cosa verrà realizzato]

### 📁 File Coinvolti
| File | Azione | Descrizione |
|------|--------|-------------|
| `path/file.py` | Modifica | [cosa cambia] |
| `path/new.py` | Crea | [cosa contiene] |

### 📦 Task da Delegare

#### Task 1: [Titolo]
- **Agente:** django-developer
- **Descrizione:** [cosa deve fare]
- **File:** [lista file]
- **Dipendenze:** [altri task che devono completare prima]

#### Task 2: [Titolo]
- **Agente:** frontend-developer
- **Descrizione:** [cosa deve fare]
- **File:** [lista file]

#### Task 3: [Titolo]
- **Agente:** test-writer
- **Descrizione:** [test da scrivere]

### ⚠️ Rischi e Mitigazioni
| Rischio | Probabilità | Mitigazione |
|---------|-------------|-------------|
| [rischio] | Alta/Media/Bassa | [come gestirlo] |

### ⏱️ Stima
- Complessità: 🟢 Bassa / 🟡 Media / 🔴 Alta
- Task paralleli: X
- Task sequenziali: Y
```

### 1.3 FERMATI E ASPETTA

**⏸️ NON procedere oltre senza approvazione esplicita dell'utente.**

Chiedi: "Il piano ti sembra corretto? Posso procedere con l'implementazione?"

---

## FASE 2: Esecuzione (Solo dopo approvazione)

### 2.1 Delegazione ai Subagenti

Per ogni task nel piano approvato:

1. **Lancia** il subagent appropriato con istruzioni precise
2. **Fornisci** tutto il contesto necessario
3. **Attendi** il completamento
4. **Verifica** il risultato prima di procedere

Esempio di delegazione:
```
Delego a django-developer:

**Task:** Aggiungere campo sconto al modello Order
**File da modificare:** vendite/models.py
**Specifiche:**
- Campo: discount_percentage (DecimalField, max 2 decimali, default 0)
- Aggiungere property calculated_total che applica lo sconto
- Aggiornare __str__ per mostrare lo sconto se presente

**Contesto:**
[snippet del modello attuale]
```

### 2.2 Task Paralleli vs Sequenziali

- **Paralleli:** Task indipendenti possono essere lanciati insieme
- **Sequenziali:** Task con dipendenze devono aspettare

---

## FASE 3: Testing

Dopo l'implementazione:

1. **Delega** a `test-writer` la scrittura dei test
2. **Esegui** la test suite completa
3. **Verifica** che non ci siano regressioni

---

## FASE 4: Review

1. **Delega** a `code-reviewer` l'analisi del codice
2. **Applica** i fix per problemi critici/alti
3. **Valuta** i suggerimenti per problemi medi/bassi

---

## FASE 5: Completamento

Riporta il risultato finale:

```markdown
## ✅ Implementazione Completata

### Modifiche Apportate
- [lista file modificati con descrizione]

### Test
- Test scritti: X
- Test passati: X/X
- Coverage: XX%

### Review
- Problemi critici risolti: X
- Suggerimenti applicati: X

### Comandi Post-Deploy
```bash
python manage.py migrate
npm run build
```

### Note
[Eventuali osservazioni per l'utente]
```

---

## Regole Importanti

1. **MAI** saltare la fase di pianificazione
2. **MAI** procedere senza approvazione esplicita
3. **SEMPRE** usare i subagenti per l'esecuzione
4. **SEMPRE** verificare i risultati di ogni subagent
5. **SEMPRE** eseguire i test alla fine
