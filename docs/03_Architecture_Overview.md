# RegTech Horizon -- Architecture Overview

## Document Control

| Field | Value |
|-------|-------|
| Document ID | RT-ARCH-003 |
| Version | 2.0 |
| Status | Current |

---

## 1. System Architecture

### 1.1 High-Level Architecture Diagram

```
                         ┌──────────────────────────┐
                         │     External Systems      │
                         │  Eramba GRC, SAP, ERP     │
                         └────────────┬─────────────┘
                                      │ Webhooks
                                      ▼
┌─────────────────────────────────────────────────────────────────┐
│                    RegTech Horizon Platform                       │
│                                                                   │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────────┐  │
│  │ Next.js  │   │ React    │   │ GRC      │   │ File Watcher │  │
│  │ Dashboard│   │ Native   │   │ Adapter  │   │ (Watchdog)   │  │
│  │ :3000    │   │ Mobile   │   │ :8000    │   │              │  │
│  └────┬─────┘   └────┬─────┘   └────┬─────┘   └──────┬───────┘  │
│       │              │              │                  │          │
│       └──────────────┼──────────────┘                  │          │
│                      ▼                                 │          │
│  ┌───────────────────────────────────────────────────┐ │          │
│  │              FastAPI Backend (:8000)               │ │          │
│  │                                                   │ │          │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │ │          │
│  │  │   NCC   │ │   FCC   │ │   CBN   │            │ │          │
│  │  │ Module  │ │ Module  │ │ Module  │            │ │          │
│  │  │         │ │         │ │         │            │ │          │
│  │  │ Report  │ │ Form477 │ │ AML/CFT │            │ │          │
│  │  │ AOL     │ │ Form499 │ │ Cyber   │            │ │          │
│  │  │ QoS     │ │ CPNI    │ │ CAR     │            │ │          │
│  │  │ Vault   │ │         │ │         │            │ │          │
│  │  │ Hub     │ │         │ │         │            │ │          │
│  │  │ ESG     │ │         │ │         │            │ │          │
│  │  └────┬────┘ └────┬────┘ └────┬────┘            │ │          │
│  │       │           │           │                   │ │          │
│  │  ┌────┴───────────┴───────────┴────┐             │ │          │
│  │  │     Configuration Service       │             │ │          │
│  │  │  (Rules, Fiscal Parameters)     │             │ │          │
│  │  └────────────────┬────────────────┘             │ │          │
│  └───────────────────┼──────────────────────────────┘ │          │
│                      │                                 │          │
│                      ▼                                 ▼          │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │                    LumaDB (:5432 / :8080)                 │    │
│  │                                                           │    │
│  │  ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐  │    │
│  │  │ document_    │ │ staging_     │ │ system_events    │  │    │
│  │  │ storage      │ │ area         │ │ (event stream)   │  │    │
│  │  │ (BYTEA)      │ │ (TEXT)       │ │ (JSONB)          │  │    │
│  │  └──────────────┘ └──────────────┘ └──────────────────┘  │    │
│  └──────────────────────────────────────────────────────────┘    │
│                                                                   │
│  ┌─────────────────────┐  ┌───────────────────────────────┐      │
│  │ Stream Processor    │  │ Evidence Vault (Filesystem)   │      │
│  │ (LumaDB Poll Loop) │  │ ./vault_storage/              │      │
│  │ telecom.cdr         │  │   ├── whistleblowing/2025/   │      │
│  │ banking.tx           │  │   ├── related-party/2025/   │      │
│  └─────────────────────┘  │   └── ledger.json            │      │
│                           └───────────────────────────────┘      │
└──────────────────────────────────────────────────────────────────┘
```

### 1.2 Architecture Style
The system follows a **modular monolith** pattern where all regulatory modules
are deployed within a single FastAPI process but are logically separated into
independent packages under `src/modules/`. Each module has its own:
- `api.py` -- FastAPI router with endpoint definitions
- `services.py` -- Business logic and calculation engines
- Pydantic models for request/response validation

Cross-cutting concerns (configuration, storage, notifications) are shared
services consumed by all modules.

---

## 2. Component Architecture

### 2.1 Backend Components

#### 2.1.1 NCC Module (`src/modules/ncc/`)

**Compliance Report Generator** (`compliance_report_generator/`)
- `api.py` -- FastAPI app with `/reports/generate` and `/reports/{id}/sign`
- `services.py` -- Board attendance parser, Principle 12 summarizer, deadline
  checker, signature verifier
- `pdf_renderer.py` -- Jinja2 + WeasyPrint HTML-to-PDF pipeline
- `storage_notifications.py` -- LumaDB document storage and email/Slack notifiers

**Financial Sustainability** (`financial_sustainability/`)
- `api.py` -- Router for AOL, ESG, and debt monitoring endpoints
- `services.py` -- AOL calculation engine, ESG metric tracker, debt flagging

**Regulatory Officer Workflow** (`regulatory_officer_workflow/`)
- `api.py` -- Router for Collection Hub, Evidence Vault, Board Advisory
- `hub_service.py` -- Multi-department data request workflow (PENDING -> REVIEW -> APPROVED)
- `vault_service.py` -- SHA-256 hashed immutable document storage with ledger
- `advisory_service.py` -- QoS metric evaluation against dynamic regulatory rules

#### 2.1.2 FCC Module (`src/modules/fcc/`)
- `api.py` -- Router for Form 477, Form 499, CPNI endpoints
- `services.py` -- Broadband aggregation, USF calculation, CPNI certification

#### 2.1.3 CBN Module (`src/modules/cbn/`)
- `api.py` -- Router for AML monitoring, cybersecurity levy, capital adequacy
- `services.py` -- Transaction threshold checker, levy calculator, CAR engine

#### 2.1.4 Configuration Service (`src/modules/configuration/`)
- `models.py` -- RegulatoryRule and FiscalParameter Pydantic models
- `service.py` -- In-memory rule store with jurisdiction/metric lookup

#### 2.1.5 GRC Adapter (`src/grc_adapter/`)
- `api.py` -- Generic webhook router that dispatches to internal services

#### 2.1.6 Ingestion Layer (`src/ingestion_layer/`)
- `file_watcher.py` -- Watchdog observer monitoring staging directory
- `stream_processor.py` -- LumaDB-based event stream with subscriber pattern

### 2.2 Frontend Components

#### 2.2.1 Web Dashboard (`frontend/`)
- **Framework:** Next.js with App Router
- **Page:** Single dashboard page (`app/page.tsx`) displaying NCC, FCC, CBN cards
- **Design System:** CSS variables with glassmorphism (backdrop-filter, blur,
  semi-transparent backgrounds)
- **Layout:** Responsive grid with `grid-template-columns: repeat(auto-fit, minmax(300px, 1fr))`

#### 2.2.2 Mobile Application (`mobile/`)
- **Framework:** React Native with React Navigation (Stack Navigator)
- **Screens:** Login, Dashboard, Settings
- **State:** AuthContext (React Context API) for authentication state
- **Theme:** Centralized design tokens (colors, gradients, spacing)

---

## 3. Data Architecture

### 3.1 Data Flow Patterns

**Pattern 1: Synchronous Request-Response**
```
Client -> FastAPI Router -> Service Layer -> Pydantic Response
```
Used by: AOL calculation, AML monitoring, Form 477 aggregation, QoS evaluation

**Pattern 2: Asynchronous Background Processing**
```
Client -> FastAPI Router -> BackgroundTasks -> PDF Generation -> Storage -> Notification
```
Used by: Compliance Report Generation

**Pattern 3: File-Based Ingestion**
```
File Drop -> Watchdog Observer -> JSON Validation -> LumaDB staging_area
```
Used by: File Watcher ingestion from external systems

**Pattern 4: Event-Driven Processing**
```
Producer -> LumaDB system_events (INSERT) -> Consumer Loop (SELECT + UPDATE)
```
Used by: Stream Processor for CDR and banking transaction handling

**Pattern 5: Webhook Integration**
```
Eramba GRC -> /grc-adapter/webhook -> Event Router -> Internal Service -> GRCResponse
```
Used by: GRC Adapter middleware

### 3.2 Storage Architecture

| Storage Type | Implementation | Use Case |
|-------------|---------------|----------|
| Relational (SQL) | LumaDB via psycopg2 | Document metadata, event stream, staging |
| Binary Object (BLOB) | LumaDB document_storage table | Generated PDFs, uploaded files |
| Immutable Filesystem | vault_storage/ with chmod 0o444 | Whistleblowing evidence, related-party docs |
| In-Memory | Python dicts (SIGNATURE_STORE, ESG_STORE) | Prototype-phase volatile state |

### 3.3 Data Integrity

The Evidence Vault implements a chain-of-custody pattern:
1. **Hashing:** SHA-256 digest computed on file upload
2. **Write-Once:** Duplicate path detection prevents overwriting
3. **Permission Lock:** `chmod 0o444` makes stored files read-only
4. **Ledger:** JSON append-only ledger records timestamp, category, hash, path, metadata
5. **Verification:** Hash comparison enables tamper detection

---

## 4. Integration Architecture

### 4.1 GRC Integration (Eramba)
The `/grc-adapter/webhook` endpoint provides a generic entry point for external
GRC tools. It accepts a `GRCWebhook` payload containing:
- `event_id`: Unique correlation identifier
- `event_type`: Routing key (CALCULATE_AOL, CHECK_AML, CALCULATE_USF)
- `payload`: Generic dictionary mapped to internal Pydantic models
- `callback_url`: Optional URL for async result delivery

### 4.2 Database Integration (LumaDB)
LumaDB exposes a PostgreSQL wire protocol on port 5432, allowing standard
`psycopg2` connections with the connection string:
```
postgresql://lumadb:lumadb@lumadb:5432/default
```

### 4.3 Notification Integration
- **Email:** Mock implementation in `NotificationService.send_email()`
- **Slack:** Mock implementation in `NotificationService.send_slack_alert()`
- **Push Notifications:** Not yet implemented for mobile

---

## 5. Deployment Architecture

### 5.1 Development Stack (docker-compose.yml)

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│   regtech_web   │  │   regtech_api   │  │ regtech_lumadb  │
│   :3000         │──│   :8000         │──│   :5432/:8080   │
│   Next.js       │  │   FastAPI       │  │   LumaDB        │
└─────────────────┘  └─────────────────┘  └─────────────────┘
```

### 5.2 Production Stack (docker-compose.prod.yml)
- gunicorn with 4 Uvicorn workers on API
- Web exposed on port 80
- Network isolation via `regtech_net` bridge network
- `restart: always` for all services
- Volume persistence for LumaDB data and WAL

### 5.3 Port Mapping

| Service | Dev Port | Prod Port | Protocol |
|---------|----------|-----------|----------|
| Web Dashboard | 3000 | 80 | HTTP |
| Backend API | 8000 | 8000 | HTTP |
| LumaDB SQL | 5432 | 5432 | PostgreSQL |
| LumaDB HTTP | 8080 | 8080 | HTTP |
| LumaDB Metrics | 9090 | 9090 | Prometheus |

---

## 6. Security Architecture

### 6.1 Current Implementation
- Pydantic input validation on all API endpoints
- Role-based signature verification (Chairman, CEO, RegulatoryOfficer)
- Immutable evidence storage with integrity hashing
- No network-level TLS (handled by reverse proxy in production)

### 6.2 Planned Enhancements
- JWT authentication with refresh tokens
- RBAC middleware on all protected endpoints
- API rate limiting (100 req/min per client)
- CORS configuration for frontend origins
- Secrets management (environment-based, no hardcoded credentials)
- TLS termination at load balancer

---

## 7. Monitoring and Observability

### 7.1 Current State
- Docker HEALTHCHECK on API (curl to /health) and LumaDB (curl to :8080/health)
- Console logging via print() statements
- LumaDB Prometheus metrics on port 9090

### 7.2 Target State
- Structured JSON logging with correlation IDs
- Prometheus metrics for request latency, error rates, queue depth
- Grafana dashboards for compliance KPIs
- OpenTelemetry distributed tracing
- Alerting via PagerDuty/Opsgenie for QoS breaches

---

## 8. Technology Decision Records

### TDR-001: LumaDB as Unified Data Layer
- **Decision:** Replace PostgreSQL + Redis + Kafka with LumaDB
- **Rationale:** Single service providing SQL interface, event storage, and BLOB
  storage reduces operational complexity
- **Trade-off:** Less mature ecosystem, potential compatibility issues
- **Fallback:** psycopg2 connection string can point to standard PostgreSQL

### TDR-002: Modular Monolith over Microservices
- **Decision:** Deploy all modules in single FastAPI process
- **Rationale:** Team size (< 5 engineers), shared data layer, simpler deployment
- **Trade-off:** Cannot scale modules independently
- **Migration Path:** Extract to microservices when team exceeds 10 engineers

### TDR-003: WeasyPrint for PDF Generation
- **Decision:** Use WeasyPrint + Jinja2 for report rendering
- **Rationale:** Full CSS support, HTML template reuse, Python-native
- **Trade-off:** Heavy system dependencies (cairo, pango, gdk-pixbuf)
- **Alternative Considered:** wkhtmltopdf (harder to containerize), Puppeteer

### TDR-004: Glassmorphism Design System
- **Decision:** Premium dark theme with glassmorphism UI patterns
- **Rationale:** Modern executive-grade appearance, differentiation from
  traditional compliance tools
- **Implementation:** CSS `backdrop-filter: blur(12px)` with semi-transparent
  backgrounds and gradient accents
