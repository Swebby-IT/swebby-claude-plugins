---
description: Crea solo il piano dettagliato per una modifica, senza eseguirla
argument-hint: "<descrizione della modifica da pianificare>"
---

# Comando: Pianifica Modifica

Stai pianificando: **$ARGUMENTS**

## Istruzioni

Usa il ragionamento esteso per creare un piano dettagliato SENZA eseguire modifiche.

### Step 1: Ricerca nel Codebase

1. Cerca file e pattern correlati alla richiesta
2. Identifica le dipendenze
3. Analizza il codice esistente

### Step 2: Analisi Impatto

Valuta:
- Quali file saranno modificati?
- Quali altri moduli potrebbero essere impattati?
- Ci sono migrazioni database necessarie?
- Servono modifiche al frontend?

### Step 3: Genera il Piano

Produci un piano nel formato:

```markdown
## 📋 Piano: $ARGUMENTS

### 🎯 Obiettivo
[Cosa verrà realizzato]

### 🔍 Analisi Codebase
[Cosa hai trovato di rilevante]

### 📁 File da Modificare
| File | Tipo | Descrizione Modifica |
|------|------|---------------------|
| `path/file.py` | Backend | [descrizione] |

### 📦 Task Breakdown

**Task 1:** [Titolo]
- Agente: django-developer / frontend-developer / test-writer
- Complessità: 🟢/🟡/🔴
- Dipendenze: Nessuna / Task X
- Descrizione dettagliata:
  [cosa deve fare esattamente]

**Task 2:** [Titolo]
...

### 🔗 Dipendenze tra Task
```
Task 1 ─┬─► Task 3 ─► Task 5
        │
Task 2 ─┘
        
Task 4 (parallelo)
```

### ⚠️ Rischi
| Rischio | Impatto | Mitigazione |
|---------|---------|-------------|
| [rischio] | Alto/Medio/Basso | [come gestire] |

### 📝 Note Tecniche
[Considerazioni importanti per l'implementazione]

### ⏱️ Stima Effort
- Backend: ~X ore
- Frontend: ~X ore
- Test: ~X ore
- **Totale:** ~X ore
```

### Step 4: Domande (se necessario)

Se hai bisogno di chiarimenti, chiedi PRIMA di finalizzare il piano.

---

## Output

Il piano verrà presentato all'utente che potrà:
1. **Approvarlo** → Eseguire `/implement` con lo stesso argomento
2. **Modificarlo** → Richiedere cambiamenti al piano
3. **Rifiutarlo** → Chiedere un approccio diverso

**NON eseguire nessuna modifica al codice con questo comando.**
