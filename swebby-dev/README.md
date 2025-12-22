# SwebbyDev Plugin

Plugin multi-modalita per sviluppo software con nove modalita specializzate.

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

### `/swebby-dev:supermode` - Massima Potenza

**SUPERMODE = SENSEI ma con TUTTI gli agenti in Opus + ultrathink.**

```
┌──────────────────────────────────────────────────────────┐
│                   SUPERMODE = SENSEI + OPUS              │
│  Sensei: Tu Opus, agenti Sonnet                          │
│  Supermode: Tu Opus, agenti OPUS con ultrathink          │
└──────────────────────────────────────────────────────────┘
```

**Cosa fa:**
- Come Sensei, ma lancia TUTTI gli agenti con `model: "opus"`
- Ogni agente usa ragionamento ultra-approfondito
- Qualita massima, velocita secondaria
- Per i task piu critici e complessi

**Quando usarla:**
- Task mission-critical
- Quando la qualita e piu importante della velocita
- Problemi complessi che richiedono ragionamento profondo
- Quando vuoi la massima potenza disponibile

**Esempio:**
```bash
/swebby-dev:supermode Refactoring completo del sistema di autenticazione
```

---

### `/swebby-dev:ultramode` - Verifica Massiva Multi-Livello

**ULTRAMODE = SUPERMODE + MEGA-VERIFICA con loop correttivo.**

```
┌──────────────────────────────────────────────────────────────────────┐
│                    ULTRAMODE = SUPERMODE + MEGA-VERIFICA            │
│  Supermode: Tu Opus, agenti Opus eseguono                           │
│  Ultramode: + 5 verificatori paralleli + loop correttivo (max 3)    │
└──────────────────────────────────────────────────────────────────────┘
```

**Workflow 6 Fasi:**
1. **ARCHITECT**: Analisi e piano dettagliato
2. **EXECUTION SWARM**: N developer in parallelo (tutti Opus)
3. **VERIFICATION SWARM**: 5 verificatori in parallelo (tutti Opus)
4. **AGGREGATION**: Raccolta e prioritizzazione problemi
5. **CORRECTION LOOP**: Fix iterativi (max 3 cicli)
6. **FINAL VALIDATION**: Cross-validator per verdict finale

**Verificatori:**
- Inspector (sintassi, import, runtime)
- Consistency Checker (naming, interfacce, tipi)
- Completeness Checker (nulla saltato dal piano)
- Tester (test automatici)
- Reviewer (code review)
- Cross-Validator (aggregazione finale e verdict)

**Quando usarla:**
- Quando serve verifica massiva e accuratezza totale
- Per task dove NON possono esserci errori
- Quando vuoi piu agenti che verificano incrociando i risultati
- Per garantire coerenza e completezza

**Esempio:**
```bash
/swebby-dev:ultramode Implementa sistema di pagamenti con validazione completa
```

---

### `/swebby-dev:ultra-coherence` - Coerenza Totale con Loop Infinito

**ULTRA-COHERENCE = COERENZA TOTALE + LOOP INFINITO finche' PERFETTO.**

```
┌──────────────────────────────────────────────────────────────────────────┐
│                    ULTRA-COHERENCE = COERENZA TOTALE                      │
│                                                                           │
│  - MCP ricerca semantica PRIORITARIA (code-search)                        │
│  - 1-6 Researcher Opus: output ATOMICO e DETTAGLIATO                      │
│  - Tu (Opus) elabori in ultrathink                                        │
│  - 1-6 Developer Opus con ultrathink                                      │
│  - 1-6 Coherence Verifier: coerenza con TUTTO il sistema                  │
│  - Loop INFINITO: itera finche' PERFETTO (0 problemi critici/alti)        │
└──────────────────────────────────────────────────────────────────────────┘
```

**Workflow Loop Infinito:**
1. **RICERCA**: MCP semantico (priorita) + 1-6 researcher Opus -> output ATOM
2. **ELABORAZIONE**: Tu Opus elabori ATOM in ultrathink -> piano preciso
3. **EXECUTION**: 1-6 developer Opus con istruzioni atomiche
4. **VERIFICA**: 1-6 coherence-verifier Opus -> coerenza con TUTTO il sistema
5. **DECISIONE**: Perfetto? -> Riepilogo | Problemi? -> Torna a 1

**Differenza da Ultramode:**
- Ultramode: 5 verificatori diversi + loop max 3
- Ultra-Coherence: 1-6 verificatori COERENZA + loop INFINITO

**Agenti:**
- `researcher`: Ricerca con output ATOM (atomico e dettagliato)
- `developer`: Esegue modifiche
- `coherence-verifier`: Verifica coerenza con TUTTO il sistema

**Quando usarla:**
- Quando la COERENZA con tutto il sistema e critica
- Per modifiche che devono integrarsi perfettamente
- Quando vuoi garanzia che tutto funzioni insieme
- Task dove incoerenze causerebbero problemi gravi

**Esempio:**
```bash
/swebby-dev:ultra-coherence Aggiungi nuovo modulo che si integra con tutto il sistema esistente
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

## Agenti

Il plugin include 9 agenti usati dalle modalita Sensei, Supermode, Ultramode e Ultra-Coherence:

| Agente | Ruolo | Usato da |
|--------|-------|----------|
| `swebby-dev:developer` | Esegue modifiche al codice | Sensei, Supermode, Ultramode, Ultra-Coherence |
| `swebby-dev:tester` | Scrive ed esegue test | Sensei, Supermode, Ultramode |
| `swebby-dev:reviewer` | Code review | Sensei, Supermode, Ultramode |
| `swebby-dev:inspector` | Verifica funzionamento (sintassi, import, runtime) | Ultramode |
| `swebby-dev:consistency-checker` | Verifica coerenza (naming, interfacce, tipi) | Ultramode |
| `swebby-dev:completeness-checker` | Verifica completezza (nulla saltato) | Ultramode |
| `swebby-dev:cross-validator` | Aggregazione finale e verdict | Ultramode |
| `swebby-dev:researcher` | Ricerca atomica con MCP semantico prioritario | Ultra-Coherence |
| `swebby-dev:coherence-verifier` | Verifica coerenza con TUTTO il sistema | Ultra-Coherence |

Questi agenti NON prendono decisioni - eseguono istruzioni precise dall'orchestratore.

## Struttura Plugin

```
swebby-dev/
├── .claude-plugin/
│   └── plugin.json
├── commands/
│   ├── sensei.md             # Orchestrazione multi-agente (Opus + Sonnet)
│   ├── supermode.md          # Sensei con agenti Opus
│   ├── ultramode.md          # Verifica massiva multi-livello
│   ├── ultra-coherence.md    # Coerenza totale + loop infinito
│   ├── architect.md
│   ├── code.md
│   ├── ask.md
│   ├── orchestrator.md
│   └── debug.md
├── agents/
│   ├── developer.md            # Esegue modifiche codice
│   ├── tester.md               # Scrive/esegue test
│   ├── reviewer.md             # Code review
│   ├── inspector.md            # Verifica funzionamento
│   ├── consistency-checker.md  # Verifica coerenza file
│   ├── completeness-checker.md # Verifica completezza
│   ├── cross-validator.md      # Aggregazione e verdict
│   ├── researcher.md           # Ricerca atomica (Ultra-Coherence)
│   └── coherence-verifier.md   # Coerenza sistema (Ultra-Coherence)
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
# Orchestrazione multi-agente (Opus + Sonnet)
/swebby-dev:sensei Implementa sistema di notifiche push

# Massima potenza (Opus + Opus con ultrathink)
/swebby-dev:supermode Refactoring critico del sistema di pagamenti

# Verifica massiva multi-livello (6 fasi + loop correttivo)
/swebby-dev:ultramode Implementa sistema di pagamenti con validazione completa

# Coerenza totale con loop infinito
/swebby-dev:ultra-coherence Aggiungi modulo che deve integrarsi perfettamente col sistema

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

## Differenza tra le Modalita Multi-Agente

| Aspetto | Orchestrator | Sensei | Supermode | Ultramode | Ultra-Coherence |
|---------|--------------|--------|-----------|-----------|-----------------|
| Delega a | Modalita | Agenti Sonnet | Agenti Opus | Agenti Opus | Agenti Opus |
| Autonomia agenti | Decidono | Eseguono | Eseguono | Eseguono | Eseguono |
| MCP semantico | No | Opzionale | Opzionale | Opzionale | PRIORITARIO |
| Ricercatori | No | No | No | No | 1-6 (ATOM) |
| Verificatori | 0 | 2 | 2 | 6 | 1-6 (coerenza) |
| Loop correttivo | No | No | No | max 3 | INFINITO |
| Focus | Velocita | Qualita | Potenza | Verifica | COERENZA |
| Termina quando | Task fatto | Task fatto | Task fatto | max 3 iter | PERFETTO |
| Uso ideale | Semplici | Complessi | Critici | Verifica totale | Integrazione sistema |

## Versione

0.7.1
