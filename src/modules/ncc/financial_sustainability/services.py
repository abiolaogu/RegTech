from datetime import date
from typing import List, Optional
from pydantic import BaseModel

# --- AOL Engine ---

class AOLInput(BaseModel):
    gross_revenue: float
    interconnect_costs: float
    roaming_costs: float

class AOLResult(BaseModel):
    gross_revenue: float
    total_deductions: float
    assessable_income: float
    levy_payable: float

def calculate_aol(data: AOLInput) -> AOLResult:
    """
    Calculates the 1% Annual Operating Levy.
    Formula: Levy = 1% of (Gross - (Interconnect + Roaming))
    """
    deductions = data.interconnect_costs + data.roaming_costs
    assessable = data.gross_revenue - deductions
    
    # Levy is 1% of assessable income
    # Note: If Assessable is negative, levy is 0? Generally yes, but NCC rules might vary.
    # Assuming standard tax logic:
    levy = max(0.0, assessable * 0.01)
    
    return AOLResult(
        gross_revenue=data.gross_revenue,
        total_deductions=deductions,
        assessable_income=assessable,
        levy_payable=levy
    )

# --- ESG Tracker ---

class ESGMetric(BaseModel):
    id: str
    category: str # "Renewable" or "Diversity"
    name: str # e.g. "Sites with Solar", "Female Engineering %"
    value: float
    unit: str # "%", "Count"
    timestamp: str

# Simple in-memory store for prototype
ESG_STORE: List[ESGMetric] = []

def log_esg_metric(metric: ESGMetric):
    ESG_STORE.append(metric)

def get_esg_report() -> List[ESGMetric]:
    return ESG_STORE

# --- Debt Settlement Monitor ---

class DebtRecord(BaseModel):
    id: str
    counterparty: str
    amount: float
    due_date: date
    status: str # "PAID", "PENDING"

def check_outstanding_debts(debts: List[DebtRecord]) -> List[DebtRecord]:
    """
    Returns a list of debts that are unpaid and past due.
    """
    today = date.today()
    flagged = []
    for d in debts:
        if d.status != "PAID" and d.due_date < today:
            flagged.append(d)
    return flagged
