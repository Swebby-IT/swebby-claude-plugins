# Template: Monolith Modulare

## Overview

Architettura monolitica strutturata in moduli ben definiti, con separazione netta delle responsabilita' e confini chiari tra componenti.

---

## Quando Usare

**Ideale per:**
- Team piccoli-medi (2-10 sviluppatori)
- MVP e startup in fase iniziale
- Domini con confini non ancora chiari
- Budget limitato per infrastruttura
- Time-to-market veloce

**Evitare se:**
- Team molto grande (20+ sviluppatori)
- Necessita' di scaling estremo e indipendente
- Requisiti di deployment continuo multi-team
- Tecnologie diverse per componente

---

## Architettura di Riferimento

### C4 Context Diagram

```mermaid
graph TB
    subgraph "External"
        USER((User))
        ADMIN((Admin))
        EXT[External APIs]
    end

    subgraph "System"
        APP[Monolith Application]
    end

    subgraph "Data"
        DB[(Database)]
        CACHE[(Cache)]
    end

    USER -->|HTTPS| APP
    ADMIN -->|HTTPS| APP
    APP -->|API| EXT
    APP --> DB
    APP --> CACHE
```

### C4 Container Diagram

```mermaid
graph TB
    subgraph "Presentation Layer"
        WEB[Web Server<br/>Nginx]
        APP[Application Server]
    end

    subgraph "Application Layer"
        subgraph "Modules"
            AUTH[Auth Module]
            USER[User Module]
            PRODUCT[Product Module]
            ORDER[Order Module]
            PAYMENT[Payment Module]
        end
    end

    subgraph "Data Layer"
        DB[(PostgreSQL)]
        CACHE[(Redis)]
        SEARCH[(Elasticsearch)]
    end

    subgraph "External"
        MAIL[Email Service]
        PAY_GW[Payment Gateway]
    end

    WEB --> APP
    APP --> AUTH
    APP --> USER
    APP --> PRODUCT
    APP --> ORDER
    APP --> PAYMENT

    AUTH --> DB
    USER --> DB
    PRODUCT --> DB
    PRODUCT --> SEARCH
    ORDER --> DB
    ORDER --> CACHE
    PAYMENT --> PAY_GW

    AUTH --> MAIL
    ORDER --> MAIL
```

---

## Struttura Directory

### Clean Architecture

```
project/
├── src/
│   ├── domain/                 # Enterprise Business Rules
│   │   ├── entities/
│   │   │   ├── user.py
│   │   │   ├── product.py
│   │   │   └── order.py
│   │   ├── value_objects/
│   │   │   ├── email.py
│   │   │   └── money.py
│   │   └── exceptions/
│   │       └── domain_exceptions.py
│   │
│   ├── application/            # Application Business Rules
│   │   ├── use_cases/
│   │   │   ├── user/
│   │   │   │   ├── create_user.py
│   │   │   │   └── get_user.py
│   │   │   ├── product/
│   │   │   └── order/
│   │   ├── interfaces/         # Ports
│   │   │   ├── repositories/
│   │   │   │   ├── user_repository.py
│   │   │   │   └── product_repository.py
│   │   │   └── services/
│   │   │       ├── email_service.py
│   │   │       └── payment_service.py
│   │   └── dto/
│   │       ├── user_dto.py
│   │       └── order_dto.py
│   │
│   ├── infrastructure/         # Frameworks & Drivers
│   │   ├── persistence/
│   │   │   ├── repositories/
│   │   │   │   ├── sqlalchemy_user_repo.py
│   │   │   │   └── sqlalchemy_product_repo.py
│   │   │   ├── models/
│   │   │   │   ├── user_model.py
│   │   │   │   └── product_model.py
│   │   │   └── migrations/
│   │   ├── external/
│   │   │   ├── email/
│   │   │   │   └── smtp_email_service.py
│   │   │   └── payment/
│   │   │       └── stripe_payment_service.py
│   │   ├── cache/
│   │   │   └── redis_cache.py
│   │   └── config/
│   │       ├── settings.py
│   │       └── dependencies.py
│   │
│   └── presentation/           # Interface Adapters
│       ├── api/
│       │   ├── v1/
│       │   │   ├── routes/
│       │   │   │   ├── user_routes.py
│       │   │   │   └── product_routes.py
│       │   │   └── schemas/
│       │   │       ├── user_schemas.py
│       │   │       └── product_schemas.py
│       │   └── middleware/
│       │       ├── auth_middleware.py
│       │       └── error_handler.py
│       ├── cli/
│       │   └── commands/
│       └── web/
│           ├── templates/
│           └── static/
│
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   ├── application/
│   │   └── infrastructure/
│   ├── integration/
│   └── e2e/
│
├── docs/
├── scripts/
├── docker-compose.yml
├── Dockerfile
└── pyproject.toml
```

### Modular Monolith (Feature-based)

```
project/
├── src/
│   ├── core/                   # Shared kernel
│   │   ├── database.py
│   │   ├── security.py
│   │   ├── events.py
│   │   └── exceptions.py
│   │
│   ├── modules/
│   │   ├── auth/              # Auth module
│   │   │   ├── __init__.py
│   │   │   ├── domain/
│   │   │   ├── application/
│   │   │   ├── infrastructure/
│   │   │   └── api/
│   │   │
│   │   ├── users/             # Users module
│   │   │   ├── __init__.py
│   │   │   ├── domain/
│   │   │   ├── application/
│   │   │   ├── infrastructure/
│   │   │   └── api/
│   │   │
│   │   ├── products/          # Products module
│   │   │   └── ...
│   │   │
│   │   └── orders/            # Orders module
│   │       └── ...
│   │
│   ├── shared/                # Shared utilities
│   │   ├── utils/
│   │   └── types/
│   │
│   └── main.py                # Application entry point
│
├── tests/
│   └── modules/
│       ├── auth/
│       ├── users/
│       ├── products/
│       └── orders/
│
└── ...
```

---

## Pattern Chiave

### 1. Dependency Injection

```mermaid
graph TB
    subgraph "High Level"
        UC[Use Case]
    end
    subgraph "Abstraction"
        IF[Interface/Port]
    end
    subgraph "Low Level"
        IMPL[Implementation/Adapter]
    end

    UC -->|depends on| IF
    IMPL -->|implements| IF
```

**Esempio Python:**
```python
# application/interfaces/repositories/user_repository.py
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def find_by_id(self, user_id: int) -> User | None:
        pass

    @abstractmethod
    def save(self, user: User) -> User:
        pass

# infrastructure/persistence/repositories/sqlalchemy_user_repo.py
class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self._session = session

    def find_by_id(self, user_id: int) -> User | None:
        model = self._session.query(UserModel).get(user_id)
        return self._to_entity(model) if model else None
```

### 2. Use Case Pattern

```mermaid
sequenceDiagram
    participant C as Controller
    participant UC as Use Case
    participant R as Repository
    participant E as Entity

    C->>UC: execute(request)
    UC->>R: find(id)
    R-->>UC: entity
    UC->>E: business_logic()
    E-->>UC: result
    UC->>R: save(entity)
    UC-->>C: response
```

### 3. Repository Pattern

```mermaid
classDiagram
    class Repository~T~ {
        <<interface>>
        +find_by_id(id) T
        +find_all() List~T~
        +save(entity) T
        +delete(entity) void
    }

    class UserRepository {
        <<interface>>
        +find_by_email(email) User
    }

    class SQLAlchemyUserRepository {
        -session: Session
        +find_by_id(id) User
        +find_by_email(email) User
        +save(user) User
    }

    Repository <|-- UserRepository
    UserRepository <|.. SQLAlchemyUserRepository
```

### 4. Domain Events

```mermaid
sequenceDiagram
    participant UC as Use Case
    participant E as Entity
    participant EB as Event Bus
    participant H1 as Handler 1
    participant H2 as Handler 2

    UC->>E: create_order()
    E->>E: raise OrderCreated event
    UC->>EB: publish(entity.events)
    EB->>H1: handle(OrderCreated)
    EB->>H2: handle(OrderCreated)
    H1->>H1: Send email
    H2->>H2: Update inventory
```

---

## Layer Rules

### Dependency Rule (Clean Architecture)

```mermaid
graph TB
    subgraph "Outer"
        P[Presentation]
        I[Infrastructure]
    end
    subgraph "Middle"
        A[Application]
    end
    subgraph "Inner"
        D[Domain]
    end

    P -->|depends on| A
    I -->|depends on| A
    A -->|depends on| D
    D -->|depends on| NOTHING[Nothing]

    style D fill:#4CAF50
    style A fill:#2196F3
    style P fill:#FF9800
    style I fill:#FF9800
```

**Regole:**
1. **Domain** - Nessuna dipendenza esterna
2. **Application** - Dipende solo da Domain
3. **Infrastructure** - Implementa interfacce di Application
4. **Presentation** - Usa Application, non conosce Infrastructure

---

## Moduli e Comunicazione

### Comunicazione tra Moduli

```mermaid
graph LR
    subgraph "Orders Module"
        OC[Order Controller]
        OUC[Order Use Case]
        OR[Order Repository]
    end

    subgraph "Users Module"
        UF[User Facade]
        UUC[User Use Case]
    end

    subgraph "Products Module"
        PF[Product Facade]
        PUC[Product Use Case]
    end

    OUC -->|via facade| UF
    OUC -->|via facade| PF
    UF --> UUC
    PF --> PUC
```

**Pattern Facade per comunicazione:**
```python
# modules/users/facade.py
class UserFacade:
    def __init__(self, get_user_use_case: GetUserUseCase):
        self._get_user = get_user_use_case

    def get_user_info(self, user_id: int) -> UserDTO:
        return self._get_user.execute(user_id)

# modules/orders/application/use_cases/create_order.py
class CreateOrderUseCase:
    def __init__(
        self,
        order_repo: OrderRepository,
        user_facade: UserFacade,  # Not direct dependency
        product_facade: ProductFacade
    ):
        ...
```

### Anti-Corruption Layer

```mermaid
graph LR
    subgraph "Our Module"
        UC[Use Case]
        ACL[Anti-Corruption Layer]
    end
    subgraph "External/Legacy"
        EXT[External Service]
    end

    UC --> ACL
    ACL --> EXT
```

---

## Database Strategy

### Single Database, Separate Schemas

```mermaid
graph TB
    subgraph "PostgreSQL"
        subgraph "users schema"
            UT[users table]
            PT[profiles table]
        end
        subgraph "products schema"
            PRODT[products table]
            CATT[categories table]
        end
        subgraph "orders schema"
            OT[orders table]
            OIT[order_items table]
        end
    end
```

### Migrations Strategy

```
migrations/
├── versions/
│   ├── 001_initial_users.py
│   ├── 002_initial_products.py
│   ├── 003_initial_orders.py
│   ├── 004_add_user_preferences.py
│   └── ...
└── alembic.ini
```

---

## Testing Strategy

### Test Pyramid

```mermaid
graph TB
    subgraph "E2E Tests"
        E2E[Few, Slow, Expensive]
    end
    subgraph "Integration Tests"
        INT[Some, Medium Speed]
    end
    subgraph "Unit Tests"
        UNIT[Many, Fast, Cheap]
    end

    E2E --> INT
    INT --> UNIT

    style UNIT fill:#4CAF50
    style INT fill:#2196F3
    style E2E fill:#FF9800
```

### Test per Layer

| Layer | Tipo Test | Mock |
|-------|-----------|------|
| Domain | Unit | Nessuno |
| Application | Unit | Repository, Services |
| Infrastructure | Integration | Database reale (testcontainers) |
| Presentation | Integration | Application layer |
| E2E | E2E | Nessuno |

---

## Scalability Path

### Vertical Scaling

```mermaid
graph TB
    LB[Load Balancer]
    APP1[App Instance<br/>8 CPU, 32GB RAM]

    LB --> APP1
```

### Horizontal Scaling

```mermaid
graph TB
    LB[Load Balancer]
    APP1[App Instance 1]
    APP2[App Instance 2]
    APP3[App Instance 3]
    DB[(Database)]
    CACHE[(Redis)]

    LB --> APP1
    LB --> APP2
    LB --> APP3
    APP1 --> DB
    APP2 --> DB
    APP3 --> DB
    APP1 --> CACHE
    APP2 --> CACHE
    APP3 --> CACHE
```

### Toward Microservices

```mermaid
graph TB
    subgraph "Phase 1: Monolith"
        M[Modular Monolith]
    end

    subgraph "Phase 2: Extract"
        CORE[Core Monolith]
        SVC1[Extracted Service 1]
    end

    subgraph "Phase 3: More Services"
        CORE2[Smaller Core]
        SVC1B[Service 1]
        SVC2[Service 2]
        SVC3[Service 3]
    end

    M --> CORE
    M --> SVC1
    CORE --> CORE2
    CORE --> SVC2
    CORE --> SVC3
```

---

## Checklist Implementazione

### Struttura
- [ ] Layer separati (Domain, Application, Infrastructure, Presentation)
- [ ] Moduli con confini chiari
- [ ] Dependency injection configurata
- [ ] Interfacce per dipendenze esterne

### Domain
- [ ] Entities con business logic
- [ ] Value Objects per tipi complessi
- [ ] Domain Events definiti
- [ ] Nessuna dipendenza esterna

### Application
- [ ] Use Cases per ogni operazione
- [ ] DTOs per input/output
- [ ] Repository interfaces
- [ ] Service interfaces

### Infrastructure
- [ ] Repository implementations
- [ ] External service adapters
- [ ] Database configuration
- [ ] Cache configuration

### Presentation
- [ ] API routes organizzate
- [ ] Validation schemas
- [ ] Error handling middleware
- [ ] Authentication/Authorization

### Testing
- [ ] Unit tests per Domain
- [ ] Unit tests per Application (with mocks)
- [ ] Integration tests per Infrastructure
- [ ] E2E tests per flussi critici

---

## Trade-offs

| Aspetto | Pro | Contro |
|---------|-----|--------|
| Semplicita' | Facile da capire e deployare | Puo' diventare complesso |
| Performance | Chiamate in-process | Scaling limitato |
| Sviluppo | Refactoring facile | Rischio coupling |
| Deploy | Un solo artifact | Downtime per update |
| Testing | Integration test semplici | E2E puo' essere lento |
| Team | Codebase condivisa | Conflitti su merge |
