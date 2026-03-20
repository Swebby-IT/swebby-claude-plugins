<!-- claude-memory:start -->
## Memory System (OBBLIGATORIO)

Memoria persistente in `.memory/`. **DEVI usarla attivamente.**

### All'inizio della sessione
- **Leggi** `.memory/CONTEXT.md` per capire lo stato del progetto
- **Leggi** `.memory/LEARNINGS.md` per evitare errori già noti

### Durante il lavoro — DEVI scrivere quando:
- **Prendi una decisione architetturale** → appendi a `.memory/DECISIONS.md`:
  ```
  ## YYYY-MM-DD: Titolo
  - **Contesto**: perché serviva
  - **Decisione**: cosa si è deciso
  - **Motivo**: perché questa scelta
  - **File coinvolti**: lista file
  ```
- **Scopri un errore o pattern** → appendi a `.memory/LEARNINGS.md`:
  ```
  ### Titolo (scoperto: YYYY-MM-DD)
  - **Errore**: cosa è andato storto
  - **Correzione**: come risolto
  - **Regola**: regola per evitarlo
  ```
- **Completi un obiettivo** → aggiorna `.memory/CONTEXT.md` sezioni "Work in Progress" e "Current State"

### NON fare
- Non modificare `.memory/sessions/` (auto-generati)
- Non sovrascrivere DECISIONS.md o LEARNINGS.md — solo append
<!-- claude-memory:end -->
