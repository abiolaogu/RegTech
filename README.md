# RegTech Horizon Platform

**RegTech Horizon** is a Multi-Jurisdictional, High-Performance Regulatory Technology platform designed to automate compliance for Telecommunications and FinTech industries in Nigeria (NCC, CBN) and the United States (FCC).

## 🚀 Features
- **Multi-Jurisdictional Intelligence**:
    - **NCC (Nigeria Telecom)**: Section A-F Report Generator, AOL Calculation, QoS Monitoring.
    - **FCC (USA Telecom)**: Form 477 Aggregation, USF Contribution, CPNI Audits.
    - **CBN (Nigeria FinTech)**: AML/CFT Transaction Monitoring, Cybersecurity Levy, Capital Adequacy.
- **Microservices Architecture**:
    - Modular Python Engines (`src/modules/*`).
    - GRC Integration Middleware (`src/grc_adapter`).
    - High-Performance Stream Ingestion (`src/ingestion_layer`).
- **Modern Interface**:
    - Next.js Dashboard with Premium Glassmorphism UI.
    - React Native Mobile App for on-the-go alerts.
- **Enterprise Ready**:
    - Dockerized Container Stack (API, Web, Postgres, Redpanda, S3).
    - Event-Driven Architecture (Kafka/FastStream).

## 🛠️ Tech Stack
- **Backend**: Python 3.11, FastAPI, Pydantic, FastStream.
- **Frontend**: Next.js 14, TypeScript, CSS Modules (Glassmorphism).
- **Mobile**: React Native (Expo).
- **Infrastructure**: Docker Compose, PostgreSQL, Redpanda (Kafka), MinIO (S3).

## 📚 Documentation
- **[Architecture Specification](docs/Architecture_Specification.md)**: System design and data flow.
- **[Product Requirements (PRD)](docs/Product_Requirements_Document.md)**: User personas and functional goals.
- **[Technical Specifications](docs/Technical_Specifications.md)**: API, Schema, and Algorithms.
- **[Operations Manual](docs/Operations_Manual.md)**: Deployment and AIOps monitoring.
- **[User Manual](docs/User_Manual.md)**: Guides for Web Dashboard and Mobile App.
- **[Developer Onboarding](docs/Training_Manual_Onboarding.md)**: Setup guide for new engineers.
- **[Video Training Scripts](docs/Video_Training_Scripts_Detailed.md)**: Content for video tutorials.

## 📦 Deployment

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.9+ (for local backend dev)

### Quick Start (Docker)
Run the full stack:
```bash
docker-compose up --build
```
Access the services:
- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **MinIO Console**: http://localhost:9001
- **Redpanda Console**: localhost:9644

### Local Development
**Backend**:
```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

**Frontend**:
```bash
cd frontend
npm install
npm run dev
```

## 🧪 Testing
Run the test suite:
```bash
python -m pytest tests/
```

## 📱 Mobile App
The mobile app source is in `mobile/`.
```bash
cd mobile
npm install
npm start
```

## 🔒 Security
- **Data Protection**: All sensitive reports are stored in WORM-compliant storage (Vault Service).
- **Audit**: Immutable logs for all Regulatory Officer actions.

---
© 2025 RegTech Horizon. All Rights Reserved.