from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# --- AML/CFT Transaction Monitoring ---
# CBN AML/CFT Regulations 2022

class Transaction(BaseModel):
    id: str
    amount: float
    currency: str = "NGN"
    sender_id: str
    recipient_id: str
    timestamp: str
    type: str # TRANSFER, DEPOSIT, WITHDRAWAL

class AMLFlag(BaseModel):
    tx_id: str
    flag_type: str # CTR (Currency Transaction Report), STR (Suspicious Transaction Report)
    reason: str

def monitor_transactions(transactions: List[Transaction]) -> List[AMLFlag]:
    """
    Flags transactions based on CBN thresholds.
    - Tier 1 Individual Limit: N50,000 (just an example of logic, but let's stick to reporting limits)
    - CBN CTR Threshold:
        - Individual: > N500,000 (Example historical, actually NGN 5M+ for individual, 10M+ corporate in recent revisions)
        - Legal Entity: > N10,000,000
    Let's implement the N5M / N10M standard for CTR.
    """
    flags = []
    CTR_INDIVIDUAL_LIMIT = 5_000_000
    CTR_CORPORATE_LIMIT = 10_000_000
    
    # We assume sender_id starting with 'CORP' implies corporate for this prototype
    
    for tx in transactions:
        threshold = CTR_CORPORATE_LIMIT if tx.sender_id.startswith("CORP") else CTR_INDIVIDUAL_LIMIT
        
        if tx.amount >= threshold:
            flags.append(AMLFlag(
                tx_id=tx.id,
                flag_type="CTR",
                reason=f"Amount {tx.amount} exceeds reporting threshold {threshold}"
            ))
            
        # Basic STR logic: Round numbers (structuring) or very rapid transfers could be here.
        # Simple placeholder:
        if tx.amount == 9_999_999: # Structuring attempt?
            flags.append(AMLFlag(tx_id=tx.id, flag_type="STR", reason="Potential structuring detected"))
            
    return flags

# --- Cybersecurity Levy (Act 2024) ---
# 0.005% on all electronic transfers

def calculate_cyber_levy(amount: float) -> float:
    """
    Calculates 0.005% levy.
    """
    LEVY_RATE = 0.00005
    return round(amount * LEVY_RATE, 2)

# --- Capital Adequacy ---
# BOFIA 2020: Minimum Shareholders' Funds unimpaired by losses.

def check_capital_adequacy(shareholders_funds: float, risk_weighted_assets: float, min_car: float = 0.10) -> dict:
    """
    Calculates CAR (Capital Adequacy Ratio).
    Min CAR is typically 10% or 15% depending on license.
    """
    if risk_weighted_assets == 0:
        car = float('inf')
    else:
        car = shareholders_funds / risk_weighted_assets
        
    compliant = car >= min_car
    return {
        "car_percent": round(car * 100, 2),
        "required_percent": min_car * 100,
        "status": "COMPLIANT" if compliant else "BREACH",
        "surplus_deficit": shareholders_funds - (risk_weighted_assets * min_car)
    }
