from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pdfplumber

from presidio_analyzer import AnalyzerEngine
from recognizers import PANRecognizer, AadhaarRecognizer, VoterIDRecognizer, OrgIDRecognizer

app = FastAPI(title="PII Detection Backend")

# ===================== CORS =====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===================== ENGINE =====================
analyzer = AnalyzerEngine()
analyzer.registry.add_recognizer(PANRecognizer())
analyzer.registry.add_recognizer(AadhaarRecognizer())
analyzer.registry.add_recognizer(VoterIDRecognizer())
analyzer.registry.add_recognizer(OrgIDRecognizer())


# ===================== MODEL =====================
class AnalyzeRequest(BaseModel):
    text: str
    threshold: Optional[float] = 0.5

# ===================== CLEAN ENTITIES =====================
def clean_entities(results):
    cleaned = []

    for r in results:
        # Remove Aadhaar overlapping with credit card
        if r.entity_type == "AADHAAR":
            overlap = any(
                c.entity_type == "CREDIT_CARD"
                and not (r.end <= c.start or r.start >= c.end)
                for c in results
            )
            if overlap:
                continue

        cleaned.append(r)

    return cleaned

# ===================== ANALYZE =====================
@app.post("/analyze")
def analyze(req: AnalyzeRequest):
    results = analyzer.analyze(req.text, language="en")
    results = clean_entities(results)

    entities = [
        {
            "entity": r.entity_type,
            "start": r.start,
            "end": r.end,
            "confidence": round(r.score, 2),
            "value": req.text[r.start:r.end]
        }
        for r in results
        if r.score >= req.threshold
    ]

    return {"entities": entities}

# ===================== MASK =====================
@app.post("/mask")
def mask(req: AnalyzeRequest):
    results = clean_entities(analyzer.analyze(req.text, language="en"))
    text = req.text

    for r in sorted(results, key=lambda x: x.start, reverse=True):
        if r.entity_type == "PAN":
            text = text[:r.start] + "XXXXXXXXXX" + text[r.end:]
        elif r.entity_type == "AADHAAR":
            text = text[:r.start] + "XXXX XXXX XXXX" + text[r.end:]
        elif r.entity_type == "IBAN_CODE":
            text = text[:r.start] + "XXXXXXXXXXXXXXXXXXXX" + text[r.end:]
        elif r.entity_type == "CREDIT_CARD":
            text = text[:r.start] + "XXXX XXXX XXXX XXXX" + text[r.end:]

    return {"masked": text}

# ===================== PDF =====================
@app.post("/upload-pdf")
def upload_pdf(file: UploadFile = File(...)):
    text = ""

    with pdfplumber.open(file.file) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                text += page.extract_text() + "\n"

    results = clean_entities(analyzer.analyze(text, language="en"))

    entities = [
        {
            "entity": r.entity_type,
            "start": r.start,
            "end": r.end,
            "confidence": round(r.score, 2),
            "value": text[r.start:r.end]
        }
        for r in results
    ]

    return {"entities": entities}
