from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel
import uuid

class ComplianceRequest(BaseModel):
    id: str
    type: str  # e.g., "Cooling-Off Check", "AOL Data"
    department: str # HR, Finance, Legal
    status: str # PENDING, REVIEW, APPROVED, REJECTED
    artifacts: List[str] = []
    created_at: str
    updated_at: str

class HubService:
    def __init__(self):
        # In-memory store
        self.requests: Dict[str, ComplianceRequest] = {}

    def create_request(self, req_type: str, department: str) -> ComplianceRequest:
        req_id = str(uuid.uuid4())
        req = ComplianceRequest(
            id=req_id,
            type=req_type,
            department=department,
            status="PENDING",
            created_at=datetime.utcnow().isoformat(),
            updated_at=datetime.utcnow().isoformat()
        )
        self.requests[req_id] = req
        # In a real app, send email/slack notification to Dept here
        print(f"Notification sent to {department} for request {req_id}")
        return req

    def get_requests(self, status: Optional[str] = None) -> List[ComplianceRequest]:
        if status:
            return [r for r in self.requests.values() if r.status == status]
        return list(self.requests.values())

    def submit_artifact(self, req_id: str, artifact_path: str) -> Optional[ComplianceRequest]:
        if req_id not in self.requests:
            return None
        req = self.requests[req_id]
        req.artifacts.append(artifact_path)
        req.status = "REVIEW"
        req.updated_at = datetime.utcnow().isoformat()
        return req

    def review_request(self, req_id: str, approve: bool, comments: str = "") -> Optional[ComplianceRequest]:
        if req_id not in self.requests:
            return None
        req = self.requests[req_id]
        if approve:
            req.status = "APPROVED"
            # In a real app, trigger immutable archival here
        else:
            req.status = "REJECTED" # Sent back to dept
        
        req.updated_at = datetime.utcnow().isoformat()
        print(f"Request {req_id} reviewed. Status: {req.status}. Comments: {comments}")
        return req
