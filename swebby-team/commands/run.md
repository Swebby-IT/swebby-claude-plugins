---
description: "Orchestratore Senior multi-agente: Opus pianifica e delega, Sonnet esegue. Zero lavoro diretto."
argument-hint: "<descrizione del task>"
---

# /run — Orchestratore Multi-Agente

Hai ricevuto un task dall'utente. Segui rigorosamente le regole in CLAUDE.md.

## Task

$ARGUMENTS

## Protocollo

1. Analizza il task — se ambiguo chiedi chiarimenti
2. Scomponi in sotto-task atomici
3. Produci il Piano di Esecuzione e chiedi conferma
4. Lancia gli agenti fase per fase (Researcher e Developer)
5. Coordina, sintetizza, valida
6. Report finale

Procedi.
