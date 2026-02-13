# 🎯 Swebby Team

Orchestratore multi-agente per Claude Code. Opus 4.6 come team leader che orchestra Researcher (Sonnet) e Developer (Sonnet/Opus) senza mai fare lavoro diretto.

```
┌─────────────────────────────────────┐
│     ORCHESTRATORE (Opus 4.6)        │
│   Pianifica · Delega · Coordina     │
│       ⛔ Zero lavoro diretto        │
└──────────┬──────────┬───────────────┘
           │          │
    ┌──────▼──┐  ┌────▼─────┐
    │RESEARCHER│  │DEVELOPER │
    │ (Sonnet) │  │(Sonnet/  │
    │          │  │  Opus)   │
    │• Analisi │  │• Codice  │
    │• Ricerca │  │• Fix     │
    │• Review  │  │• Feature │
    │• Test    │  │• Arch.   │
    └──────────┘  └──────────┘
```

## Installazione

Aggiungi Swebby Team al tuo progetto come custom instructions da GitHub:

```bash
claude install github:YOUR_USERNAME/swebby-team
```

Oppure aggiungilo manualmente nei settings di Claude Code:

```bash
claude config add customInstructions "$(curl -s https://raw.githubusercontent.com/YOUR_USERNAME/swebby-team/main/CLAUDE.md)"
```

## Comandi

| Comando | Uso | Esempio |
|---------|-----|---------|
| `/orchestrate` | Task completo multi-fase | `/orchestrate Aggiungi autenticazione OAuth2` |
| `/research` | Solo ricerca/analisi | `/research Analizza le API di pagamento` |
| `/develop` | Solo sviluppo codice | `/develop Implementa UserProfile component` |
| `/review` | Verifica e code review | `/review Controlla le modifiche all'auth` |
| `/plan` | Piano senza eseguire (dry-run) | `/plan Migrazione da REST a GraphQL` |

## Come Funziona

1. **Tu dai un task** → L'orchestratore analizza e scompone
2. **Piano di esecuzione** → Mostra fasi, agenti, modelli, dipendenze
3. **Conferma** → Chiede ok prima di lanciare
4. **Dispatch** → Lancia agenti con brief atomici strutturati
5. **Coordinamento** → Sintetizza output, passa info tra fasi
6. **Verifica** → Review automatica del risultato
7. **Report** → Riassunto finale

## Regole Chiave

- **Zero lavoro diretto**: l'orchestratore NON tocca mai file, codice, terminale
- **Scaling automatico**: da 2 a 8 agenti in base alla complessità
- **Modello adattivo**: Sonnet per default, Opus per task critici
- **Escalation**: se Sonnet fallisce 2x → promuove a Opus
- **Comunicazione atomica**: brief strutturati in entrata, output con formato fisso in uscita

## Scaling Agenti

| Complessità | Researcher | Developer | Totale |
|------------|------------|-----------|--------|
| Semplice | 1 | 1 | 2 |
| Media | 2 | 2 | 4 |
| Complessa | 3 | 4 | 7 |
| Max | - | - | 8 |

## Requisiti

- Claude Code
- Accesso ai modelli Opus 4.6 e Sonnet
- Piano Team o Enterprise (per multi-agent)

## Licenza

MIT
