from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import Dict, Any, Optional

# Import internal modules
from modules.ncc.financial_sustainability.services import calculate_aol, AOLInput
from modules.cbn.services import monitor_transactions, Transaction
from modules.fcc.services import calculate_usf_contribution, RevenueWorksheet

router = APIRouter(prefix="/grc-adapter", tags=["GRC Integration Middleware"])

class GRCWebhook(BaseModel):
    event_id: str
    event_type: str # e.g., "CALCULATE_AOL", "CHECK_AML", "CALCULATE_USF"
    payload: Dict[str, Any]
    callback_url: Optional[str] = None # Where to send results back to Eramba

class GRCResponse(BaseModel):
    status: str
    result: Dict[str, Any]

@router.post("/webhook", response_model=GRCResponse)
def handle_grc_event(webhook: GRCWebhook):
    """
    Central handler for generic GRC webhooks (e.g. from Eramba).
    Routes to specific internal calculation engines.
    """
    result = {}
    
    try:
        if webhook.event_type == "CALCULATE_AOL":
            # Map Generic payload to AOLInput
            # Expecting: {"gross": 100, "interconnect": 10, "roaming": 5}
            data = AOLInput(
                gross_revenue=webhook.payload.get("gross", 0),
                interconnect_costs=webhook.payload.get("interconnect", 0),
                roaming_costs=webhook.payload.get("roaming", 0)
            )
            res = calculate_aol(data)
            result = res.model_dump()
            
        elif webhook.event_type == "CHECK_AML":
            # Map Generic payload to List[Transaction]
            # Expecting: {"transactions": [...]}
            raw_txs = webhook.payload.get("transactions", [])
            txs = [Transaction(**t) for t in raw_txs]
            res = monitor_transactions(txs)
            result = {"flags": [f.model_dump() for f in res]}
            
        elif webhook.event_type == "CALCULATE_USF":
            # Map Generic payload to RevenueWorksheet
            data = RevenueWorksheet(
                interstate_revenue=webhook.payload.get("interstate", 0),
                international_revenue=webhook.payload.get("international", 0),
                intrastate_revenue=webhook.payload.get("intrastate", 0),
                end_user_revenue=webhook.payload.get("end_user", 0),
                reseller_revenue=webhook.payload.get("reseller", 0)
            )
            val = calculate_usf_contribution(data)
            result = {"usf_contribution": val}
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown event_type: {webhook.event_type}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return GRCResponse(status="success", result=result)
