# Template: Architettura Serverless

## Overview

Architettura basata su funzioni stateless eseguite on-demand, con scaling automatico e modello pay-per-use. Ideale per workload variabili ed event-driven.

---

## Quando Usare

**Ideale per:**
- Carichi di lavoro variabili/imprevedibili
- Event-driven processing
- API con traffico burst
- Batch processing periodico
- MVP con budget limitato
- Integrazioni e automazioni

**Evitare se:**
- Latenza critica (cold start problematico)
- Processi long-running (>15 min)
- Stato persistente necessario in-memory
- Alto throughput costante (piu' costoso)
- Vendor lock-in inaccettabile

---

## Architettura di Riferimento

### C4 Context Diagram

```mermaid
graph TB
    subgraph "External"
        USER((User))
        MOBILE((Mobile))
        IOT[IoT Devices]
        SCHEDULE[Scheduler]
    end

    subgraph "Cloud Platform"
        SERVERLESS[Serverless Application]
    end

    USER -->|HTTPS| SERVERLESS
    MOBILE -->|HTTPS| SERVERLESS
    IOT -->|Events| SERVERLESS
    SCHEDULE -->|Cron| SERVERLESS
```

### C4 Container Diagram (AWS Example)

```mermaid
graph TB
    subgraph "Edge"
        CF[CloudFront CDN]
        APIGW[API Gateway]
    end

    subgraph "Compute"
        FN1[Lambda: API Handler]
        FN2[Lambda: Event Processor]
        FN3[Lambda: Scheduled Job]
    end

    subgraph "Storage"
        S3[(S3 Bucket)]
        DDB[(DynamoDB)]
        RDS[(RDS/Aurora Serverless)]
    end

    subgraph "Messaging"
        SQS[SQS Queue]
        SNS[SNS Topic]
        EB[EventBridge]
    end

    subgraph "Auth"
        COG[Cognito]
    end

    CF --> APIGW
    APIGW --> FN1
    FN1 --> DDB
    FN1 --> RDS

    S3 -->|trigger| FN2
    SQS -->|trigger| FN2
    SNS -->|trigger| FN2
    FN2 --> DDB

    EB -->|schedule| FN3
    FN3 --> S3

    APIGW --> COG
```

### Multi-Cloud View

```mermaid
graph TB
    subgraph "AWS"
        LAMBDA[Lambda]
        DYNAMO[(DynamoDB)]
        APIGW_AWS[API Gateway]
    end

    subgraph "Google Cloud"
        FUNC[Cloud Functions]
        FIRE[(Firestore)]
        APIGW_GCP[Cloud Endpoints]
    end

    subgraph "Azure"
        AZFN[Azure Functions]
        COSMOS[(CosmosDB)]
        APIM[API Management]
    end

    subgraph "Agnostic"
        KNATIVE[Knative]
        OPENFAAS[OpenFaaS]
    end
```

---

## Struttura Directory

### Single Function Project

```
project/
├── src/
│   ├── handlers/
│   │   ├── api/
│   │   │   ├── users.py
│   │   │   ├── products.py
│   │   │   └── orders.py
│   │   ├── events/
│   │   │   ├── s3_processor.py
│   │   │   ├── sqs_consumer.py
│   │   │   └── sns_handler.py
│   │   └── scheduled/
│   │       ├── daily_report.py
│   │       └── cleanup.py
│   │
│   ├── services/
│   │   ├── user_service.py
│   │   ├── notification_service.py
│   │   └── payment_service.py
│   │
│   ├── repositories/
│   │   ├── dynamodb/
│   │   │   └── user_repository.py
│   │   └── s3/
│   │       └── file_repository.py
│   │
│   ├── models/
│   │   ├── user.py
│   │   └── order.py
│   │
│   └── utils/
│       ├── logger.py
│       ├── validators.py
│       └── response.py
│
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── infrastructure/
│   ├── serverless.yml          # Serverless Framework
│   ├── template.yaml           # SAM
│   └── terraform/
│       ├── main.tf
│       ├── lambda.tf
│       └── api_gateway.tf
│
├── scripts/
│   ├── deploy.sh
│   └── local.sh
│
├── requirements.txt
└── README.md
```

### Multi-Service Project

```
project/
├── services/
│   ├── api-service/
│   │   ├── src/
│   │   ├── serverless.yml
│   │   └── package.json
│   │
│   ├── processor-service/
│   │   ├── src/
│   │   ├── serverless.yml
│   │   └── package.json
│   │
│   └── notification-service/
│       ├── src/
│       ├── serverless.yml
│       └── package.json
│
├── shared/
│   ├── models/
│   ├── utils/
│   └── package.json
│
├── infrastructure/
│   ├── base/                    # VPC, IAM, shared resources
│   └── environments/
│       ├── dev/
│       ├── staging/
│       └── prod/
│
└── scripts/
    └── deploy-all.sh
```

---

## Pattern Chiave

### 1. API Gateway + Lambda

```mermaid
sequenceDiagram
    participant C as Client
    participant GW as API Gateway
    participant L as Lambda
    participant DB as DynamoDB

    C->>GW: GET /users/123
    GW->>GW: Validate request
    GW->>GW: Check auth (Cognito/JWT)
    GW->>L: Invoke handler
    L->>L: Cold start (if needed)
    L->>DB: GetItem
    DB-->>L: User data
    L-->>GW: JSON response
    GW-->>C: 200 OK
```

**Handler Example (Python):**
```python
import json
from services.user_service import UserService

def handler(event, context):
    """GET /users/{id}"""
    try:
        user_id = event['pathParameters']['id']
        user_service = UserService()
        user = user_service.get_by_id(user_id)

        if not user:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'User not found'})
            }

        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps(user.to_dict())
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### 2. Event-Driven Processing

```mermaid
sequenceDiagram
    participant S3 as S3 Bucket
    participant L1 as Lambda: Processor
    participant SQS as SQS Queue
    participant L2 as Lambda: Worker
    participant DB as DynamoDB
    participant SNS as SNS Topic

    S3->>L1: ObjectCreated event
    L1->>L1: Validate file
    L1->>SQS: Send messages (batch)

    loop For each message
        SQS->>L2: Trigger
        L2->>L2: Process item
        L2->>DB: Save result
    end

    L2->>SNS: Publish completion
    SNS->>SNS: Fan-out to subscribers
```

### 3. Saga Pattern (Distributed Transactions)

```mermaid
sequenceDiagram
    participant API as API Lambda
    participant SF as Step Functions
    participant L1 as Lambda: Reserve
    participant L2 as Lambda: Payment
    participant L3 as Lambda: Ship
    participant L4 as Lambda: Compensate

    API->>SF: Start execution
    SF->>L1: Reserve inventory
    L1-->>SF: Success

    SF->>L2: Process payment
    alt Payment Success
        L2-->>SF: Success
        SF->>L3: Create shipment
        L3-->>SF: Success
        SF-->>API: Order completed
    else Payment Failed
        L2-->>SF: Failed
        SF->>L4: Compensate (release inventory)
        L4-->>SF: Compensated
        SF-->>API: Order failed
    end
```

### 4. Fan-Out Pattern

```mermaid
graph TB
    subgraph "Trigger"
        S3[S3 Upload]
    end

    subgraph "Distribution"
        SNS[SNS Topic]
    end

    subgraph "Processors"
        L1[Lambda: Thumbnail]
        L2[Lambda: Metadata]
        L3[Lambda: ML Analysis]
        L4[Lambda: Archive]
    end

    S3 --> SNS
    SNS --> L1
    SNS --> L2
    SNS --> L3
    SNS --> L4
```

### 5. CQRS with Event Sourcing

```mermaid
graph LR
    subgraph "Command Side"
        API[API Gateway]
        CMD[Command Lambda]
        EVT[(Event Store<br/>DynamoDB Streams)]
    end

    subgraph "Event Processing"
        PROC[Processor Lambda]
    end

    subgraph "Query Side"
        READ[(Read Model<br/>Elasticsearch)]
        QUERY[Query Lambda]
    end

    API --> CMD
    CMD --> EVT
    EVT --> PROC
    PROC --> READ
    READ --> QUERY
```

---

## Cold Start Mitigation

### Strategie

| Strategia | Descrizione | Trade-off |
|-----------|-------------|-----------|
| Provisioned Concurrency | Lambda pre-riscaldate | Costo fisso |
| Keep-warm | Ping periodico | Complessita' |
| Smaller packages | Bundle minimo | Manutenzione |
| Lazy loading | Import on-demand | Complessita' codice |
| SnapStart (Java) | Snapshot JVM | Solo Java |

### Provisioned Concurrency

```mermaid
graph LR
    subgraph "Without PC"
        REQ1[Request] --> COLD[Cold Start: 2-5s]
        COLD --> EXEC1[Execution]
    end

    subgraph "With PC"
        REQ2[Request] --> WARM[Warm: <100ms]
        WARM --> EXEC2[Execution]
    end
```

---

## Database Patterns

### DynamoDB Single Table Design

```mermaid
erDiagram
    SINGLE_TABLE {
        string PK "Partition Key"
        string SK "Sort Key"
        string GSI1PK "GSI1 Partition"
        string GSI1SK "GSI1 Sort"
        map data "Attributes"
    }
```

**Access Patterns:**
| Pattern | PK | SK |
|---------|----|----|
| Get user | USER#123 | PROFILE |
| Get user orders | USER#123 | ORDER#* |
| Get order | ORDER#456 | ORDER#456 |
| Get order items | ORDER#456 | ITEM#* |

### Aurora Serverless v2

```mermaid
graph TB
    subgraph "Connection"
        PROXY[RDS Proxy]
    end

    subgraph "Aurora Serverless"
        WRITER[(Writer)]
        READER1[(Reader 1)]
        READER2[(Reader 2)]
    end

    LAMBDA[Lambda] --> PROXY
    PROXY --> WRITER
    PROXY --> READER1
    PROXY --> READER2
```

---

## Infrastructure as Code

### Serverless Framework

```yaml
# serverless.yml
service: my-service

provider:
  name: aws
  runtime: python3.11
  region: eu-west-1
  memorySize: 256
  timeout: 30
  environment:
    TABLE_NAME: ${self:custom.tableName}

custom:
  tableName: ${self:service}-${self:provider.stage}

functions:
  getUser:
    handler: src/handlers/api/users.get_handler
    events:
      - http:
          path: users/{id}
          method: get
          cors: true

  processUpload:
    handler: src/handlers/events/s3_processor.handler
    events:
      - s3:
          bucket: ${self:custom.uploadBucket}
          event: s3:ObjectCreated:*

  dailyReport:
    handler: src/handlers/scheduled/daily_report.handler
    events:
      - schedule: cron(0 8 * * ? *)

resources:
  Resources:
    UsersTable:
      Type: AWS::DynamoDB::Table
      Properties:
        TableName: ${self:custom.tableName}
        BillingMode: PAY_PER_REQUEST
        AttributeDefinitions:
          - AttributeName: PK
            AttributeType: S
          - AttributeName: SK
            AttributeType: S
        KeySchema:
          - AttributeName: PK
            KeyType: HASH
          - AttributeName: SK
            KeyType: RANGE
```

### AWS SAM

```yaml
# template.yaml
AWSTemplateFormatVersion: '2010-09-09'
Transform: AWS::Serverless-2016-10-31

Globals:
  Function:
    Timeout: 30
    Runtime: python3.11
    MemorySize: 256

Resources:
  GetUserFunction:
    Type: AWS::Serverless::Function
    Properties:
      CodeUri: src/
      Handler: handlers.api.users.get_handler
      Events:
        GetUser:
          Type: Api
          Properties:
            Path: /users/{id}
            Method: get
```

---

## Observability

### Distributed Tracing (X-Ray)

```mermaid
graph LR
    subgraph "Trace"
        SEG1[API Gateway<br/>Segment]
        SEG2[Lambda<br/>Segment]
        SUB1[DynamoDB<br/>Subsegment]
        SUB2[External API<br/>Subsegment]
    end

    SEG1 --> SEG2
    SEG2 --> SUB1
    SEG2 --> SUB2
```

### CloudWatch Insights

```
# Query per errori
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 100

# Query per cold starts
filter @type = "REPORT"
| stats avg(@duration), max(@duration), count(*) by bin(5m)
| filter @message like /Init Duration/
```

### Custom Metrics

```python
from aws_lambda_powertools import Metrics
from aws_lambda_powertools.metrics import MetricUnit

metrics = Metrics()

@metrics.log_metrics
def handler(event, context):
    metrics.add_metric(
        name="OrdersProcessed",
        unit=MetricUnit.Count,
        value=1
    )
    metrics.add_dimension("Environment", "prod")
```

---

## Security

### IAM Best Practices

```yaml
# Least privilege
Statement:
  - Effect: Allow
    Action:
      - dynamodb:GetItem
      - dynamodb:PutItem
    Resource:
      - !GetAtt UsersTable.Arn
```

### Secrets Management

```mermaid
graph LR
    LAMBDA[Lambda] --> CACHE[Local Cache]
    CACHE -->|miss| SM[Secrets Manager]
    SM --> KMS[KMS Decrypt]
    KMS --> LAMBDA
```

---

## Checklist Implementazione

### Setup
- [ ] Account cloud configurato
- [ ] IAM roles/policies
- [ ] VPC (se necessario)
- [ ] API Gateway configurato
- [ ] CI/CD pipeline

### Per Funzione
- [ ] Handler implementato
- [ ] Input validation
- [ ] Error handling
- [ ] Logging strutturato
- [ ] Timeout appropriato
- [ ] Memory sizing
- [ ] Cold start ottimizzato

### Database
- [ ] Schema progettato
- [ ] Access patterns definiti
- [ ] Indexes configurati
- [ ] Backup/restore

### Security
- [ ] IAM least privilege
- [ ] Secrets in Secrets Manager
- [ ] Encryption at rest/transit
- [ ] WAF (se API pubblica)

### Observability
- [ ] X-Ray tracing
- [ ] CloudWatch alarms
- [ ] Custom metrics
- [ ] Log retention policy

---

## Trade-offs

| Aspetto | Pro | Contro |
|---------|-----|--------|
| Costo | Pay-per-use, no idle cost | Puo' essere costoso ad alto volume |
| Scaling | Automatico, quasi infinito | Cold start latency |
| Ops | Zero server management | Debugging distribuito complesso |
| Vendor | Servizi managed integrati | Lock-in significativo |
| Dev | Focus su business logic | Nuovi pattern da imparare |
| Latency | Buona per carichi variabili | Cold start problematico |
