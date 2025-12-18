# Production Build & Deployment Guide

This guide details how to build the production-ready Docker containers for RegTech Horizon and deploy them.

## 1. Prerequisites
- **Docker Engine**: v24.0 or later.
- **Docker Compose**: v2.0 or later.
- **Network**: Stable internet connection (initial build pulls ~500MB Python 3.11 image).

## 2. Production Services
The production stack is defined in `docker-compose.prod.yml` and consists of:
1.  **`regtech_api_prod`**: FastAPI backend (Python 3.11) served by Gunicorn.
2.  **`regtech_web_prod`**: Next.js frontend (Node 18).
3.  **`regtech_lumadb_prod`**: LumaDB unified data layer.

## 3. Building the Containers
We separate the build step to ensure all images are ready before runtime.

### Step 3.1: Optimize Context (Important)
Ensure the `.dockerignore` file exists in the root. This prevents unrelated files (like `node_modules` or `lumadb_reference`) from being sent to the Docker daemon, significantly speeding up the build.

### Step 3.2: Run the Build Command
Execute the following in your terminal:

```bash
docker-compose -f docker-compose.prod.yml build
```

**Troubleshooting Build Timeouts:**
If the build hangs (e.g., at "Sending build context"), check:
1.  **Context Size**: Run `du -sh .` - it should be < 50MB (excluding `.git`).
2.  **Ignore File**: Confirm `.dockerignore` excludes large directories.
3.  **Verbose Mode**: Run with `--progress=plain` to see where it gets stuck:
    ```bash
    docker-compose -f docker-compose.prod.yml build --progress=plain
    ```

## 4. Deploying to Production
Once built, start the stack in detached mode:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Verification
- **API Health**: `curl http://localhost:8000/health` (Should return HTTP 200).
- **Logs**:
    ```bash
    docker logs -f regtech_api_prod
    ```

## 5. Security Checklist
Before going live:
1.  **Environment Variables**: Ensure `.env` contains strong, unique passwords for `LUMADB_PASSWORD` and `JWT_SECRET`.
2.  **Ports**: `docker-compose.prod.yml` exposes port `8000` (API) and `3000` (Web). Ensure your firewall restricts access or uses a reverse proxy (Nginx) for SSL termination.
