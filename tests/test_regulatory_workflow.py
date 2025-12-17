from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import os
import sys
import pytest

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modules.ncc.regulatory_officer_workflow.api import router, hub_service, vault_service, advisory_service
# We need an app to mount the router
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

client = TestClient(app)

# --- Hub Tests ---
def test_create_and_list_request():
    # 1. Create
    resp = client.post("/regulatory-officer/hub/requests", json={"type": "HR Data", "department": "HR"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["type"] == "HR Data"
    req_id = data["id"]
    assert data["status"] == "PENDING"

    # 2. List
    resp = client.get("/regulatory-officer/hub/requests")
    assert resp.status_code == 200
    all_reqs = resp.json()
    assert any(r["id"] == req_id for r in all_reqs)

def test_hub_workflow():
    # Create
    resp = client.post("/regulatory-officer/hub/requests", json={"type": "Finance Data", "department": "Finance"})
    req_id = resp.json()["id"]

    # Submit Artifact (Mock file)
    with open("test_artifact.txt", "w") as f:
        f.write("test content")
    
    with open("test_artifact.txt", "rb") as f:
        resp = client.post(f"/regulatory-officer/hub/requests/{req_id}/submit", files={"file": ("test_artifact.txt", f, "text/plain")})
    
    assert resp.status_code == 200
    assert resp.json()["status"] == "REVIEW"
    
    os.remove("test_artifact.txt")

    # Review
    resp = client.post(f"/regulatory-officer/hub/requests/{req_id}/review", json={"approve": True, "comments": "LGTM"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "APPROVED"

# --- Vault Tests ---
def test_vault_upload():
    # Config vault to use a temp dir for tests
    vault_service.base_path = "/tmp/test_vault"
    vault_service._load_ledger() # Reload empty ledger

    with open("secret_doc.txt", "w") as f:
        f.write("confidential")
    
    with open("secret_doc.txt", "rb") as f:
        resp = client.post("/regulatory-officer/vault/upload", 
            data={"category": "whistleblowing", "meta": '{"tag": "urgent"}'},
            files={"file": ("secret_doc.txt", f, "text/plain")}
        )
    
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "stored"
    assert "hash" in data
    
    # Verify file exists
    assert os.path.exists(data["path"])
    
    os.remove("secret_doc.txt")
    shutil.rmtree("/tmp/test_vault")

# --- Advisory Tests ---
import shutil # Re-import for cleanup if needed

def test_qos_breach():
    # No breach
    resp = client.post("/regulatory-officer/advisory/qos-event", json={"metric": "DropCallRate", "value": 0.5})
    assert resp.json()["status"] == "ok"

    # Breach
    resp = client.post("/regulatory-officer/advisory/qos-event", json={"metric": "DropCallRate", "value": 2.5})
    data = resp.json()
    assert data["status"] == "breach_alerted"
    assert data["report"]["title"] == "URGENT: QoS Breach - DropCallRate"
