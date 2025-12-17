from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure src is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from modules.ncc.compliance_report_generator.api import app
from modules.ncc.compliance_report_generator.services import check_deadline_trigger, verify_signature_role

client = TestClient(app)

def test_deadline_checker():
    assert check_deadline_trigger('mid-year') is True
    assert check_deadline_trigger('annual') is True
    assert check_deadline_trigger('invalid') is False

def test_signature_roles():
    assert verify_signature_role('board_chairman') is False  # Case sensitive in our simple logic
    assert verify_signature_role('Chairman') is True
    assert verify_signature_role('CEO') is True
    assert verify_signature_role('RegulatoryOfficer') is True
    assert verify_signature_role('Intern') is False

@patch('modules.ncc.compliance_report_generator.api.fetch_board_attendance')
@patch('modules.ncc.compliance_report_generator.api.generate_principle12_summary')
@patch('modules.ncc.compliance_report_generator.api.BackgroundTasks.add_task')
def test_generate_report_endpoint(mock_bg, mock_p12, mock_attendance):
    mock_attendance.return_value = ["2025-01-01: Meeting"]
    mock_p12.return_value = "Summary of P12"
    
    payload = {
        "company_name": "Test Telecom",
        "reporting_period": "2025",
        "board_secretariat_log_path": "dummy.log",
        "consultant_report_path": "consultant.txt",
        "submit_type": "mid-year"
    }
    
    response = client.post("/reports/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "report_id" in data
    assert len(data["sections"]) == 6
    assert data["sections"][0]["title"] == "A. Introduction"

def test_generate_report_invalid_deadline():
    payload = {
        "company_name": "Test Telecom",
        "reporting_period": "2025",
        "board_secretariat_log_path": "dummy.log",
        "submit_type": "invalid-type"
    }
    response = client.post("/reports/generate", json=payload)
    assert response.status_code == 400
