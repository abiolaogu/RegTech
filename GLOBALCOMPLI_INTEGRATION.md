# GlobalCompli Integration

This RegTech Horizon platform has been integrated into **GlobalCompli** to create a unified cross-border compliance orchestration platform.

## Integration Details

The following modules from RegTech Horizon have been integrated into GlobalCompli:

| Module | Endpoint Prefix | Description |
|:-------|:----------------|:------------|
| NCC (Nigeria Telecom) | `/api/v1/ncc/*` | AOL, QoS, Section A-F Reports |
| FCC (USA Telecom) | `/api/v1/fcc/*` | Form 477, Form 499, CPNI |
| CBN (Nigeria FinTech) | `/api/v1/cbn/*` | AML/CFT, Cyber Levy, CAR |

## Unified Platform Features

GlobalCompli combines RegTech Horizon's regional compliance modules with:
- **GDPR** (EU Data Protection)
- **CCPA** (California Privacy)
- **SOC 2** (Security Controls)
- **HIPAA** (Healthcare)
- **AML** (Anti-Money Laundering - Global)

## Access the Unified Platform

- **Repository**: [GlobalCompli](https://github.com/abiolaogu/GlobalCompli)
- **API Docs**: http://localhost:8000/docs
- **Dashboard**: http://localhost:3000

## What Was Migrated

### Backend Modules
- `src/modules/ncc/` → `GlobalCompli/backend/modules/ncc/`
- `src/modules/fcc/` → `GlobalCompli/backend/modules/fcc/`
- `src/modules/cbn/` → `GlobalCompli/backend/modules/cbn/`

### Frontend
- RegTech's glassmorphism UI extended with GDPR, CCPA, SOC2 modules
- Unified navigation across all 8 jurisdictions
- Real-time compliance stream display

## Running the Unified Platform

```bash
# Clone GlobalCompli
git clone https://github.com/abiolaogu/GlobalCompli.git
cd GlobalCompli

# Start backend
cd backend && pip install -r requirements.txt
uvicorn main:app --reload

# Start frontend
cd frontend && npm install && npm run dev
```
