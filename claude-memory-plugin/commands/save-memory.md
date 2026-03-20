---
description: "Salva un riassunto della sessione corrente nella memoria persistente"
argument-hint: ""
---

# /save-memory — Salva Riassunto Sessione

Devi creare un riassunto della sessione corrente e salvarlo in `.memory/sessions/`.

## Cosa fare

1. **Analizza cosa è stato fatto** in questa sessione:
   - Quali file sono stati modificati? (guarda il checkpoint se esiste: `.memory/checkpoints/.session.json`)
   - Quali task sono stati completati?
   - Quali decisioni sono state prese?
   - Quali problemi sono stati risolti?

2. **Scrivi un riassunto conciso** in `.memory/sessions/YYYY-MM-DD_HHMM.md` con questo formato:

```markdown
# Sessione YYYY-MM-DD HH:MM

## Cosa è stato fatto
- [1-5 bullet points che descrivono il lavoro svolto in linguaggio umano]

## File principali modificati
- [lista dei file più importanti, non tutti — solo quelli significativi]

## Decisioni prese
- [se ce ne sono state, altrimenti ometti la sezione]

## Problemi risolti
- [se ce ne sono stati, altrimenti ometti la sezione]

## Note per la prossima sessione
- [se c'è qualcosa di incompleto o da continuare]
```

3. **Aggiorna `.memory/CONTEXT.md`**:
   - Aggiorna "Work in Progress" con lo stato attuale
   - Aggiorna "Current State" se ci sono stati cambiamenti significativi

4. **Se ci sono decisioni architetturali**, appendile a `.memory/DECISIONS.md`

5. **Se ci sono learnings/errori**, appendili a `.memory/LEARNINGS.md`

## Regole

- **MAX 30 righe** per il riassunto — deve essere conciso
- **Linguaggio umano**, non tecnico — "Migrata dashboard progetti a SWCSS" non "Modificato progetti/templates/dashboard.html"
- **No diff, no git log** — solo il riassunto semantico
- **No file in .memory/sessions/ più vecchi di 60 giorni** — se ne trovi, ignorali
