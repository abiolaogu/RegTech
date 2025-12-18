# RegTech Horizon: Operations Manual

## 1. Deployment Guide
### 1.1 Infrastructure Requirements
- **Hardware**: 4x vCPU, 16GB RAM (Minimum for Production).
- **OS**: Linux (Ubuntu 22.04 LTS recommended).
- **Dependencies**: Docker 24.0+, Docker Compose v2.

### 1.2 Production Deployment
1.  **Clone Repository**:
    ```bash
    git clone https://github.com/abiolaogu/RegTech.git
    cd RegTech
    ```
2.  **Environment Configuration**:
    - Copy `.env.example` to `.env`.
    - Set `LUMADB_USER`, `LUMADB_PASSWORD` (MD5 hashed), and `JWT_SECRET`.
3.  **Start Services**:
    ```bash
    docker-compose -f docker-compose.prod.yml up -d
    ```
4.  **Verify Health**:
    - Check API: `curl http://localhost:8000/health` -> `{"status": "ok"}`
    - Check LumaDB: `docker exec regtech-lumadb-1 luma-cli ping`

## 2. Monitoring & AIOps
### 2.1 Prometheus Metrics
The platform exposes metrics at `/metrics`. Key indicators:
- `http_requests_total`: Rate of API calls.
- `report_generation_duration_seconds`: Time to generate PDF.
- `ingestion_lag`: Delay in processing file uploads.

### 2.2 Dashboard Alerts
- **Red Alert (Critical)**: Service downtime or compliance breach (e.g., "NCC QoS below 98%").
- **Yellow Alert (Warning)**: Data latency > 5 mins.
- **Blue Alert (Info)**: Successful report submission.

## 3. Maintenance Procedures
### 3.1 Database Backups
LumaDB snapshots occur daily at 02:00 UTC.
- **Manual Backup**:
  ```bash
  docker exec lumadb sh -c "luma-dump > /backups/dump_$(date +%F).sql"
  ```
- **Restore**:
  ```bash
  cat dump.sql | docker exec -i lumadb luma-restore
  ```

### 3.2 Log Rotation
Logs are stored in `/var/log/regtech/`. Retention policy is 30 days.
- Access Logic Engine logs: `docker logs regtech-api-1`
- Access Ingestion logs: `docker logs regtech-watchdog-1`

## 4. Troubleshooting
### 4.1 "Worker Timeout" Error
- **Cause**: Generating massive PDF reports (1000+ pages).
- **Fix**: Increase Gunicorn timeout in `docker-compose.yml`:
  ```yaml
  command: gunicorn -k uvicorn.workers.UvicornWorker --timeout 120
  ```

### 4.2 "LumaDB Connection Refused"
- **Check**: Ensure container is running.
- **Check**: Verify MD5 password hash in `.env` matches database user.
