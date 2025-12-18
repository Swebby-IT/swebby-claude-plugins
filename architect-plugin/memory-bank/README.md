# Memory Bank

La Memory Bank e' una directory `.architect/` che contiene la documentazione architetturale persistente del progetto.

## Struttura

```
.architect/
├── architecture.md      # Overview architettura sistema
├── dependencies.md      # Grafo dipendenze
├── decisions.md         # Template e lista ADR
├── patterns.md          # Pattern usati nel progetto
├── tech-debt.md         # Registro technical debt
├── plans/               # Piani di implementazione
│   └── plan_YYYYMMDD_HHMMSS.md
├── diagrams/            # Diagrammi generati
│   └── diagram_YYYYMMDD_HHMMSS.md
├── reviews/             # Review dei piani
│   └── review_YYYYMMDD_HHMMSS.md
├── components/          # README per componenti
│   └── [component]-README.md
├── guides/              # Guide implementazione
│   └── [feature]-guide.md
├── api/                 # Documentazione API
│   └── [api]-docs.md
└── exports/             # File esportati
    └── [export].[ext]
```

## Inizializzazione

Per inizializzare la Memory Bank:

```
/architect:init
```

Questo comando:
1. Crea la directory `.architect/`
2. Analizza la codebase esistente
3. Genera i file base:
   - `architecture.md`
   - `dependencies.md`
   - `decisions.md`
   - `patterns.md`
   - `tech-debt.md`

## File Principali

### architecture.md

Contiene l'overview dell'architettura:
- Stack tecnologico
- Diagrammi C4 (Context, Container)
- Layer e moduli
- Flussi principali
- Entry points
- Configurazioni

### dependencies.md

Mappa le dipendenze:
- Dipendenze esterne (npm, pip, etc.)
- Dipendenze interne tra moduli
- Grafo dipendenze (Mermaid)
- Dipendenze circolari (se presenti)
- Aggiornamenti suggeriti

### decisions.md

Architecture Decision Records:
- Template ADR
- Lista ADR esistenti
- Stato (Proposed, Accepted, Deprecated)
- Storico decisioni

### patterns.md

Pattern e convenzioni:
- Pattern architetturali usati
- Design patterns identificati
- Convenzioni di naming
- Struttura file standard
- Error handling
- Logging
- Testing

### tech-debt.md

Registro technical debt:
- Sommario per severita'
- Dettaglio per ogni debito
- Priorita' di risoluzione
- Metriche qualita' codice

## Uso Quotidiano

### Aggiungere un Piano

```
/architect:plan Aggiungi sistema notifiche
```

Salva automaticamente in:
`.architect/plans/plan_20240115_143022.md`

### Aggiungere un ADR

1. Apri `.architect/decisions.md`
2. Copia il template ADR
3. Compila con la nuova decisione
4. Aggiungi alla lista

Oppure usa:
```
/architect:design sistema notifiche
```
Che genera ADR automaticamente.

### Aggiornare Technical Debt

1. Apri `.architect/tech-debt.md`
2. Aggiungi nuovo debito con template
3. Aggiorna sommario

### Generare Diagrammi

```
/architect:diagram auth module
```

Salva in:
`.architect/diagrams/auth_diagram_20240115_150000.md`

## Best Practices

### Mantenimento

1. **Aggiorna dopo ogni modifica significativa**
   - Nuovo componente? Aggiorna `architecture.md`
   - Nuova dipendenza? Aggiorna `dependencies.md`
   - Decisione importante? Crea ADR

2. **Review periodica**
   - Mensile: verifica accuratezza
   - Trimestrale: aggiorna tech-debt
   - Ad ogni release: verifica completezza

3. **Versionamento**
   - Committa `.architect/` nel repo
   - Review della documentazione nelle PR
   - Usa blame per storico modifiche

### Naming

| Tipo | Formato | Esempio |
|------|---------|---------|
| Piano | `plan_YYYYMMDD_HHMMSS.md` | `plan_20240115_143022.md` |
| Diagramma | `[tipo]_[target]_YYYYMMDD.md` | `sequence_auth_20240115.md` |
| Review | `review_[piano]_YYYYMMDD.md` | `review_notifications_20240115.md` |
| ADR | `ADR-NNN-[titolo].md` | `ADR-001-database-choice.md` |

### Contenuto

- **Conciso ma completo**: informazioni necessarie, non di piu'
- **Aggiornato**: documentazione obsoleta e' peggio di nessuna
- **Linkato**: riferimenti tra documenti correlati
- **Visuale**: diagrammi dove possibile

## Integrazione Git

### .gitignore

Raccomandazione: **NON ignorare** `.architect/`

La documentazione architetturale e' parte del progetto e dovrebbe essere versionata.

Eccezione: se contiene informazioni sensibili, aggiungi file specifici a `.gitignore`.

### Pre-commit Hook (opzionale)

```bash
#!/bin/sh
# Verifica che .architect/ sia aggiornato
if git diff --cached --name-only | grep -q "src/"; then
    echo "Ricorda di aggiornare .architect/ se necessario"
fi
```

## Comandi Correlati

| Comando | Descrizione |
|---------|-------------|
| `/architect:init` | Inizializza Memory Bank |
| `/architect:plan <req>` | Crea piano (salva in plans/) |
| `/architect:design <sys>` | Design completo (salva ADR) |
| `/architect:diagram <comp>` | Genera diagrammi |
| `/architect:review [plan]` | Review piano (salva in reviews/) |
| `/architect:export <fmt>` | Esporta (salva in exports/) |

## FAQ

**Q: Posso modificare i file manualmente?**
A: Si, sono file Markdown standard. Mantieni la struttura per compatibilita'.

**Q: Come gestisco conflitti di merge?**
A: Come qualsiasi altro file. I Mermaid diagram sono text-based quindi diffabili.

**Q: Quanto dettaglio nei diagrammi?**
A: Dipende dal pubblico. Overview per stakeholder, dettaglio per sviluppatori.

**Q: Devo documentare tutto?**
A: No, documenta cio' che e' importante e non ovvio dal codice.
