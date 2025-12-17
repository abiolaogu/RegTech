from fastapi import APIRouter
from typing import List

from .services import (
    monitor_transactions, Transaction, AMLFlag,
    calculate_cyber_levy,
    check_capital_adequacy
)

router = APIRouter(prefix="/cbn", tags=["CBN FinTech Compliance"])

@router.post("/aml/monitor", response_model=List[AMLFlag])
def api_monitor_tx(transactions: List[Transaction]):
    """
    Submits a batch of transactions for AML/CFT monitoring (CTR/STR).
    """
    return monitor_transactions(transactions)

@router.post("/levy/cybersecurity", description="Calculate 0.005% Cybersecurity Levy (Act 2024)")
def api_cyber_levy(amount: float):
    return {
        "transaction_amount": amount,
        "levy_payable": calculate_cyber_levy(amount),
        "rate": "0.005%"
    }

@router.get("/capital-adequacy/check")
def api_check_car(shareholders_funds: float, risk_weighted_assets: float, license_type: str = "NATIONAL"):
    # Min CAR depends on license, defaulting logic here:
    min_car = 0.10 if license_type == "REGIONAL" else 0.15 # Example logic
    return check_capital_adequacy(shareholders_funds, risk_weighted_assets, min_car)
