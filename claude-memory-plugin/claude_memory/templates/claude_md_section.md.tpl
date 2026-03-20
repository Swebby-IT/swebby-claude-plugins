<!-- claude-memory:start -->
## Memory System (OBBLIGATORIO)

Questo progetto usa memoria persistente in `.memory/`. **Le regole sotto sono OBBLIGATORIE, non opzionali.**

### PRIMA di iniziare qualsiasi task
1. Leggi `.memory/CONTEXT.md` — contiene lo stato del progetto e cosa stanno facendo gli altri
2. Leggi `.memory/LEARNINGS.md` — contiene errori già noti da non ripetere
3. **Scrivi** in `.memory/CONTEXT.md` nella sezione "Work in Progress" cosa stai per fare (es. "Migrazione dashboard progetti a SWCSS")

### DURANTE il lavoro
- **Decisione architetturale?** → APPENDI a `.memory/DECISIONS.md`:
  `## YYYY-MM-DD: Titolo` + Contesto/Decisione/Motivo/File
- **Errore scoperto o pattern?** → APPENDI a `.memory/LEARNINGS.md`:
  `### Titolo (scoperto: YYYY-MM-DD)` + Errore/Correzione/Regola
- **Obiettivo completato?** → AGGIORNA `.memory/CONTEXT.md` sezioni "Current State" e "Work in Progress"

### REGOLE
- Solo append su DECISIONS.md e LEARNINGS.md — MAI sovrascrivere
- Non toccare `.memory/sessions/` — auto-generati dagli hook
- Il CONTEXT.md è condiviso tra sessioni — scrivi cosa fai così gli altri Claude lo vedono
<!-- claude-memory:end -->
