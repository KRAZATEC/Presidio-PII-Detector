import pytest
import io
from fastapi.testclient import TestClient
from reportlab.pdfgen import canvas
from main import app

# Initialize the FastAPI TestClient
client = TestClient(app)


## ===================== TEXT ANALYSIS TESTS =====================

def test_analyze_standard_pii():
    """Test detection of standard Presidio PII (Email)."""
    payload = {
        "text": "My email is test@example.com",
        "threshold": 0.4
    }
    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    data = response.json()

    entities = [e['entity'] for e in data['entities']]
    assert "EMAIL_ADDRESS" in entities
    assert any(e['value'] == "test@example.com" for e in data['entities'])


def test_analyze_indian_pii():
    """Test custom recognizers for PAN and OrgID."""
    text = "User PAN is ABCDE1234F and Org ID is ORG99999"
    payload = {"text": text, "threshold": 0.5}

    response = client.post("/analyze", json=payload)
    assert response.status_code == 200
    entities = [e['entity'] for e in response.json()['entities']]

    assert "PAN" in entities
    assert "ORG_ID" in entities


def test_analyze_aadhaar():
    """Test Aadhaar detection with space formatting."""
    payload = {"text": "Aadhaar number: 1234 5678 9012"}
    response = client.post("/analyze", json=payload)
    data = response.json()

    assert any(e['entity'] == "AADHAAR" for e in data['entities'])


## ===================== MASKING TESTS =====================

def test_masking_logic():
    """Verify masking transformations for sensitive Indian IDs."""
    payload = {"text": "PAN: ABCDE1234F, Aadhaar: 1234 5678 9012"}
    response = client.post("/mask", json=payload)
    assert response.status_code == 200
    masked_text = response.json()["masked"]

    assert "XXXXXXXXXX" in masked_text
    assert "XXXX XXXX XXXX" in masked_text
    assert "ABCDE1234F" not in masked_text


## ===================== PDF UPLOAD TESTS =====================

def test_upload_pdf_integration():
    """
    Simulates a real PDF upload using reportlab to generate a file in memory.
    """
    pdf_buffer = io.BytesIO()
    c = canvas.Canvas(pdf_buffer)
    c.drawString(100, 750, "CONFIDENTIAL DOCUMENT")
    c.drawString(100, 730, "Name: Rajesh Kumar")
    c.drawString(100, 710, "Email: rajesh@example.in")
    c.drawString(100, 690, "Voter ID: ABC1234567")
    c.save()
    pdf_buffer.seek(0)

    files = {"file": ("test.pdf", pdf_buffer, "application/pdf")}
    response = client.post("/upload-pdf", files=files)

    assert response.status_code == 200
    data = response.json()
    entities = [e['entity'] for e in data['entities']]

    assert "EMAIL_ADDRESS" in entities
    assert "VOTER_ID" in entities
    assert any(e['value'] == "ABC1234567" for e in data['entities'])


def test_upload_pdf_no_file():
    """Test response when no file is provided."""
    response = client.post("/upload-pdf")
    assert response.status_code == 422


## ===================== EDGE CASES =====================

def test_threshold_filtering():
    """Verify that the confidence threshold correctly filters out weak matches."""
    # OrgID has a score of 0.8 in recognizers.py
    payload = {
        "text": "Code ORG12345",
        "threshold": 0.9
    }
    response = client.post("/analyze", json=payload)
    # Check that no entities were returned because 0.8 < 0.9
    assert len(response.json()["entities"]) == 0