<!-- claude-memory:start -->
## Memory System (OBBLIGATORIO)

Memoria persistente in `.memory/`. **Le regole sotto sono OBBLIGATORIE.**

### PRIMA di iniziare qualsiasi task
1. Leggi `.memory/CONTEXT.md` — stato progetto e cosa stanno facendo gli altri
2. Leggi `.memory/LEARNINGS.md` — errori già noti da non ripetere
3. **Scrivi** in `.memory/CONTEXT.md` sezione "Work in Progress" cosa stai per fare

### DURANTE il lavoro
- **Decisione architetturale?** → APPENDI a `.memory/DECISIONS.md`
- **Errore scoperto o pattern?** → APPENDI a `.memory/LEARNINGS.md`
- **Obiettivo completato?** → AGGIORNA `.memory/CONTEXT.md`

### SALVATAGGIO MEMORIA
La memoria si salva con `/save-memory` o automaticamente alla compattazione contesto.
Quando salvi, scrivi un **riassunto in linguaggio umano** (non diff tecnici) in `.memory/sessions/`.

### REGOLE
- Solo append su DECISIONS.md e LEARNINGS.md — MAI sovrascrivere
- Non toccare `.memory/sessions/` vecchi — sono log di sessioni passate
- Il CONTEXT.md è condiviso tra sessioni — scrivi cosa fai così gli altri Claude lo vedono
<!-- claude-memory:end -->
