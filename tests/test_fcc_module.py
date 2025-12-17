from fastapi.testclient import TestClient
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modules.fcc.api import router
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_form477_aggregation():
    # 2 Fiber locations, 1 Cable
    payload = [
        {"census_block_id": "001", "technology": "50", "max_download_mbps": 1000, "max_upload_mbps": 1000, "consumer": True, "business": False},
        {"census_block_id": "002", "technology": "50", "max_download_mbps": 900, "max_upload_mbps": 900, "consumer": True, "business": True},
        {"census_block_id": "003", "technology": "42", "max_download_mbps": 500, "max_upload_mbps": 50, "consumer": True, "business": False}
    ]
    
    resp = client.post("/fcc/form477/aggregate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["total_locations"] == 3
    assert data["fiber_coverage"] == 2 # "50" is Fiber
    # Avg down: (1000+900+500)/3 = 800
    assert data["avg_down_mbps"] == 800.0

def test_form499_usf():
    payload = {
        "interstate_revenue": 100_000,
        "international_revenue": 50_000,
        "intrastate_revenue": 200_000,
        "end_user_revenue": 150_000,
        "reseller_revenue": 0
    }
    # Factor = 0.346 (34.6%)
    # Assessable = 100k + 50k = 150k
    # Contribution = 150k * 0.346 = 51,900
    
    resp = client.post("/fcc/form499/calculate?usf_factor=0.346", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    assert data["estimated_contribution"] == 51_900.0

def test_cpni_cert():
    payload = {
        "officer_name": "Jane Compliance",
        "breaches": []
    }
    
    resp = client.post("/fcc/cpni/certify?officer_name=Jane%20Compliance", json=[])
    assert resp.status_code == 200
    data = resp.json()
    assert data["compliance_officer_name"] == "Jane Compliance"
