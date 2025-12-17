from fastapi.testclient import TestClient
from datetime import date, timedelta
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modules.ncc.financial_sustainability.api import router
from modules.ncc.financial_sustainability.services import ESG_STORE
from fastapi import FastAPI
app = FastAPI()
app.include_router(router)

client = TestClient(app)

def test_aol_calculation_billyroot_case():
    """
    Test Case:
    Gross Revenue: N60B
    Assessable Income: N45.2B
    Implied Deductions: N14.8B
    Expected Levy: 1% of 45.2B = N0.452B
    """
    # We split the 14.8B deduction arbitrarily between interconnect and roaming for input
    # 10B + 4.8B = 14.8B
    payload = {
        "gross_revenue": 60_000_000_000,
        "interconnect_costs": 10_000_000_000,
        "roaming_costs": 4_800_000_000
    }
    
    resp = client.post("/finance/aol/calculate", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    
    # Verify Assessable Income
    assert data["assessable_income"] == 45_200_000_000
    
    # Verify Levy (1%)
    assert data["levy_payable"] == 452_000_000

def test_esg_tracker():
    # Clear store
    ESG_STORE.clear()
    
    metric = {
        "id": "m1",
        "category": "Diversity",
        "name": "Female Engineering %",
        "value": 35.0,
        "unit": "%",
        "timestamp": "2025-06-01T10:00:00"
    }
    
    # Log
    resp = client.post("/sustainability/metrics", json=metric)
    assert resp.status_code == 200
    
    # Get
    resp = client.get("/sustainability/metrics")
    data = resp.json()
    assert len(data) == 1
    assert data[0]["value"] == 35.0

def test_debt_monitor():
    today = date.today()
    past = today - timedelta(days=10)
    future = today + timedelta(days=10)
    
    payload = [
        {"id": "d1", "counterparty": "Telco A", "amount": 1000, "due_date": past.isoformat(), "status": "PENDING"}, # Should flag
        {"id": "d2", "counterparty": "Telco B", "amount": 2000, "due_date": future.isoformat(), "status": "PENDING"}, # Safe
        {"id": "d3", "counterparty": "Telco C", "amount": 3000, "due_date": past.isoformat(), "status": "PAID"} # Safe
    ]
    
    resp = client.post("/finance/debt/monitor", json=payload)
    assert resp.status_code == 200
    flagged = resp.json()
    
    assert len(flagged) == 1
    assert flagged[0]["id"] == "d1"
