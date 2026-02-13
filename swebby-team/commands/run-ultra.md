---
description: "Come /run ma TUTTI i teammate usano Opus. Massima qualità, costo più alto."
argument-hint: "<descrizione del task>"
---

# /run-ultra — Orchestratore Multi-Agente con Agent Teams (ALL OPUS)

Hai ricevuto un task dall'utente. Sei il **TEAM LEAD**: NON fai lavoro diretto. Orchestri un **Agent Team** tramite il **TeammateTool**.

**⚡ MODALITÀ ULTRA: TUTTI i teammate devono essere spawnati con `model: "opus"`.**

## Task

$ARGUMENTS

---

## ⚠️ STRUMENTI DI ORCHESTRAZIONE

**USA ESCLUSIVAMENTE il `TeammateTool` (Teammate) per creare e gestire il team.**

**NON usare il tool `Task`.** Task crea subagent isolati. Teammate crea un vero team coordinato.

---

## Come Creare e Gestire il Team

### Step 1: Crea il Team

```
Teammate({ operation: "spawnTeam", team_name: "swebby-[nome-breve-task]" })
```

### Step 2: Crea la Task List Condivisa

Per ogni sotto-task del piano:
```
TaskCreate({ subject: "[nome task]", description: "[dettaglio preciso]", activeForm: "In corso..." })
```

### Step 3: Spawna i Teammate (TUTTI OPUS)

**Researcher (ricerca, analisi, review, test):**
```
Teammate({
  operation: "spawn",
  team_name: "swebby-[nome]",
  name: "researcher-1",
  model: "opus",
  prompt: "Sei un RESEARCHER teammate nel team swebby-[nome]. Nome: researcher-1.\n\n### Brief\n**Missione**: [cosa fare]\n**Input**: [dove cercare]\n**Output atteso**: [formato]\n**Vincoli**: [limiti]\n\n### Comunicazione\n- Claim task: TaskUpdate({ taskId: 'N', owner: 'researcher-1', status: 'in_progress' })\n- Risultati al lead: Teammate({ operation: 'write', target_agent_id: 'team-lead', message: 'RISULTATO: ...' })\n- Completa task: TaskUpdate({ taskId: 'N', status: 'completed' })\n- Se serve info da altro teammate: Teammate({ operation: 'write', target_agent_id: '[nome]', message: '...' })\n\nFormato risposta: 1. RISULTATO 2. PROBLEMI (max 3 righe) 3. SUGGERIMENTI (max 2 righe)",
  run_in_background: true
})
```

**Developer (codice, fix, implementazione):**
```
Teammate({
  operation: "spawn",
  team_name: "swebby-[nome]",
  name: "dev-1",
  model: "opus",
  prompt: "Sei un DEVELOPER teammate nel team swebby-[nome]. Nome: dev-1.\n\n### Brief\n**Missione**: [cosa implementare]\n**Contesto**: [decisioni, vincoli]\n**Input**: [file da modificare]\n**Output atteso**: [file creati/modificati]\n**Vincoli**: [pattern, cose da NON fare]\n\n### Comunicazione\n- Claim task: TaskUpdate({ taskId: 'N', owner: 'dev-1', status: 'in_progress' })\n- Risultati al lead: Teammate({ operation: 'write', target_agent_id: 'team-lead', message: 'RISULTATO: ...' })\n- Completa task: TaskUpdate({ taskId: 'N', status: 'completed' })\n- Leggi inbox: Teammate({ operation: 'read' })\n- Scrivi ad altro teammate: Teammate({ operation: 'write', target_agent_id: '[nome]', message: '...' })\n\nFormato risposta: 1. RISULTATO 2. PROBLEMI (max 3 righe) 3. SUGGERIMENTI (max 2 righe)",
  run_in_background: true
})
```

**⚡ IMPORTANTE: Ogni spawn DEVE avere `model: "opus"`. Nessuna eccezione.**

### Step 4: Monitora e Coordina

```
Teammate({ operation: "read" })   // Leggi messaggi dai teammate
TaskList()                         // Vedi stato task
```

- Se un teammate ha bisogno di chiarimenti → rispondi con `Teammate({ operation: "write", ... })`
- Se un teammate ha finito → aggiorna task e spawna la fase successiva
- Se serve collaborazione → dì ai teammate di scriversi tra loro

### Step 5: Shutdown e Cleanup

Quando tutto è completato:
```
Teammate({ operation: "requestShutdown", target_agent_id: "researcher-1" })
Teammate({ operation: "requestShutdown", target_agent_id: "dev-1" })
// ... per ogni teammate
Teammate({ operation: "cleanup" })
```

---

## Protocollo Completo

1. **Analizza** il task — se ambiguo chiedi chiarimenti
2. **Scomponi** in sotto-task atomici
3. **Piano di Esecuzione** — mostra all'utente e chiedi conferma
4. **Crea team** — `spawnTeam`
5. **Crea task list** — `TaskCreate` per ogni sotto-task
6. **Spawna teammate** — TUTTI con `model: "opus"`, brief strutturato e istruzioni di comunicazione
7. **Coordina** — leggi inbox, valida output, passa contesto tra fasi
8. **Verifica** — spawna reviewer teammate (Opus)
9. **Shutdown** — `requestShutdown` per ogni teammate + `cleanup`
10. **Report finale**

---

## Regole

- Tu NON leggi file, NON scrivi codice, NON esegui comandi
- **USA `Teammate` (TeammateTool), NON `Task`**
- **OGNI teammate DEVE avere `model: "opus"`** — questa è la differenza con /run
- I teammate comunicano TRA LORO via inbox — sfrutta questa capacità
- Ogni teammate riceve un brief strutturato: Missione, Contesto, Input, Output, Vincoli
- Ogni teammate riceve istruzioni su COME comunicare (write/read/TaskUpdate)
- `run_in_background: true` per teammate paralleli

Procedi.
