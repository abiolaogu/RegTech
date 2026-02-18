# RegTech Horizon: Technical Specifications

## 1. System Components
### 1.1 Backend Service
- **Language**: Python 3.11
- **Framework**: FastAPI (asyncio) for high-concurrency API performance.
- **Validation**: Pydantic V2 modules for strict type checking.
- **Streaming**: `FastStream` (Kafka wrapper) for event processing.

### 1.2 Frontend Application
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS + CSS Modules (Glassmorphism design system).
- **State Management**: React Query (TanStack) for server state.

## 2. Database Schema (LumaDB)
### 2.1 Core Tables
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255), -- MD5 (Legacy LumaDB requirement)
    role VARCHAR(20) -- 'admin', 'officer', 'monitor'
);

CREATE TABLE regulatory_reports (
    report_id UUID PRIMARY KEY,
    jurisdiction VARCHAR(10), -- 'NCC', 'FCC', 'CBN'
    status VARCHAR(20), -- 'DRAFT', 'SUBMITTED', 'REJECTED'
    generated_at TIMESTAMP,
    data JSONB -- Full report payload
);

CREATE TABLE system_events (
    event_id UUID PRIMARY KEY,
    event_type VARCHAR(50), -- 'INGESTION', 'ALERT', 'LOGIN'
    payroll JSONB,
    timestamp TIMESTAMP DEFAULT NOW()
);
```

## 3. API Specification
### 3.1 Authentication
- `POST /auth/token`: Exchange credentials for JWT Access Token.

### 3.2 Reporting
- `POST /api/v1/generator/ncc`: Trigger NCC report generation.
  - **Input**: `{ "quarter": "Q3-2025", "files": ["revenue.csv", "qos.json"] }`
  - **Output**: `{ "report_id": "...", "status": "processing" }`

### 3.3 AIOps
- `GET /api/v1/aiops/alerts`: Fetch active system alerts.
- `POST /api/v1/ingest/webhook`: Webhook endpoint for external data sources.

## 4. Algorithms
### 4.1 "Three-Cs" Validation Logic
1.  **Completeness Check**: Iterate all keys in `schema.required`. If `key not in data`, flag error.
2.  **Correctness Check**: Execute Python `eval()` rules safely. E.g., `revenue > 0`.
3.  **Consistency Check**:
    ```python
    def check_consistency(report_a, report_b):
        diff = abs(report_a.total_subscribers - report_b.total_subscribers)
        if diff > threshold:
            raise ConsistencyError("Subscriber count mismatch")
    ```

### 4.2 Anomaly Detection (Z-Score)
- Calculate moving average ($μ$) and standard deviation ($σ$) of last 30 days.
- If current value ($x$) satisfies $|x - μ| > 3σ$, trigger critical alert.
