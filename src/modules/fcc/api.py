from fastapi import APIRouter
from typing import List

from .services import (
    aggregate_form477_data, DeploymentLocation,
    calculate_usf_contribution, RevenueWorksheet,
    generate_cpni_certificate, CPNIBreach, CPNIAuditCertificate
)

router = APIRouter(prefix="/fcc", tags=["USA FCC Compliance"])

@router.post("/form477/aggregate", description="Aggregates broadband deployment data for Form 477/BDC")
def api_form477(locations: List[DeploymentLocation]):
    return aggregate_form477_data(locations)

@router.post("/form499/calculate", description="Estimates USF contribution for Form 499-A/Q")
def api_form499(worksheet: RevenueWorksheet, usf_factor: float = 0.346):
    contribution = calculate_usf_contribution(worksheet, usf_factor)
    return {
        "usf_factor_used": usf_factor,
        "estimated_contribution": contribution,
        "assessable_revenue": worksheet.interstate_revenue + worksheet.international_revenue
    }

@router.post("/cpni/certify", response_model=CPNIAuditCertificate, description="Generates CPNI Annual Compliance Certificate")
def api_cpni_certify(officer_name: str, breaches: List[CPNIBreach]):
    return generate_cpni_certificate(officer_name, breaches)
