# SwebbyDev Plugin

Plugin multi-modalita per sviluppo software ispirato a KiloCode. Sei modalita specializzate per diversi aspetti dello sviluppo.

## Modalita Disponibili

### `/swebby-dev:sensei` - Orchestrazione Multi-Agente

**LA MODALITA PIU POTENTE.** Opus pianifica e orchestra, agenti Sonnet eseguono.

```
┌─────────────────────────────────────────────────────────┐
│                    SENSEI (Opus)                         │
│  Analizza -> Pianifica -> Prepara istruzioni dettagliate │
└─────────────────────────────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┐
          ▼               ▼               ▼
   ┌────────────┐  ┌────────────┐  ┌────────────┐
   │ Developer  │  │  Tester    │  │ Reviewer   │
   │  (Sonnet)  │  │  (Sonnet)  │  │  (Sonnet)  │
   │  Esegue    │  │  Testa     │  │  Revisiona │
   └────────────┘  └────────────┘  └────────────┘
```

**Cosa fa:**
- Opus analizza la codebase e crea piano dettagliato
- Chiede approvazione utente
- Per ogni step, prepara istruzioni ULTRA specifiche (file, righe, codice esatto)
- Delega ad agenti Sonnet che eseguono SENZA decidere
- Verifica risultati e coordina test/review

**Quando usarla:**
- Implementazioni complesse
- Quando vuoi che Opus pensi e Sonnet esegua
- Per massimizzare qualita e controllo
- Progetti che richiedono piu modifiche coordinate

**Esempio:**
```bash
/swebby-dev:sensei Aggiungi autenticazione JWT con refresh token
```

---

### `/swebby-dev:architect` - Pianificazione

Leader tecnico per pianificare e progettare soluzioni prima dell'implementazione.

**Cosa fa:**
- Raccoglie informazioni sul task
- Fa domande di chiarimento
- Crea piani dettagliati con TodoWrite
- Include diagrammi Mermaid quando utili
- Suggerisce la modalita successiva

**Quando usarla:**
- Pianificare nuove feature
- Progettare architetture
- Scomporre problemi complessi
- Creare specifiche tecniche

---

### `/swebby-dev:code` - Implementazione

Sviluppatore esperto per scrivere codice di qualita.

**Cosa fa:**
- Comprende il contesto del progetto
- Implementa seguendo le best practice
- Mantiene le convenzioni esistenti
- Evita over-engineering
- Traccia i progressi

**Quando usarla:**
- Scrivere nuovo codice
- Modificare codice esistente
- Refactoring
- Implementare feature
- Fixare bug

---

### `/swebby-dev:ask` - Domande

Assistente tecnico per spiegazioni e analisi.

**Cosa fa:**
- Risponde in modo approfondito
- Analizza codice
- Spiega concetti tecnici
- Usa diagrammi Mermaid
- NON implementa (a meno che richiesto)

**Quando usarla:**
- Capire concetti tecnici
- Analizzare codice esistente
- Ottenere raccomandazioni
- Apprendere nuove tecnologie

---

### `/swebby-dev:orchestrator` - Coordinamento

Coordinatore per gestire workflow complessi.

**Cosa fa:**
- Scompone task in subtask
- Delega alle modalita appropriate
- Traccia il progresso
- Sintetizza i risultati

**Quando usarla:**
- Progetti multi-step
- Task che richiedono piu specialita
- Workflow che attraversano piu domini
- Coordinamento di task complessi

---

### `/swebby-dev:debug` - Debugging

Esperto debugger per diagnosi sistematica.

**Cosa fa:**
- Genera 5-7 ipotesi sulle cause
- Distilla a 1-2 piu probabili
- Aggiunge log per validare
- Chiede conferma prima del fix
- Documenta la soluzione

**Quando usarla:**
- Investigare errori
- Diagnosticare problemi
- Analizzare stack trace
- Troubleshooting sistematico

---

## Agenti (usati da Sensei)

Il plugin include tre agenti Sonnet usati dalla modalita Sensei:

| Agente | Ruolo |
|--------|-------|
| `swebby-dev:developer` | Esegue modifiche al codice |
| `swebby-dev:tester` | Scrive ed esegue test |
| `swebby-dev:reviewer` | Code review |

Questi agenti NON prendono decisioni - eseguono istruzioni precise da Sensei.

## Struttura Plugin

```
swebby-dev/
├── .claude-plugin/
│   └── plugin.json      # Include definizione agenti
├── commands/
│   ├── sensei.md        # Orchestrazione multi-agente
│   ├── architect.md
│   ├── code.md
│   ├── ask.md
│   ├── orchestrator.md
│   └── debug.md
└── README.md
```

## Installazione

Il plugin e gia incluso nel marketplace swebby-plugins. Per usarlo:

```bash
# Dalla directory del progetto
claude --plugin swebby-dev
```

## Esempi di Utilizzo

```bash
# NUOVO: Orchestrazione multi-agente (Opus + Sonnet)
/swebby-dev:sensei Implementa sistema di notifiche push

# Pianificare una nuova feature
/swebby-dev:architect Voglio aggiungere autenticazione OAuth2

# Implementare codice
/swebby-dev:code Implementa il componente login form

# Fare una domanda
/swebby-dev:ask Come funziona il pattern Repository in questo progetto?

# Gestire un task complesso
/swebby-dev:orchestrator Migra il database da MySQL a PostgreSQL

# Debuggare un problema
/swebby-dev:debug L'API restituisce 500 quando faccio POST su /users
```

## Differenza tra Sensei e Orchestrator

| Orchestrator | Sensei |
|--------------|--------|
| Delega a modalita (stesso modello) | Delega ad agenti Sonnet |
| Agenti decidono autonomamente | Agenti eseguono ordini precisi |
| Istruzioni generiche | Istruzioni ultra-specifiche |
| Piu veloce per task semplici | Piu controllo per task complessi |

## Versione

0.4.0
