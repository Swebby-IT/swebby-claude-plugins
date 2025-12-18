# Template: Architettura Microservizi

## Overview

Architettura distribuita basata su servizi indipendenti, ognuno con la propria responsabilita', database e ciclo di deployment.

---

## Quando Usare

**Ideale per:**
- Team grandi (5+ sviluppatori)
- Necessita' di scaling indipendente
- Deployment frequenti e indipendenti
- Diversi linguaggi/tecnologie per servizio
- Alta disponibilita' richiesta

**Evitare se:**
- Team piccolo (< 5 sviluppatori)
- MVP o prototipo
- Budget limitato per infrastruttura
- Dominio semplice senza confini chiari

---

## Architettura di Riferimento

### C4 Context Diagram

```mermaid
graph TB
    subgraph "External"
        USER((User))
        MOBILE((Mobile App))
        PARTNER[Partner Systems]
    end

    subgraph "System Boundary"
        GW[API Gateway]
    end

    USER -->|HTTPS| GW
    MOBILE -->|HTTPS| GW
    PARTNER -->|API| GW
```

### C4 Container Diagram

```mermaid
graph TB
    subgraph "Frontend"
        WEB[Web App<br/>React/Vue/Angular]
        MOBILE[Mobile App<br/>React Native/Flutter]
    end

    subgraph "API Layer"
        GW[API Gateway<br/>Kong/Nginx/AWS ALB]
        AUTH[Auth Service<br/>OAuth2/JWT]
    end

    subgraph "Core Services"
        USER_SVC[User Service]
        PRODUCT_SVC[Product Service]
        ORDER_SVC[Order Service]
        PAYMENT_SVC[Payment Service]
        NOTIFICATION_SVC[Notification Service]
    end

    subgraph "Data Layer"
        USER_DB[(User DB<br/>PostgreSQL)]
        PRODUCT_DB[(Product DB<br/>PostgreSQL)]
        ORDER_DB[(Order DB<br/>PostgreSQL)]
        CACHE[(Cache<br/>Redis)]
    end

    subgraph "Messaging"
        QUEUE[Message Broker<br/>RabbitMQ/Kafka]
    end

    subgraph "Infrastructure"
        LOG[Logging<br/>ELK Stack]
        MONITOR[Monitoring<br/>Prometheus/Grafana]
        TRACE[Tracing<br/>Jaeger/Zipkin]
    end

    WEB --> GW
    MOBILE --> GW
    GW --> AUTH
    GW --> USER_SVC
    GW --> PRODUCT_SVC
    GW --> ORDER_SVC
    GW --> PAYMENT_SVC

    USER_SVC --> USER_DB
    PRODUCT_SVC --> PRODUCT_DB
    ORDER_SVC --> ORDER_DB
    ORDER_SVC --> CACHE

    ORDER_SVC -->|publish| QUEUE
    PAYMENT_SVC -->|consume| QUEUE
    NOTIFICATION_SVC -->|consume| QUEUE

    USER_SVC --> LOG
    PRODUCT_SVC --> LOG
    ORDER_SVC --> LOG
```

---

## Struttura Directory

### Monorepo

```
project/
├── services/
│   ├── user-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── product-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── order-service/
│   │   └── ...
│   └── payment-service/
│       └── ...
├── shared/
│   ├── proto/              # gRPC definitions
│   ├── schemas/            # JSON schemas
│   └── utils/              # Shared utilities
├── infrastructure/
│   ├── docker-compose.yml
│   ├── kubernetes/
│   │   ├── base/
│   │   └── overlays/
│   └── terraform/
├── gateway/
│   └── kong.yml
└── docs/
    ├── architecture/
    └── api/
```

### Multi-Repo

```
organization/
├── user-service/           # Repo separato
├── product-service/        # Repo separato
├── order-service/          # Repo separato
├── shared-libs/            # Librerie condivise
└── infrastructure/         # IaC
```

---

## Pattern Chiave

### 1. API Gateway

```mermaid
sequenceDiagram
    participant C as Client
    participant G as API Gateway
    participant A as Auth
    participant S as Service

    C->>G: Request + Token
    G->>A: Validate Token
    A-->>G: Valid
    G->>G: Rate Limit Check
    G->>G: Transform Request
    G->>S: Forward Request
    S-->>G: Response
    G->>G: Transform Response
    G-->>C: Response
```

**Responsabilita':**
- Authentication/Authorization
- Rate limiting
- Request/Response transformation
- Load balancing
- Circuit breaking
- Logging/Monitoring

### 2. Service Discovery

```mermaid
graph LR
    SVC1[Service A] -->|register| SD[(Service Registry)]
    SVC2[Service B] -->|register| SD
    SVC3[Service C] -->|discover| SD
    SVC3 -->|call| SVC1
```

**Opzioni:**
- Consul
- Eureka
- Kubernetes DNS
- AWS Cloud Map

### 3. Event-Driven Communication

```mermaid
sequenceDiagram
    participant O as Order Service
    participant Q as Message Queue
    participant P as Payment Service
    participant N as Notification Service

    O->>Q: OrderCreated event
    Q-->>P: Consume
    Q-->>N: Consume
    P->>P: Process Payment
    P->>Q: PaymentCompleted event
    Q-->>O: Consume
    Q-->>N: Consume
    O->>O: Update Order Status
    N->>N: Send Email
```

### 4. Database per Service

```mermaid
graph TB
    subgraph "User Service"
        US[User Service]
        UDB[(User DB)]
    end
    subgraph "Order Service"
        OS[Order Service]
        ODB[(Order DB)]
    end
    subgraph "Product Service"
        PS[Product Service]
        PDB[(Product DB)]
    end

    US --> UDB
    OS --> ODB
    PS --> PDB
    OS -.->|API call| US
    OS -.->|API call| PS
```

### 5. Saga Pattern (Distributed Transactions)

```mermaid
sequenceDiagram
    participant O as Orchestrator
    participant I as Inventory
    participant P as Payment
    participant S as Shipping

    O->>I: Reserve Items
    I-->>O: Reserved
    O->>P: Process Payment
    P-->>O: Paid
    O->>S: Create Shipment
    S-->>O: Created

    Note over O: If any step fails
    O->>S: Cancel Shipment
    O->>P: Refund
    O->>I: Release Items
```

---

## Comunicazione tra Servizi

### Sincrona (HTTP/gRPC)

| Metodo | Quando | Pro | Contro |
|--------|--------|-----|--------|
| REST | CRUD, query semplici | Semplice, universale | Latenza, coupling |
| gRPC | Alta performance, streaming | Veloce, type-safe | Complessita' |
| GraphQL | Aggregazione, flessibilita' | Flessibile | Overhead |

### Asincrona (Events/Messages)

| Pattern | Quando | Pro | Contro |
|---------|--------|-----|--------|
| Pub/Sub | Notifiche, broadcast | Decoupling | Eventual consistency |
| Queue | Task processing | Retry, ordering | Complessita' |
| Event Sourcing | Audit, replay | Tracciabilita' | Storage |

---

## Data Management

### Strategie

| Strategia | Descrizione | Quando |
|-----------|-------------|--------|
| Database per Service | Ogni servizio ha il suo DB | Default |
| Shared Database | Servizi condividono DB | Legacy migration |
| CQRS | Separazione read/write | Alta scalabilita' read |
| Event Sourcing | Eventi come source of truth | Audit required |

### Gestione Transazioni Distribuite

```mermaid
stateDiagram-v2
    [*] --> Pending
    Pending --> Processing: Start Saga
    Processing --> Committed: All Success
    Processing --> Compensating: Any Failure
    Compensating --> RolledBack: Compensations Done
    Committed --> [*]
    RolledBack --> [*]
```

---

## Observability

### Three Pillars

```mermaid
graph TB
    subgraph "Logging"
        L1[Service A Logs]
        L2[Service B Logs]
        ELK[ELK Stack]
    end
    subgraph "Metrics"
        M1[Service A Metrics]
        M2[Service B Metrics]
        PROM[Prometheus]
        GRAF[Grafana]
    end
    subgraph "Tracing"
        T1[Service A Spans]
        T2[Service B Spans]
        JAEGER[Jaeger]
    end

    L1 --> ELK
    L2 --> ELK
    M1 --> PROM
    M2 --> PROM
    PROM --> GRAF
    T1 --> JAEGER
    T2 --> JAEGER
```

### Correlation ID

```mermaid
sequenceDiagram
    participant C as Client
    participant G as Gateway
    participant S1 as Service A
    participant S2 as Service B

    C->>G: Request
    G->>G: Generate correlation-id: abc123
    G->>S1: Request [correlation-id: abc123]
    S1->>S2: Request [correlation-id: abc123]
    S2-->>S1: Response [correlation-id: abc123]
    S1-->>G: Response [correlation-id: abc123]
    G-->>C: Response [correlation-id: abc123]
```

---

## Deployment

### Kubernetes

```yaml
# Service deployment example
apiVersion: apps/v1
kind: Deployment
metadata:
  name: user-service
spec:
  replicas: 3
  selector:
    matchLabels:
      app: user-service
  template:
    metadata:
      labels:
        app: user-service
    spec:
      containers:
      - name: user-service
        image: myregistry/user-service:v1.0.0
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
```

---

## Checklist Implementazione

### Infrastruttura
- [ ] Container orchestration (Kubernetes)
- [ ] Service mesh (Istio/Linkerd) - opzionale
- [ ] API Gateway configurato
- [ ] Message broker setup
- [ ] Centralized logging
- [ ] Distributed tracing
- [ ] Metrics collection

### Per Servizio
- [ ] Dockerfile ottimizzato
- [ ] Health endpoints (/health, /ready)
- [ ] Graceful shutdown
- [ ] Configuration via env vars
- [ ] Correlation ID propagation
- [ ] Circuit breaker
- [ ] Retry with backoff
- [ ] Rate limiting

### Data
- [ ] Database isolato per servizio
- [ ] Migration strategy
- [ ] Backup/restore plan
- [ ] Data consistency strategy

### Security
- [ ] Service-to-service auth (mTLS)
- [ ] Secrets management
- [ ] Network policies
- [ ] API authentication

---

## Trade-offs

| Aspetto | Pro | Contro |
|---------|-----|--------|
| Scalabilita' | Scaling indipendente | Complessita' operativa |
| Deployment | Deploy indipendenti | CI/CD complesso |
| Team | Team autonomi | Coordinamento difficile |
| Tecnologia | Liberta' di scelta | Skill diverse richieste |
| Resilienza | Failure isolation | Gestione failure distribuiti |
| Testing | Unit test semplici | Integration test complessi |
