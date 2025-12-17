from fastapi.testclient import TestClient
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from grc_adapter.api import router
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_aol_routing():
    # Eramba sends generic JSON
    payload = {
        "event_id": "evt_1",
        "event_type": "CALCULATE_AOL",
        "payload": {
            "gross": 100,
            "interconnect": 10,
            "roaming": 0
        }
    }
    # Expected: (100 - 10) * 1% = 0.9
    resp = client.post("/grc-adapter/webhook", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "success"
    assert data["result"]["levy_payable"] == 0.9

def test_usf_routing():
    payload = {
        "event_id": "evt_2",
        "event_type": "CALCULATE_USF",
        "payload": {
            "interstate": 1000,
            "international": 0
            # others default to 0
        }
    }
    # Expected: 1000 * 0.346 = 346.0
    resp = client.post("/grc-adapter/webhook", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["result"]["usf_contribution"] == 346.0

def test_aml_routing():
    payload = {
        "event_id": "evt_3",
        "event_type": "CHECK_AML",
        "payload": {
            "transactions": [
                {"id": "t1", "amount": 6_000_000, "sender_id": "INDIVIDUAL", "recipient_id": "B", "timestamp": "2025", "type": "T"}
            ]
        }
    }
    resp = client.post("/grc-adapter/webhook", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    flags = data["result"]["flags"]
    assert len(flags) == 1
    assert flags[0]["tx_id"] == "t1"
