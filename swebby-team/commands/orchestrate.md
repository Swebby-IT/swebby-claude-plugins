---
description: "Orchestrazione completa multi-agente: analisi, sviluppo, review. Opus coordina, Sonnet esegue."
argument-hint: "<descrizione del task>"
---

# /orchestrate — Avvia l'orchestratore

Hai ricevuto un task dall'utente. Attiva il protocollo di orchestrazione completo.

## Istruzioni

1. **NON fare nulla direttamente** — segui rigorosamente le regole in CLAUDE.md
2. Analizza il task fornito dall'utente: $ARGUMENTS
3. Produci il **Piano di Esecuzione** completo con fasi, agenti, modelli e dipendenze
4. Chiedi conferma all'utente prima di procedere con il dispatch
5. Lancia gli agenti fase per fase
6. Coordina, sintetizza, valida
7. Produci il report finale

## Checklist pre-lancio
- [ ] Il task è chiaro? (se no → chiedi chiarimenti)
- [ ] Hai scomposto in sotto-task atomici?
- [ ] Hai classificato complessità e tipo per ogni sotto-task?
- [ ] Hai assegnato il modello giusto a ogni agente?
- [ ] Hai identificato cosa può andare in parallelo?
- [ ] Hai scritto brief completi per ogni agente?

Procedi.
