from datetime import date
from typing import List, Optional
from pydantic import BaseModel
import enum

# --- Form 477 (Broadband Deployment) ---

class TechnologyCode(str, enum.Enum):
    FIBER = "50"
    CABLE = "42"
    DSL = "10"
    FIXED_WIRELESS = "70"
    SATELLITE = "60"

class DeploymentLocation(BaseModel):
    census_block_id: str
    technology: TechnologyCode
    max_download_mbps: float
    max_upload_mbps: float
    consumer: bool # Residential
    business: bool

def aggregate_form477_data(locations: List[DeploymentLocation]) -> dict:
    """
    Aggregates deployment data by state/county (implied by Census Block).
    Returns basic stats for the filing.
    """
    aggregated = {
        "total_locations": len(locations),
        "fiber_coverage": 0,
        "avg_down_mbps": 0.0
    }
    
    if not locations:
        return aggregated

    fiber_count = sum(1 for loc in locations if loc.technology == TechnologyCode.FIBER)
    total_down = sum(loc.max_download_mbps for loc in locations)
    
    aggregated["fiber_coverage"] = fiber_count
    aggregated["avg_down_mbps"] = round(total_down / len(locations), 2)
    
    return aggregated

# --- Form 499-A/Q (USF Contribution) ---

class RevenueWorksheet(BaseModel):
    interstate_revenue: float
    international_revenue: float
    intrastate_revenue: float # Often exempt from federal USF but relevant
    end_user_revenue: float # Subject to USF
    reseller_revenue: float # often exempt

def calculate_usf_contribution(worksheet: RevenueWorksheet, factor: float = 0.346) -> float:
    """
    Calculates estimated USF contribution based on Interstate + International End-User Revenue.
    Input factor is the quarterly USF contribution factor (e.g., 34.6% for Q2 2025).
    """
    # Simply: (Interstate + International end-user) * factor
    # Assumption: All provided interstate/intl revenue is end-user revenue for this helper.
    # Real form 499 is much more complex with lines 400-500.
    
    assessable = worksheet.interstate_revenue + worksheet.international_revenue
    contribution = assessable * factor
    return round(contribution, 2)

# --- CPNI Audit (Customer Proprietary Network Information) ---

class CPNIBreach(BaseModel):
    id: str
    customer_id: str
    breach_type: str # "Unauthorized Access", "Disclosure"
    detected_at: str
    reported_to_law_enforcement: bool

class CPNIAuditCertificate(BaseModel):
    compliance_officer_name: str
    certification_date: date
    breaches_reported: List[CPNIBreach]
    statement: str = "I certify that the company has established operating procedures valid for CPNI compliance."

def generate_cpni_certificate(officer: str, breaches: List[CPNIBreach]) -> CPNIAuditCertificate:
    return CPNIAuditCertificate(
        compliance_officer_name=officer,
        certification_date=date.today(),
        breaches_reported=breaches
    )
