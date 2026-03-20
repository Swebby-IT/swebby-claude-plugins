<!-- claude-memory:start -->
## Memory System (claude-memory)

Questo progetto ha un sistema di memoria persistente in `.memory/`.

### File di memoria
- `.memory/CONTEXT.md` — Stato corrente del progetto. Leggilo all'inizio di ogni sessione per capire dove siamo.
- `.memory/DECISIONS.md` — Log decisioni architetturali. Consultalo quando devi prendere una decisione per verificare coerenza con le precedenti.
- `.memory/LEARNINGS.md` — Errori passati e pattern consolidati. Consultalo per evitare errori noti.

### Regole
1. **Quando prendi una decisione architetturale significativa**, aggiungila a `.memory/DECISIONS.md` con formato:
   ```
   ## YYYY-MM-DD: [Titolo decisione]
   - **Contesto**: perché è servita questa decisione
   - **Decisione**: cosa si è deciso
   - **Motivo**: perché questa scelta e non le alternative
   - **File coinvolti**: quali file sono stati impattati
   ```

2. **Quando scopri un errore o un pattern importante**, aggiungilo a `.memory/LEARNINGS.md` con formato:
   ```
   ### [Titolo] (scoperto: YYYY-MM-DD)
   - **Errore**: cosa è andato storto
   - **Correzione**: come è stato risolto
   - **Regola**: regola da seguire per evitarlo in futuro
   ```

3. **Quando completi un obiettivo significativo**, aggiorna la sezione "Current State" e "Work in Progress" di `.memory/CONTEXT.md`.

4. **Per cercare contesto storico**, usa il tool MCP Qdrant con la collection `{collection_name}` per trovare decisioni passate, sessioni precedenti, o codice correlato.

5. **Non modificare** i file in `.memory/sessions/` — sono log generati automaticamente.
<!-- claude-memory:end -->
