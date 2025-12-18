# AIOps User Manual

## Overview
The AIOps system provides automated detection, correlation, and remediation of incidents across the RegTech platform.

## Getting Started
1. **Access** – Log in to the RegTech portal and navigate to **Operations → AIOps**.
2. **Dashboard** – The main dashboard shows real‑time alerts, health metrics, and suggested actions.

## Daily Workflow
- **Review Alerts** – Inspect high‑severity alerts, confirm auto‑remediation actions, or manually intervene.
- **Validate Remediations** – After a remediation script runs, verify the issue is resolved via the dashboard.
- **Tune Rules** – Adjust thresholds or add new remediation scripts in the **Settings** tab.

## Roles & Permissions
| Role | Permissions |
|------|-------------|
| Operator | View alerts, approve remediations, edit rules |
| Engineer | Create/modify remediation scripts, access logs |
| Admin | Full access, manage integrations |

## Troubleshooting
- **No alerts** – Ensure data sources (Prometheus, LumaDB) are reachable.
- **Remediation failed** – Check `/var/log/aioops.log` and script exit codes.
- **Performance issues** – Review resource usage in the **Metrics** tab.

---
*This is a placeholder; detailed step‑by‑step procedures will be added.*
