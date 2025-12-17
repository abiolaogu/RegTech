from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime, date, timedelta
import uuid

from .services import (
    fetch_board_attendance,
    generate_principle12_summary,
    check_deadline_trigger,
    sign_document,
    verify_signature_role,
)

app = FastAPI(title="Compliance Report Generator", version="1.0")

class SectionContent(BaseModel):
    title: str
    content: str
    evidences: Optional[List[str]] = None

class GenerateReportRequest(BaseModel):
    company_name: str = Field(..., description="Name of the telecom licensee")
    reporting_period: str = Field(..., description="e.g., '2025')")
    board_secretariat_log_path: str = Field(..., description="Path or identifier for board attendance logs")
    consultant_report_path: Optional[str] = Field(None, description="Path to external consultant report for Principle 12")
    submit_type: str = Field(..., description="'mid-year' or 'annual'")

class SignatureRequest(BaseModel):
    report_id: str
    signer_role: str = Field(..., description="One of: 'Chairman', 'CEO', 'RegulatoryOfficer'")
    signature: str = Field(..., description="Digital signature payload (e.g., base64)")

@app.post("/reports/generate")
async def generate_report(req: GenerateReportRequest, background: BackgroundTasks):
    # Verify deadline triggers
    if not check_deadline_trigger(req.submit_type):
        raise HTTPException(status_code=400, detail="Submission deadline missed or invalid submit_type")

    # Gather dynamic data
    attendance = fetch_board_attendance(req.board_secretariat_log_path)
    principle12_summary = generate_principle12_summary(req.consultant_report_path)

    # Build sections A-F
    sections = []
    sections.append(SectionContent(title="A. Introduction", content=f"Compliance report for {req.company_name} for period {req.reporting_period}."))
    sections.append(SectionContent(title="B. General Info", content="[Static general information here]"))
    sections.append(SectionContent(title="C. Board Details", content="Board attendance records attached.", evidences=attendance))
    sections.append(SectionContent(title="D. Senior Management", content="[Static senior management info]"))
    sections.append(SectionContent(title="E. Application of Principles", content=principle12_summary))
    sections.append(SectionContent(title="F. Certification", content="Awaiting digital signatures from authorized signers."))

    report_id = str(uuid.uuid4())
    # Define the background process
    def process_report(r_id, data_sections, company, period):
        # 1. Prepare context
        context = {
            "company_name": company,
            "reporting_period": period,
            "sections": [s.dict() for s in data_sections],
            "signatures": {} # Signatures added later via separate endpoint, strictly
        }
        
        # 2. Render PDF
        pdf_filename = f"Compliance_Report_{r_id}.pdf"
        # Temp path for generation
        temp_path = f"/tmp/{pdf_filename}"
        
        from .pdf_renderer import render_report_to_pdf
        render_report_to_pdf(context, temp_path)
        
        # 3. Upload
        from .storage_notifications import StorageService, NotificationService
        storage = StorageService(provider='local') # Default to local for dev
        file_url = storage.upload_file(temp_path, pdf_filename)
        
        # 4. Notify
        notifier = NotificationService()
        notifier.send_email(
            "compliance@example.com", 
            f"New Compliance Report Generated: {r_id}",
            f"The report for {company} is ready. Access it here: {file_url}"
        )
        
        # Cleanup
        if os.path.exists(temp_path):
            os.remove(temp_path)

    background.add_task(process_report, report_id, sections, req.company_name, req.reporting_period)
    return {"report_id": report_id, "status": "processing_started", "sections": [s.dict() for s in sections]}

@app.post("/reports/{report_id}/sign")
async def sign_report(report_id: str, sig_req: SignatureRequest):
    # Verify role is allowed
    if not verify_signature_role(sig_req.signer_role):
        raise HTTPException(status_code=403, detail="Signer role not authorized for signature")
    # Store signature (placeholder)
    sign_document(report_id, sig_req.signer_role, sig_req.signature)
    return {"status": "signature recorded", "report_id": report_id, "signer": sig_req.signer_role}
