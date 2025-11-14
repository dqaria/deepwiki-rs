# Mermaid Diagram Patterns for Architecture Documentation

Quick reference for creating architecture diagrams with Mermaid.

---

## C4 Diagrams

### System Context (C1)

```mermaid
C4Context
    title System Context Diagram

    Person(user, "User", "End user")
    System(system, "Main System", "Core application")
    System_Ext(ext, "External API", "Third-party service")

    Rel(user, system, "Uses")
    Rel(system, ext, "Calls", "HTTPS")
```

### Container Diagram (C2)

```mermaid
C4Container
    title Container Diagram

    Container(web, "Web App", "React", "User interface")
    Container(api, "API", "Node.js", "Business logic")
    ContainerDb(db, "Database", "PostgreSQL", "Data storage")

    Rel(web, api, "API calls", "JSON/HTTPS")
    Rel(api, db, "Reads/Writes", "SQL")
```

### Component Diagram (C3)

```mermaid
C4Component
    title Component Diagram - API Module

    Component(controller, "Controller", "REST", "HTTP handlers")
    Component(service, "Service", "Business Logic", "Core processing")
    Component(repo, "Repository", "Data Access", "DB operations")
    ComponentDb(cache, "Cache", "Redis", "Session data")

    Rel(controller, service, "Calls")
    Rel(service, repo, "Uses")
    Rel(service, cache, "Caches")
```

---

## Sequence Diagrams (Workflows)

### Basic Request Flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as API
    participant D as Database

    U->>A: POST /api/items
    activate A
    A->>D: INSERT INTO items
    activate D
    D-->>A: ID=123
    deactivate D
    A-->>U: 201 Created
    deactivate A
```

### With Alternative Paths

```mermaid
sequenceDiagram
    participant C as Client
    participant S as Server
    participant DB as Database

    C->>S: Request data
    alt Success
        S->>DB: Query
        DB-->>S: Results
        S-->>C: 200 OK
    else Error
        S->>DB: Query
        DB-->>S: Error
        S-->>C: 500 Error
    end
```

### Authentication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant A as App
    participant Auth as Auth Service
    participant API as API Server

    U->>A: Login
    A->>Auth: Authenticate
    Auth-->>A: Token
    A->>API: Request + Token
    API->>Auth: Validate Token
    Auth-->>API: Valid
    API-->>A: Data
    A-->>U: Display
```

---

## Flowcharts (Decision Logic)

### Process Flow

```mermaid
flowchart TD
    Start([Start]) --> Input[Receive Request]
    Input --> Validate{Valid?}
    Validate -->|Yes| Process[Process Data]
    Validate -->|No| Error[Return Error]
    Process --> Save[(Save to DB)]
    Save --> Success[Return Success]
    Error --> End([End])
    Success --> End
```

### Conditional Workflow

```mermaid
flowchart LR
    A[User Action] --> B{Check Auth}
    B -->|Authenticated| C{Check Permission}
    B -->|Not Auth| D[Login Page]
    C -->|Allowed| E[Execute Action]
    C -->|Denied| F[403 Forbidden]
    D --> B
```

---

## Class Diagrams (Code Level)

### Basic Class Structure

```mermaid
classDiagram
    class User {
        +String name
        +String email
        +login()
        +logout()
    }

    class Order {
        +int id
        +Date created
        +decimal total
        +addItem()
        +checkout()
    }

    class Item {
        +String sku
        +decimal price
    }

    User "1" --> "*" Order : places
    Order "*" --> "*" Item : contains
```

### Inheritance

```mermaid
classDiagram
    class Animal {
        +String name
        +makeSound()
    }

    class Dog {
        +bark()
    }

    class Cat {
        +meow()
    }

    Animal <|-- Dog
    Animal <|-- Cat
```

---

## State Diagrams

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Review : Submit
    Review --> Approved : Approve
    Review --> Draft : Request Changes
    Approved --> Published : Publish
    Published --> Archived : Archive
    Archived --> [*]
```

---

## Entity Relationship Diagrams

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"

    USER {
        int id PK
        string email
        string name
    }

    ORDER {
        int id PK
        int user_id FK
        date created
        decimal total
    }

    PRODUCT {
        int id PK
        string sku
        decimal price
    }

    ORDER_ITEM {
        int order_id FK
        int product_id FK
        int quantity
    }
```

---

## Graph Diagrams (Dependencies)

### Simple Dependency Graph

```mermaid
graph TD
    A[Main] --> B[Module 1]
    A --> C[Module 2]
    B --> D[Utility]
    C --> D
    D --> E[Core]
```

### Left-to-Right

```mermaid
graph LR
    Frontend --> API
    API --> Database
    API --> Cache
    API --> Queue
```

### With Styling

```mermaid
graph TD
    A[Client]:::client --> B[Load Balancer]:::infra
    B --> C[Server 1]:::server
    B --> D[Server 2]:::server
    C --> E[(Database)]:::data
    D --> E

    classDef client fill:#e1f5ff,stroke:#01579b
    classDef infra fill:#fff9c4,stroke:#f57f17
    classDef server fill:#c8e6c9,stroke:#2e7d32
    classDef data fill:#f8bbd0,stroke:#c2185b
```

---

## Common Patterns

### Microservices Architecture

```mermaid
C4Container
    title Microservices Architecture

    Container(web, "Web UI", "React")
    Container(gateway, "API Gateway", "Kong")
    Container(auth, "Auth Service", "Node.js")
    Container(user, "User Service", "Python")
    Container(order, "Order Service", "Java")
    ContainerDb(db1, "User DB", "PostgreSQL")
    ContainerDb(db2, "Order DB", "MongoDB")

    Rel(web, gateway, "HTTPS")
    Rel(gateway, auth, "gRPC")
    Rel(gateway, user, "REST")
    Rel(gateway, order, "REST")
    Rel(user, db1, "SQL")
    Rel(order, db2, "NoSQL")
```

### Layered Architecture

```mermaid
flowchart TB
    subgraph Presentation
        UI[Web UI]
        API[REST API]
    end

    subgraph Business
        Service[Business Logic]
        Rules[Business Rules]
    end

    subgraph Data
        Repo[Repository]
        DB[(Database)]
    end

    UI --> API
    API --> Service
    Service --> Rules
    Rules --> Repo
    Repo --> DB
```

### Event-Driven Architecture

```mermaid
flowchart LR
    Producer1[Service A] --> Queue[Message Queue]
    Producer2[Service B] --> Queue
    Queue --> Consumer1[Service C]
    Queue --> Consumer2[Service D]
    Consumer1 --> DB1[(DB 1)]
    Consumer2 --> DB2[(DB 2)]
```

---

## Auto-Fix Patterns

### Common Mermaid Errors

❌ **Missing quotes around labels with spaces**
```mermaid
Rel(a, b, Uses API)  # Error!
```

✅ **Fixed**
```mermaid
Rel(a, b, "Uses API")  # Correct
```

❌ **Special characters not escaped**
```mermaid
System(api, "User's API")  # Error!
```

✅ **Fixed**
```mermaid
System(api, "User&apos;s API")  # Correct
```

❌ **Missing diagram type**
```mermaid
graph
    A --> B  # Error!
```

✅ **Fixed**
```mermaid
graph TD
    A --> B  # Correct
```

---

## Best Practices

1. **Keep it simple**: Max 7-10 nodes per diagram
2. **Use meaningful IDs**: `userService` not `s1`
3. **Add titles**: Every diagram should have a title
4. **Show direction**: Use arrows to indicate data flow
5. **Group related items**: Use subgraphs for modules
6. **Consistent naming**: Same entity = same name across diagrams
7. **Include technology**: Specify languages, frameworks, databases

## Diagram Selection Guide

| Need to Show | Use This Diagram |
|-------------|------------------|
| System boundaries | C4 Context |
| High-level architecture | C4 Container |
| Module internals | C4 Component |
| Data flow over time | Sequence Diagram |
| Decision logic | Flowchart |
| Code structure | Class Diagram |
| State transitions | State Diagram |
| Data relationships | ER Diagram |
| Dependencies | Graph |
