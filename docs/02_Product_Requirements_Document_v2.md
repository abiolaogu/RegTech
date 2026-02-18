# RegTech Horizon -- Product Requirements Document v2

## Document Control

| Field | Value |
|-------|-------|
| Document ID | RT-PRD-002 |
| Version | 2.0 |
| Status | Draft |
| Last Updated | 2026-02-17 |

---

## 1. Product Vision

RegTech Horizon automates multi-jurisdictional regulatory compliance for
telecommunications and fintech operators. The platform replaces manual
spreadsheet-based compliance workflows with an intelligent, event-driven system
that calculates levies, monitors transactions, generates regulatory reports,
and maintains immutable audit trails.

---

## 2. User Personas

### 2.1 Regulatory Officer (Primary User)
- **Name:** Adaeze, Regulatory Compliance Manager
- **Organization:** Nigerian telecom operator (dual-licensed NCC/CBN)
- **Goals:** Generate NCC Section A-F reports on time, calculate AOL levy
  accurately, monitor QoS breaches, coordinate data collection across
  departments
- **Pain Points:** Manual data aggregation from Finance/HR/Legal takes 2 weeks,
  deadline tracking is error-prone, no single view of compliance status
- **Key Workflows:**
  - Create data collection requests via Collection Hub
  - Review submitted artifacts from departments
  - Generate and sign compliance reports
  - Upload evidence to immutable vault
  - Monitor QoS breach alerts

### 2.2 Chief Compliance Officer (Executive User)
- **Name:** David, Group CCO
- **Organization:** Multinational telecom with Nigeria and US operations
- **Goals:** 360-degree compliance visibility, board-ready reports, risk
  mitigation across jurisdictions
- **Pain Points:** Cannot see real-time compliance status, relies on monthly
  email updates from country teams, no mobile access
- **Key Workflows:**
  - View compliance dashboard on web and mobile
  - Sign-off on reports (Section F digital signature)
  - Review AML flags escalated by CBN module
  - Track filing deadlines across NCC, FCC, CBN

### 2.3 Financial Analyst (Data Provider)
- **Name:** Chinwe, Senior Financial Analyst
- **Organization:** Finance department of telecom operator
- **Goals:** Provide accurate revenue data for AOL calculation, track outstanding
  debts, manage ESG metrics
- **Pain Points:** Multiple manual exports from SAP to different compliance
  spreadsheets, version control issues
- **Key Workflows:**
  - Submit revenue breakdowns (gross, interconnect, roaming costs)
  - Upload debt settlement records
  - Log ESG metrics (renewable energy sites, diversity numbers)

### 2.4 IT/GRC Administrator
- **Name:** Olumide, GRC Platform Admin
- **Organization:** IT department managing Eramba GRC tool
- **Goals:** Integrate RegTech Horizon with existing GRC tooling, automate
  compliance calculations
- **Pain Points:** Manual data transfer between Eramba and custom spreadsheets
- **Key Workflows:**
  - Configure GRC adapter webhooks
  - Route AOL, AML, USF calculations through /grc-adapter/webhook
  - Monitor integration health

---

## 3. Functional Requirements

### 3.1 NCC Nigeria Telecom Module

#### FR-NCC-001: Compliance Report Generation
- **Description:** Generate NCC Section A-F compliance reports with dynamic data
- **Endpoint:** `POST /reports/generate`
- **Input:** Company name, reporting period, board log path, consultant report
  path, submission type (mid-year/annual)
- **Processing:**
  - Validate submission deadline (July 31 mid-year, January 31 annual)
  - Fetch board attendance from secretariat logs
  - Generate Principle 12 summary from consultant report
  - Build Sections A through F with dynamic content
  - Render HTML template to PDF via WeasyPrint
  - Upload PDF to document storage (LumaDB BLOB or local)
  - Send email notification to compliance team
- **Output:** Report ID, processing status, section previews

#### FR-NCC-002: Digital Signature
- **Description:** Record authorized digital signatures on compliance reports
- **Endpoint:** `POST /reports/{report_id}/sign`
- **Authorized Roles:** Chairman, CEO, RegulatoryOfficer
- **Validation:** Role verification before accepting signature
- **Storage:** Signature data with timestamp in persistent store

#### FR-NCC-003: Annual Operating Levy (AOL) Calculation
- **Description:** Calculate NCC AOL based on assessable income
- **Endpoint:** `POST /finance/aol/calculate`
- **Formula:** `Levy = levy_percent * (Gross Revenue - Interconnect - Roaming)`
- **Default Rate:** 1% (configurable via ConfigurationService)
- **Example:** N60B gross, N14.8B deductions = N45.2B assessable, N452M levy

#### FR-NCC-004: Quality of Service (QoS) Monitoring
- **Description:** Real-time evaluation of QoS metrics against NCC thresholds
- **Endpoint:** `POST /regulatory-officer/advisory/qos-event`
- **Rules (from ConfigurationService):**
  - NCC-001: Drop Call Rate must be < 1% (breach if > 1.0)
  - NCC-002: Call Setup Success Rate must be >= 98% (breach if < 98.0)
  - NCC-003: Internet Latency must be < 100ms (breach if > 100.0)
- **On Breach:** Generate remediation report with CRITICAL status

#### FR-NCC-005: Collection Hub Workflow
- **Description:** Multi-department data collection and review workflow
- **Endpoints:**
  - `POST /regulatory-officer/hub/requests` -- create data request
  - `GET /regulatory-officer/hub/requests` -- list requests (filterable by status)
  - `POST /regulatory-officer/hub/requests/{id}/submit` -- upload artifact
  - `POST /regulatory-officer/hub/requests/{id}/review` -- approve/reject
- **Status Flow:** PENDING -> REVIEW -> APPROVED/REJECTED

#### FR-NCC-006: Evidence Vault
- **Description:** Immutable document storage with SHA-256 hashing
- **Endpoint:** `POST /regulatory-officer/vault/upload`
- **Categories:** whistleblowing, related-party
- **Process:**
  1. Calculate SHA-256 hash of uploaded file
  2. Store in year-partitioned directory structure
  3. Set read-only permissions (chmod 0o444)
  4. Record in tamper-evident ledger (ledger.json)
- **Write-Once:** Duplicate hash detection prevents overwriting

#### FR-NCC-007: ESG Sustainability Tracker
- **Description:** Track and report Environmental, Social, Governance metrics
- **Endpoints:**
  - `POST /sustainability/metrics` -- log a metric
  - `GET /sustainability/metrics` -- retrieve all metrics
- **Categories:** Renewable (solar sites), Diversity (female engineering %)

#### FR-NCC-008: Debt Settlement Monitor
- **Description:** Flag overdue unpaid debts from ERP system
- **Endpoint:** `POST /finance/debt/monitor`
- **Logic:** Flag debts where status != PAID and due_date < today

### 3.2 FCC USA Telecom Module

#### FR-FCC-001: Form 477 Broadband Deployment Aggregation
- **Description:** Aggregate deployment locations by technology type
- **Endpoint:** `POST /fcc/form477/aggregate`
- **Technology Codes:** Fiber (50), Cable (42), DSL (10), Fixed Wireless (70),
  Satellite (60)
- **Output:** Total locations, fiber coverage count, average download speed

#### FR-FCC-002: Form 499 USF Contribution Calculator
- **Description:** Estimate Universal Service Fund contribution
- **Endpoint:** `POST /fcc/form499/calculate`
- **Formula:** `Contribution = (Interstate + International Revenue) * USF Factor`
- **Default Factor:** 0.346 (34.6%, adjustable per quarter)

#### FR-FCC-003: CPNI Annual Compliance Certificate
- **Description:** Generate CPNI audit certification document
- **Endpoint:** `POST /fcc/cpni/certify`
- **Output:** Officer name, certification date, breach list, compliance statement

### 3.3 CBN FinTech Module

#### FR-CBN-001: AML/CFT Transaction Monitoring
- **Description:** Flag transactions exceeding CBN reporting thresholds
- **Endpoint:** `POST /cbn/aml/monitor`
- **Thresholds:**
  - Individual: > N5,000,000 triggers CTR (Currency Transaction Report)
  - Corporate (CORP prefix): > N10,000,000 triggers CTR
  - Structuring detection: exact N9,999,999 triggers STR (Suspicious Transaction Report)

#### FR-CBN-002: Cybersecurity Levy Calculator
- **Description:** Calculate 0.005% cybersecurity levy per Cybersecurity Act 2024
- **Endpoint:** `POST /cbn/levy/cybersecurity`
- **Formula:** `Levy = amount * 0.00005`

#### FR-CBN-003: Capital Adequacy Ratio (CAR) Check
- **Description:** Verify bank capital meets BOFIA 2020 requirements
- **Endpoint:** `GET /cbn/capital-adequacy/check`
- **Formula:** `CAR = Shareholders Funds / Risk Weighted Assets`
- **Thresholds:** Regional 10%, National 15%
- **Output:** CAR percentage, required percentage, COMPLIANT/BREACH status

### 3.4 GRC Integration Module

#### FR-GRC-001: Webhook Router
- **Description:** Accept generic GRC tool webhooks and route to internal engines
- **Endpoint:** `POST /grc-adapter/webhook`
- **Supported Events:**
  - CALCULATE_AOL -> NCC AOL engine
  - CHECK_AML -> CBN AML monitor
  - CALCULATE_USF -> FCC USF calculator
- **Response:** Standardized GRCResponse with status and result payload

### 3.5 Ingestion Layer

#### FR-ING-001: File Watcher
- **Description:** Monitor staging directory for new files, validate, ingest
- **Process:** Detect file creation -> validate JSON -> insert into LumaDB
  staging_area table -> move to processed directory
- **Configuration:** INGEST_DIR and PROCESSED_DIR environment variables

#### FR-ING-002: Stream Processor
- **Description:** Event-driven processing via LumaDB system_events table
- **Topics:** telecom.cdr (call detail records), banking.tx (financial transactions)
- **Processing:** Poll unprocessed events, execute registered handlers, mark processed

---

## 4. Non-Functional Requirements

### 4.1 Performance
- API response time < 200ms for calculation endpoints (p95)
- PDF generation < 10 seconds for standard compliance report
- AML monitoring batch of 1000 transactions < 5 seconds
- Form 477 aggregation of 10,000 locations < 3 seconds

### 4.2 Availability
- Target: 99.5% uptime for API services
- Docker health checks with 30s interval, 3 retries
- Production mode: gunicorn with 4 workers behind Uvicorn

### 4.3 Security
- All regulatory reports stored with SHA-256 integrity hashes
- Evidence vault with write-once semantics
- Digital signatures recorded with timestamp and role verification
- Authorized signer roles: Chairman, CEO, RegulatoryOfficer

### 4.4 Scalability
- Modular architecture supports adding new jurisdictions as separate modules
- LumaDB scales horizontally with Raft consensus (future)
- Docker Compose supports multi-replica deployment

### 4.5 Compliance
- Immutable audit ledger for all vault operations
- Report generation tracked with unique UUIDs
- Configurable regulatory rules via ConfigurationService
- Deadline enforcement for NCC submissions

---

## 5. Data Models

### 5.1 Core Pydantic Models

```python
# NCC Compliance
class SectionContent(BaseModel):
    title: str
    content: str
    evidences: Optional[List[str]] = None

class ComplianceRequest(BaseModel):
    id: str
    type: str          # "Cooling-Off Check", "AOL Data"
    department: str    # HR, Finance, Legal
    status: str        # PENDING, REVIEW, APPROVED, REJECTED
    artifacts: List[str] = []
    created_at: str
    updated_at: str

# NCC Financial
class AOLInput(BaseModel):
    gross_revenue: float
    interconnect_costs: float
    roaming_costs: float

class ESGMetric(BaseModel):
    id: str
    category: str      # "Renewable" or "Diversity"
    name: str
    value: float
    unit: str          # "%", "Count"
    timestamp: str

# Configuration
class RegulatoryRule(BaseModel):
    rule_id: str
    jurisdiction: str  # "NCC", "FCC", "CBN"
    metric: str
    threshold: float
    operator: str      # "GT", "LT"
    enabled: bool = True

class FiscalParameter(BaseModel):
    param_id: str
    jurisdiction: str
    key: str           # "AOL_LEVY_PERCENT"
    value: float
    effective_date: date
```

### 5.2 LumaDB Tables

| Table | Columns | Purpose |
|-------|---------|---------|
| document_storage | id TEXT PK, filename TEXT, content BYTEA, created_at TIMESTAMP | Binary document storage |
| staging_area | id SERIAL PK, filename TEXT, content TEXT, ingested_at TIMESTAMP | File watcher ingestion |
| system_events | id SERIAL PK, topic TEXT, payload JSONB, processed BOOLEAN, created_at TIMESTAMP | Event stream |

---

## 6. Acceptance Criteria

### 6.1 NCC Module
- [x] AOL calculation matches N452M for N60B gross / N14.8B deductions
- [x] Report generates all 6 sections (A-F) with dynamic content
- [x] Deadline trigger returns false for invalid submit_type
- [x] Signature roles validated (Chairman, CEO, RegulatoryOfficer only)
- [x] QoS breach detected when DropCallRate > 1.0%
- [x] Vault stores file with SHA-256 hash and read-only permissions

### 6.2 FCC Module
- [x] Form 477 correctly counts fiber locations (technology code "50")
- [x] USF contribution = $51,900 for $150K assessable at 34.6% factor
- [x] CPNI certificate includes officer name and certification date

### 6.3 CBN Module
- [x] Individual CTR flagged for transactions > N5M
- [x] Corporate CTR flagged for transactions > N10M
- [x] Cybersecurity levy = N50 on N1M transaction
- [x] CAR COMPLIANT at 10% for Regional, BREACH at 15% for National

### 6.4 GRC Adapter
- [x] CALCULATE_AOL webhook returns levy_payable = 0.9 for (100-10)*1%
- [x] CALCULATE_USF webhook returns 346.0 for 1000 interstate at 34.6%
- [x] CHECK_AML webhook returns flag for N6M individual transaction
