---
description: Crea un design architetturale completo per un nuovo sistema o feature complessa
argument-hint: "<descrizione sistema da progettare>"
---

# Comando: /architect:design

Stai per creare un design architetturale completo per: **$ARGUMENTS**

---

## FASE 1: Comprensione Requisiti

### 1.1 Analisi Richiesta

```
Sistema da progettare: $ARGUMENTS

Domande chiave:
- Qual e' lo scopo principale del sistema?
- Chi sono gli utenti/attori?
- Quali sono i requisiti funzionali core?
- Quali sono i requisiti non funzionali (scalabilita', performance, sicurezza)?
- Esistono vincoli tecnologici o di business?
```

### 1.2 Chiarimenti Obbligatori

**FERMATI** e usa AskUserQuestion per chiarire:

1. **Scala prevista:**
   - Utenti concorrenti attesi?
   - Volume dati previsto?
   - Requisiti di latency?

2. **Stack tecnologico:**
   - Linguaggio/framework preferito?
   - Database preferenze?
   - Cloud provider/on-premise?

3. **Architettura preferita:**
   - Monolith modulare?
   - Microservizi?
   - Serverless?
   - Ibrida?

4. **Integrazioni:**
   - Sistemi esterni da integrare?
   - API da esporre?
   - Eventi/messaggi da gestire?

---

## FASE 2: Selezione Template

### 2.1 Valuta Template Disponibili

Leggi i template disponibili:
- `templates/microservices.md`
- `templates/monolith.md`
- `templates/serverless.md`
- `templates/mvc.md`

### 2.2 Seleziona Template Base

In base alle risposte dell'utente, seleziona il template piu' appropriato:

| Scenario | Template Consigliato |
|----------|---------------------|
| Team piccolo, MVP, dominio semplice | Monolith Modulare |
| Team grande, scaling indipendente, deploy frequenti | Microservizi |
| Carichi variabili, event-driven, pay-per-use | Serverless |
| Web app tradizionale, CRUD-heavy | MVC |

---

## FASE 3: Design Architetturale

### 3.1 Lancia Architect per Design

```
Task tool con subagent_type: architect:architect

Prompt:
"Crea un design architetturale completo per: $ARGUMENTS

Requisiti raccolti:
[inserisci risposte utente]

Template base selezionato: [template]

Il design deve includere:

1. **Overview Sistema**
   - Descrizione e scopo
   - Attori e casi d'uso principali
   - Vincoli e assunzioni

2. **Architettura Alto Livello**
   - C4 Context Diagram
   - C4 Container Diagram
   - Descrizione componenti principali

3. **Architettura Dettagliata**
   - Struttura directory proposta
   - Pattern architetturali da usare
   - Design patterns da applicare

4. **Data Architecture**
   - Schema database (ER diagram)
   - Strategia di persistenza
   - Caching strategy

5. **API Design**
   - Endpoints principali
   - Formato request/response
   - Autenticazione/Autorizzazione

6. **Integration Architecture**
   - Sistemi esterni
   - Protocolli di comunicazione
   - Event/Message flow

7. **Infrastructure**
   - Deployment diagram
   - Scaling strategy
   - Monitoring/Logging

8. **Security Architecture**
   - Threat model basics
   - Security controls
   - Data protection

9. **Piano di Implementazione**
   - Fasi di sviluppo
   - MVP scope
   - Roadmap evolutiva

Usa diagrammi Mermaid per ogni sezione visuale."
```

### 3.2 Genera Diagrammi Dettagliati

```
Task tool con subagent_type: architect:diagram-generator

Prompt:
"Genera diagrammi architetturali completi per: $ARGUMENTS

Diagrammi richiesti:
1. C4 Context Diagram
2. C4 Container Diagram
3. C4 Component Diagram (per componenti core)
4. Sequence Diagrams (per flussi principali)
5. ER Diagram (schema dati)
6. Deployment Diagram

Salva in .architect/diagrams/[sistema]/"
```

---

## FASE 4: Documentazione

### 4.1 Genera ADR Iniziali

```
Task tool con subagent_type: architect:documentation-writer

Prompt:
"Genera Architecture Decision Records per le decisioni chiave del design: $ARGUMENTS

ADR da creare:
1. ADR-001: Scelta architettura [monolith/microservices/etc]
2. ADR-002: Scelta database
3. ADR-003: Strategia autenticazione
4. ADR-004: Strategia deployment

Per ogni ADR:
- Contesto della decisione
- Decisione presa e motivazione
- Alternative considerate
- Conseguenze

Salva in .architect/decisions/"
```

### 4.2 Genera README Sistema

```
Task tool con subagent_type: architect:documentation-writer

Prompt:
"Genera README architetturale per: $ARGUMENTS

Includi:
- Overview sistema
- Quick start per sviluppatori
- Struttura progetto
- Come contribuire
- Riferimenti a diagrammi e ADR

Salva in .architect/[sistema]-README.md"
```

---

## FASE 5: Review Design

### 5.1 Valida con Plan Reviewer

```
Task tool con subagent_type: architect:plan-reviewer

Prompt:
"Rivedi il design architetturale per: $ARGUMENTS

[inserisci design completo]

Valuta:
1. Completezza del design
2. Coerenza tra componenti
3. Scalabilita' e performance
4. Security considerations
5. Fattibilita' implementazione
6. Alignment con best practices

Score e feedback dettagliato."
```

---

## FASE 6: Presentazione

### 6.1 Output Finale

Presenta il design completo:

```markdown
## Design Architetturale: [Nome Sistema]

**Data:** [YYYY-MM-DD]
**Versione:** 1.0
**Stato:** Draft / Review / Approved

---

### 1. Executive Summary

[Riassunto 2-3 paragrafi del sistema e delle scelte chiave]

### 2. Architettura

#### Context Diagram
```mermaid
[diagramma]
```

#### Container Diagram
```mermaid
[diagramma]
```

### 3. Componenti Principali

| Componente | Responsabilita' | Tecnologia |
|------------|-----------------|------------|

### 4. Data Model

```mermaid
erDiagram
[schema]
```

### 5. API Overview

| Endpoint | Metodo | Descrizione |
|----------|--------|-------------|

### 6. Flussi Principali

[Sequence diagrams per flussi chiave]

### 7. Deployment

```mermaid
[deployment diagram]
```

### 8. Decisioni Architetturali

| ADR | Titolo | Stato |
|-----|--------|-------|
| ADR-001 | ... | Accepted |

### 9. Piano di Implementazione

#### Fase 1: MVP
- [deliverable 1]
- [deliverable 2]

#### Fase 2: Features
- [deliverable 3]
- [deliverable 4]

#### Fase 3: Scale
- [deliverable 5]

### 10. Review Score: [X.X]/10

[Riepilogo feedback reviewer]

---

**File generati in .architect/:**
- [sistema]-README.md
- diagrams/[sistema]/
- decisions/ADR-001-*.md
- decisions/ADR-002-*.md
- ...
```

---

## REGOLE IMPORTANTI

1. **Chiedi SEMPRE chiarimenti** - Non assumere requisiti
2. **Usa template come base** - Non reinventare la ruota
3. **Documenta decisioni** - ADR per ogni scelta importante
4. **Visualizza** - Diagrammi per ogni aspetto
5. **Valida** - Review del design prima di presentare
6. **Itera** - Il design puo' evolvere con feedback

---

## OUTPUT ATTESO

Al termine del comando, l'utente avra':

1. **Design Document** completo con:
   - Architettura alto livello
   - Dettaglio componenti
   - Data model
   - API design
   - Deployment strategy

2. **Diagrammi** in `.architect/diagrams/`:
   - Context, Container, Component (C4)
   - Sequence diagrams
   - ER diagram
   - Deployment diagram

3. **ADR** in `.architect/decisions/`:
   - Decisioni architetturali documentate
   - Alternative considerate
   - Motivazioni

4. **README** in `.architect/`:
   - Overview sistema
   - Getting started
   - Riferimenti

5. **Review Score** con feedback per miglioramenti
