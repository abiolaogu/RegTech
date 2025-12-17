from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List
import shutil
import os

from .hub_service import HubService, ComplianceRequest
from .vault_service import VaultService
from .advisory_service import AdvisoryService

router = APIRouter(prefix="/regulatory-officer", tags=["Regulatory Officer"])

# Initialize Services (Singleton pattern for prototype)
hub_service = HubService()
vault_service = VaultService()
advisory_service = AdvisoryService()

# --- Collection Hub Endpoints ---

class CreateRequestModel(BaseModel):
    type: str
    department: str

class ReviewRequestModel(BaseModel):
    approve: bool
    comments: Optional[str] = ""

@router.post("/hub/requests", response_model=ComplianceRequest)
def create_data_request(req: CreateRequestModel):
    return hub_service.create_request(req.type, req.department)

@router.get("/hub/requests", response_model=List[ComplianceRequest])
def list_requests(status: Optional[str] = None):
    return hub_service.get_requests(status)

@router.post("/hub/requests/{req_id}/submit")
def submit_artifact(req_id: str, file: UploadFile = File(...)):
    # Save temp file
    temp_dir = "/tmp/regtech_uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    updated_req = hub_service.submit_artifact(req_id, file_path)
    if not updated_req:
        raise HTTPException(status_code=404, detail="Request not found")
    return updated_req

@router.post("/hub/requests/{req_id}/review")
def review_request(req_id: str, review: ReviewRequestModel):
    updated_req = hub_service.review_request(req_id, review.approve, review.comments)
    if not updated_req:
        raise HTTPException(status_code=404, detail="Request not found")
    
    # If approved and has artifacts, maybe move to Vault automatically? 
    # For now, we leave that as a separate manual step or implicit in Logic.
    return updated_req

# --- Evidence Vault Endpoints ---

@router.post("/vault/upload")
def upload_evidence(category: str = Form(...), file: UploadFile = File(...), meta: str = Form('{}')):
    # Save temp
    temp_dir = "/tmp/regtech_vault_staging"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    import json
    meta_dict = json.loads(meta)
    
    result = vault_service.store_document(category, file_path, meta_dict)
    
    # Cleanup temp
    os.remove(file_path)
    
    return result

# --- Board Advisory Endpoints ---

class QoSModel(BaseModel):
    metric: str
    value: float

@router.post("/advisory/qos-event")
def trigger_qos_check(event: QoSModel):
    result = advisory_service.process_qos_event(event.metric, event.value)
    return result
