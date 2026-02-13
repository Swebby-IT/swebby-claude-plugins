---
description: "Fase di sviluppo orchestrata: Opus delega a Developer Sonnet/Opus. Zero codice diretto."
argument-hint: "<cosa sviluppare>"
---

# /develop — Lancia una fase di sviluppo

Devi orchestrare una fase di sviluppo. NON scrivere codice tu stesso.

## Task di sviluppo

$ARGUMENTS

## Istruzioni

1. **NON scrivere codice, modificare file o eseguire comandi** — delega ai Developer
2. Analizza il lavoro di sviluppo richiesto
3. Scomponi in task di codifica atomici e indipendenti
4. Per ogni task decidi il modello:
   - **Sonnet**: CRUD, fix semplici, feature standard, refactoring minore
   - **Opus**: architettura, algoritmi complessi, sicurezza, migrazioni delicate, logica di business critica
5. Lancia Developer con brief strutturati:
   - **Missione**: cosa implementare (una frase)
   - **Contesto**: decisioni architetturali già prese, vincoli
   - **Input**: file da modificare, path, specifiche
   - **Output atteso**: file creati/modificati, test
   - **Vincoli**: pattern da seguire, cose da NON fare
   - **Formato risposta**: RISULTATO → PROBLEMI → SUGGERIMENTI
6. Valida gli output e coordina eventuali dipendenze tra developer

## Scaling
- 1 file/componente → 1 Developer
- 2-3 componenti indipendenti → 2 Developer in parallelo
- Sistema complesso → fino a 4 Developer (Sonnet + Opus mix)

## Escalation
Se un Developer Sonnet fallisce 2 volte → promuovi a Opus e rilancia.

Procedi.
