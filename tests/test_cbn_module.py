from fastapi.testclient import TestClient
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modules.cbn.api import router
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_aml_monitor():
    txs = [
        {"id": "t1", "amount": 6_000_000, "sender_id": "INDIVIDUAL_JOHN", "recipient_id": "ALICE", "timestamp": "2025-01-01", "type": "TRANSFER"}, # > 5M -> CTR
        {"id": "t2", "amount": 9_999_999, "sender_id": "INDIVIDUAL_DOE", "recipient_id": "BOB", "timestamp": "2025-01-01", "type": "TRANSFER"}, # STR (Structuring) + CTR? No, >5M
        {"id": "t3", "amount": 4_000_000, "sender_id": "INDIVIDUAL_JANE", "recipient_id": "CHARLIE", "timestamp": "2025-01-01", "type": "TRANSFER"} # OK
    ]
    
    resp = client.post("/cbn/aml/monitor", json=txs)
    assert resp.status_code == 200
    flags = resp.json()
    
    ids = [f["tx_id"] for f in flags]
    assert "t1" in ids # CTR
    assert "t2" in ids # STR or CTR
    assert "t3" not in ids

def test_cyber_levy():
    # 0.005% of 1,000,000 = 50
    resp = client.post("/cbn/levy/cybersecurity?amount=1000000")
    assert resp.status_code == 200
    data = resp.json()
    assert data["levy_payable"] == 50.0

def test_capital_adequacy():
    # 1B Funds, 10B Assets -> 10%
    # Min 10% -> Compliant
    resp = client.get("/cbn/capital-adequacy/check?shareholders_funds=1000000000&risk_weighted_assets=10000000000&license_type=REGIONAL")
    assert resp.status_code == 200
    assert resp.json()["status"] == "COMPLIANT"
    
    # Min 15% -> Breach
    resp = client.get("/cbn/capital-adequacy/check?shareholders_funds=1000000000&risk_weighted_assets=10000000000&license_type=NATIONAL")
    assert resp.status_code == 200
    assert resp.json()["status"] == "BREACH"
