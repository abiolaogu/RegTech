from typing import List, Optional
from datetime import date
from .models import RegulatoryRule, FiscalParameter

class ConfigurationService:
    def __init__(self):
        # In a real implementation, these would be loaded from LumaDB
        self._rules_store: List[RegulatoryRule] = [
            RegulatoryRule(
                rule_id="NCC-001",
                jurisdiction="NCC",
                metric="DropCallRate",
                threshold=1.0,
                operator="GT", # Breach if > 1.0%
                description="Drop Call Rate must be less than 1%"
            ),
            RegulatoryRule(
                rule_id="NCC-002", 
                jurisdiction="NCC",
                metric="CallSetupSuccessRate",
                threshold=98.0,
                operator="LT", # Breach if < 98%
                description="Call Setup Success Rate must be >= 98%"
            ),
             RegulatoryRule(
                rule_id="NCC-003",
                jurisdiction="NCC",
                metric="InternetLatency",
                threshold=100.0,
                operator="GT", # Breach if > 100ms
                description="Latency must be < 100ms"
            )
        ]
        
        self._fiscal_store: List[FiscalParameter] = [
            FiscalParameter(
                param_id="FIS-001",
                jurisdiction="NCC",
                key="AOL_LEVY_PERCENT",
                value=0.01, # 1%
                effective_date=date(2023, 1, 1)
            )
        ]

    def get_rules_for_jurisdiction(self, jurisdiction: str) -> List[RegulatoryRule]:
        return [r for r in self._rules_store if r.jurisdiction == jurisdiction and r.enabled]

    def get_rule_for_metric(self, jurisdiction: str, metric: str) -> Optional[RegulatoryRule]:
        for r in self._rules_store:
            if r.jurisdiction == jurisdiction and r.metric == metric and r.enabled:
                return r
        return None

    def get_fiscal_parameter(self, jurisdiction: str, key: str) -> Optional[float]:
        # Logic to return active param based on date could go here
        # For now, return the first match
        for p in self._fiscal_store:
            if p.jurisdiction == jurisdiction and p.key == key:
                return p.value
        return None
