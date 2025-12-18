# RegTech Horizon: Developer Onboarding & Training Manual

## 1. Introduction
Welcome to the RegTech engineering team! This manual will guide you from "zero to code" in under 2 hours.

## 2. Dev Environment Setup
### 2.1 Prerequisites
- **OS**: MacOS or Linux (Windows via WSL2).
- **Tools**: VS Code, Docker Desktop, Git, Python 3.9+, Node.js 18+.

### 2.2 First-Time Setup
1.  **Clone the Repo**:
    ```bash
    git clone https://github.com/abiolaogu/RegTech.git
    cd RegTech
    ```
2.  **Install Backend Dependencies**:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Install Frontend Dependencies**:
    ```bash
    cd frontend && npm install
    cd ../mobile && npm install
    ```
4.  **Local Infrastructure**:
    ```bash
    docker-compose up -d lumadb
    ```

## 3. Contribution Guidelines
### 3.1 Git Workflow
- **Branching**: Use `feature/feature-name` or `fix/issue-id`.
- **Commits**: Follow Conventional Commits (e.g., `feat: add ncc report generator`).
- **PRs**: Requires 1 approval and passing CI (Lint + Tests).

### 3.2 Code Standards
- **Python**: PEP8. enforced by `ruff`. Type hints required (`mypy`).
- **JavaScript**: Airbnb Style Guide, enforced by `eslint`.
- **Documentation**: All public API endpoints must have docstrings.

## 4. Architecture Deep Dive
- **Event-Driven**: We avoid direct synchronous coupling. Use `FastStream` to publish events to LumaDB streams.
- **Glassmorphism**: UI components live in `frontend/components/ui`. Re-use them! Don't create custom styles unless necessary.

## 5. Resources
- **Jira Board**: [Link]
- **Figma Designs**: [Link]
- **Team API Keys**: Check Vault (Ask team lead for access).
