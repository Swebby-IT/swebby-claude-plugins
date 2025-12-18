---
description: Esegui review di un piano esistente o delle modifiche recenti
argument-hint: "<path piano> oppure 'recent' per ultimo piano"
---

# Comando: /architect:review

Stai per eseguire una review di: **$ARGUMENTS**

---

## FASE 1: Identificazione Target

### 1.1 Determina Cosa Revisionare

**Se $ARGUMENTS = "recent" o vuoto:**
```
1. Cerca l'ultimo piano in .architect/plans/
2. Ordina per data modifica (piu' recente prima)
3. Seleziona il primo file
```

**Se $ARGUMENTS = path specifico:**
```
1. Verifica che il file esista
2. Leggi il contenuto
```

**Se $ARGUMENTS = descrizione:**
```
1. Cerca in .architect/plans/ file che matchano
2. Mostra lista e chiedi conferma
```

### 1.2 Verifica File

```bash
# Verifica esistenza
ls -la .architect/plans/

# Se vuoto o non esiste
echo "Nessun piano trovato in .architect/plans/"
echo "Usa /architect:plan per creare un piano prima"
```

---

## FASE 2: Analisi Contesto

### 2.1 Leggi Piano

```
1. Read del file piano identificato
2. Estrai:
   - Titolo/Obiettivo
   - Task previsti
   - File coinvolti
   - Dipendenze
```

### 2.2 Analisi Codebase (se necessario)

Se il piano fa riferimento a file esistenti:

```
Task tool con subagent_type: architect:codebase-analyzer

Prompt:
"Analizza i file menzionati nel piano per verificare:
1. I file esistono?
2. Le linee indicate sono corrette?
3. Il codice esistente e' compatibile con le modifiche proposte?
4. Ci sono dipendenze non considerate?

File da verificare:
[lista file dal piano]

Output: Report di verifica con discrepanze trovate."
```

---

## FASE 3: Review

### 3.1 Lancia Plan Reviewer

```
Task tool con subagent_type: architect:plan-reviewer

Prompt:
"Esegui una review approfondita del seguente piano:

---
[contenuto piano]
---

Contesto codebase (se disponibile):
[output codebase-analyzer]

Valuta secondo questi criteri:

1. **Completezza (25%)**
   - Tutti i requisiti sono coperti?
   - Mancano task?
   - Edge cases considerati?

2. **Chiarezza (20%)**
   - Il piano e' facile da seguire?
   - Le istruzioni sono specifiche?
   - I task sono ben definiti?

3. **Fattibilita' (20%)**
   - Le modifiche sono realistiche?
   - Le dipendenze sono corrette?
   - I file/linee esistono?

4. **Rischi (15%)**
   - Rischi identificati adeguatamente?
   - Mitigazioni proposte?
   - Casi limite gestiti?

5. **Test (10%)**
   - Piano di test adeguato?
   - Copertura sufficiente?
   - Test automatizzabili?

6. **Best Practices (10%)**
   - Segue convenzioni del progetto?
   - Pattern appropriati?
   - Security considerata?

Output:
- Score per ogni criterio
- Score complessivo
- Problemi trovati (per severita')
- Suggerimenti miglioramento
- Verdetto (APPROVED / NEEDS REVISION / REJECTED)"
```

---

## FASE 4: Presentazione Risultati

### 4.1 Mostra Review

```markdown
## Review: [Titolo Piano]

**File revisionato:** [path]
**Data review:** [YYYY-MM-DD HH:MM]
**Reviewer:** Plan Reviewer Agent (Opus)

---

### Score Complessivo: [X.X]/10 [EMOJI]

| Criterio | Score | Commento |
|----------|-------|----------|
| Completezza | X/10 | [breve] |
| Chiarezza | X/10 | [breve] |
| Fattibilita' | X/10 | [breve] |
| Rischi | X/10 | [breve] |
| Test | X/10 | [breve] |
| Best Practices | X/10 | [breve] |

---

### Verdetto: [APPROVED / APPROVED WITH CHANGES / NEEDS REVISION / REJECTED]

[Spiegazione verdetto in 2-3 frasi]

---

### Punti di Forza

1. [punto forte 1]
2. [punto forte 2]
3. [punto forte 3]

---

### Problemi Trovati

#### Critici (da risolvere prima di procedere)

[Se presenti]

#### Alti (fortemente raccomandato risolvere)

[Se presenti]

#### Medi (consigliato risolvere)

[Se presenti]

#### Bassi (miglioramenti opzionali)

[Se presenti]

---

### Suggerimenti

1. [suggerimento 1]
2. [suggerimento 2]
3. [suggerimento 3]

---

### Prossimi Passi

**Se APPROVED:**
- Procedi con l'implementazione
- Usa il piano come guida

**Se APPROVED WITH CHANGES:**
- Risolvi i problemi Alti indicati
- Poi procedi con l'implementazione

**Se NEEDS REVISION:**
- Rivedi il piano incorporando i feedback
- Esegui nuovamente /architect:review

**Se REJECTED:**
- Il piano richiede rework significativo
- Considera /architect:plan per ricominciare
```

---

## FASE 5: Salvataggio (Opzionale)

### 5.1 Chiedi se Salvare

```
Vuoi salvare questa review in .architect/reviews/?

[Si/No]
```

### 5.2 Se Si

```
Salva come: .architect/reviews/review_[nome_piano]_YYYYMMDD_HHMMSS.md
```

---

## REGOLE IMPORTANTI

1. **Verifica sempre il codebase** - Non fidarti solo del piano
2. **Sii specifico** - Problemi vaghi non sono utili
3. **Prioritizza** - Critico > Alto > Medio > Basso
4. **Suggerisci soluzioni** - Non solo problemi
5. **Sii costruttivo** - L'obiettivo e' migliorare, non criticare

---

## GESTIONE CASI SPECIALI

### Nessun piano trovato

```
Non ho trovato piani in .architect/plans/

Opzioni:
1. Crea un piano con /architect:plan <requisiti>
2. Specifica un path diverso: /architect:review /path/to/plan.md
3. Incolla il piano direttamente e chiedi review
```

### Piano incompleto

```
Il piano sembra incompleto (mancano sezioni critiche).

Sezioni mancanti:
- [sezione 1]
- [sezione 2]

Vuoi procedere comunque con una review parziale?
[Si/No]
```

### File riferiti non esistono

```
Attenzione: alcuni file nel piano non esistono nella codebase:

- path/file1.py (non trovato)
- path/file2.py (non trovato)

Questo potrebbe indicare:
1. Il piano e' per un nuovo progetto
2. I path sono errati
3. I file devono essere ancora creati

Procedo con la review considerando questi come nuovi file.
```

---

## ESEMPIO OUTPUT

```markdown
## Review: Piano Sistema Notifiche

**File revisionato:** .architect/plans/plan_20240115_143022.md
**Data review:** 2024-01-15 15:30
**Reviewer:** Plan Reviewer Agent (Opus)

---

### Score Complessivo: 7.8/10

| Criterio | Score | Commento |
|----------|-------|----------|
| Completezza | 8/10 | Copre i casi principali |
| Chiarezza | 9/10 | Ben strutturato |
| Fattibilita' | 7/10 | Alcune dipendenze da verificare |
| Rischi | 6/10 | Mancano alcuni rischi |
| Test | 8/10 | Buon piano di test |
| Best Practices | 8/10 | Segue pattern esistenti |

---

### Verdetto: APPROVED WITH CHANGES

Piano solido con buona struttura. Alcuni rischi di integrazione non considerati che potrebbero causare problemi in produzione.

---

### Problemi Trovati

#### Alti

1. **Mancata gestione rate limiting SMTP**
   - Dove: Task #4 (invio email)
   - Impatto: Blocco account SMTP in caso di burst
   - Suggerimento: Aggiungere queue con throttling

#### Medi

1. **Template email non versionati**
   - Dove: Task #2
   - Suggerimento: Usare template versionati in DB

---

### Prossimi Passi

Risolvi il problema di rate limiting SMTP, poi procedi con l'implementazione.
```
