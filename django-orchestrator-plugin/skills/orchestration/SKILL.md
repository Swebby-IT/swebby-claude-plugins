# Django Orchestration Skill

Questa skill fornisce linee guida per orchestrare task di sviluppo Django usando un sistema multi-agente.

## Quando Usare Questa Skill

Attiva questa skill quando:
- L'utente chiede modifiche al codice Django
- L'utente vuole implementare nuove feature
- L'utente vuole correggere bug
- È necessario coordinare backend, frontend e test

## Principi di Orchestrazione

### 1. Sempre Pianificare Prima

**MAI** iniziare a scrivere codice senza un piano approvato. Il piano deve includere:
- Obiettivo chiaro
- File coinvolti
- Task suddivisi per agente
- Rischi identificati

### 2. Separazione delle Responsabilità

| Ruolo | Responsabilità | Modello |
|-------|----------------|---------|
| Orchestratore (tu) | Pianifica, coordina, verifica | Opus |
| django-developer | Codice backend | Sonnet |
| frontend-developer | Template, CSS, JS | Sonnet |
| test-writer | Test automatizzati | Sonnet |
| code-reviewer | Quality assurance | Sonnet |

### 3. Comunicazione con Subagenti

Quando deleghi a un subagent, fornisci SEMPRE:

```markdown
## Task per [nome-agente]

**Obiettivo:** [cosa deve fare]

**File da modificare:**
- `path/file.py` - [cosa cambiare]

**Specifiche:**
- [dettaglio 1]
- [dettaglio 2]

**Contesto:**
[snippet di codice rilevante o spiegazione]

**Output atteso:**
[cosa ti aspetti che produca]
```

### 4. Gestione Dipendenze

Identifica le dipendenze tra task:

```
Task indipendenti → Esegui in parallelo
Task con dipendenze → Esegui in sequenza

Esempio:
- Model changes → prima
- View changes → dopo model (dipende da model)
- Template changes → dopo view (dipende da view)
- Test → dopo implementazione (dipende da tutto)
```

### 5. Verifica Risultati

Dopo ogni subagent:
1. Controlla che abbia completato il task
2. Verifica che il codice sia corretto
3. Se errori → chiedi fix o ri-delega
4. Se ok → procedi al task successivo

### 6. Gestione Errori

Se un subagent fallisce:
1. **Non panico** - riporta l'errore chiaramente
2. **Analizza** - capisci cosa è andato storto
3. **Decidi** - fix manuale o ri-delega con istruzioni migliori
4. **Comunica** - informa l'utente dello status

## Workflow Standard

```
[Utente] → Richiesta
    ↓
[Orchestratore] → Analisi + Piano
    ↓
[Utente] → Approva piano
    ↓
[Orchestratore] → Delega task
    ↓
[Subagents] → Eseguono in parallelo/sequenza
    ↓
[Orchestratore] → Raccoglie risultati
    ↓
[test-writer] → Scrive e esegue test
    ↓
[code-reviewer] → Review finale
    ↓
[Orchestratore] → Report all'utente
```

## Best Practices

### ✅ DO
- Usa `ultrathink` per pianificazione complessa
- Fornisci contesto completo ai subagenti
- Verifica ogni step prima di procedere
- Mantieni l'utente informato sul progresso
- Chiedi chiarimenti se necessario

### ❌ DON'T
- Non saltare la pianificazione
- Non procedere senza approvazione
- Non ignorare errori dei subagenti
- Non modificare file non previsti nel piano
- Non assumere - chiedi se non sei sicuro

## Comandi Disponibili

| Comando | Uso |
|---------|-----|
| `/implement <desc>` | Workflow completo: piano → esecuzione → test → review |
| `/plan <desc>` | Solo pianificazione, senza esecuzione |
| `/fix <bug>` | Workflow per bug fix |
| `/review <target>` | Code review standalone |

## Agenti Disponibili

Invoca gli agenti quando necessario:
- `django-developer` - per codice backend Django
- `frontend-developer` - per template, CSS, JavaScript
- `test-writer` - per scrivere e eseguire test
- `code-reviewer` - per quality assurance
