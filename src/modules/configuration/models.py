from typing import Optional
from pydantic import BaseModel
from datetime import date

class RegulatoryRule(BaseModel):
    rule_id: str
    jurisdiction: str  # "NCC", "FCC", "CBN"
    metric: str        # e.g., "DropCallRate"
    threshold: float   # e.g., 1.0
    operator: str      # "GT" (Greater Than), "LT" (Less Than)
    description: Optional[str] = None
    enabled: bool = True

class FiscalParameter(BaseModel):
    param_id: str
    jurisdiction: str
    key: str           # e.g., "AOL_LEVY_PERCENT"
    value: float       # e.g., 0.01
    effective_date: date
