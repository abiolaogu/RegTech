from fastapi import APIRouter
from typing import List
from datetime import datetime

from .services import (
    calculate_aol, AOLInput, AOLResult,
    log_esg_metric, get_esg_report, ESGMetric,
    check_outstanding_debts, DebtRecord
)

router = APIRouter(tags=["Financial & Sustainability"])

@router.post("/finance/aol/calculate", response_model=AOLResult)
def api_calculate_aol(data: AOLInput):
    return calculate_aol(data)

@router.post("/sustainability/metrics")
def api_log_metric(metric: ESGMetric):
    log_esg_metric(metric)
    return {"status": "logged"}

@router.get("/sustainability/metrics", response_model=List[ESGMetric])
def api_get_metrics():
    return get_esg_report()

@router.post("/finance/debt/monitor", response_model=List[DebtRecord])
def api_monitor_debts(debts: List[DebtRecord]):
    """
    Accepts a list of current debts (from SAP/ERP) and returns those that are overdue.
    """
    return check_outstanding_debts(debts)
