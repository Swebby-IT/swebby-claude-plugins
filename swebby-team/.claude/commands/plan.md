---
description: "Genera Piano di Esecuzione senza lanciare agenti. Dry-run per validare l'approccio."
argument-hint: "<task da pianificare>"
---

# /plan — Genera solo il Piano di Esecuzione

Analizza il task e produci SOLO il piano di esecuzione, senza lanciare nessun agente. Utile per validare l'approccio con l'utente prima di procedere.

## Task da pianificare

$ARGUMENTS

## Istruzioni

1. Analizza il task
2. Scomponi in sotto-task atomici
3. Classifica ogni sotto-task (tipo, complessità, dipendenze)
4. Produci il piano completo:

```
📋 PIANO DI ESECUZIONE (DRAFT)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Obiettivo: [one-liner]
Complessità globale: [LOW|MEDIUM|HIGH|CRITICAL]
Agenti stimati: N (R: X researcher, D: Y developer)
Tempo stimato: [stima grezza]

FASE A — [nome] (parallela/sequenziale)
  ├─ 🔍 R1 (Sonnet): [task]
  └─ Output atteso: [deliverable]

FASE B — [nome] (dipende da: Fase A)
  ├─ 🛠️ D1 (Sonnet/Opus): [task]
  └─ Output atteso: [deliverable]

[... altre fasi ...]

RISCHI IDENTIFICATI:
- [rischio 1]
- [rischio 2]

DOMANDE APERTE:
- [domanda per l'utente, se ce ne sono]
```

5. Chiedi conferma o modifiche all'utente
6. **NON lanciare agenti** — aspetta l'ok esplicito

Procedi con la pianificazione.
