import os
import json
from presidio_analyzer import AnalyzerEngine
from recognizers import (
    PANRecognizer,
    AadhaarRecognizer,
    VoterIDRecognizer,
    OrgIDRecognizer,
)
from pdf_utils import extract_text_from_pdf

# ================= CONFIG =================

TEST_DIR = "TEST"

ALLOWED_ENTITIES = {
    "PERSON",
    "EMAIL_ADDRESS",
    "PHONE_NUMBER",
    "PAN",
    "AADHAAR",
    "VOTER_ID",
    "IBAN_CODE",
    "CREDIT_CARD",
    "LOCATION",
    "ORG_ID",
}

# ================= SETUP =================

def setup_analyzer():
    analyzer = AnalyzerEngine()
    analyzer.registry.add_recognizer(PANRecognizer())
    analyzer.registry.add_recognizer(AadhaarRecognizer())
    analyzer.registry.add_recognizer(VoterIDRecognizer())
    analyzer.registry.add_recognizer(OrgIDRecognizer())
    return analyzer

# ================= ANALYSIS =================

def analyze_text(text, analyzer):
    results = analyzer.analyze(text=text, language="en")

    output = []
    for r in results:
        if r.entity_type not in ALLOWED_ENTITIES:
            continue

        output.append({
            "entity": r.entity_type,
            "value": text[r.start:r.end],
            "confidence": round(r.score, 2),
            "start": r.start,
            "end": r.end
        })

    return output

# ================= RUN TESTS =================

def main():
    analyzer = setup_analyzer()
    final_output = {}

    for file in os.listdir(TEST_DIR):
        path = os.path.join(TEST_DIR, file)

        if file.endswith(".txt"):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
            final_output[file] = analyze_text(text, analyzer)

        elif file.endswith(".pdf"):
            text = extract_text_from_pdf(path)
            final_output[file] = analyze_text(text, analyzer)

    print(json.dumps(final_output, indent=2))

# ================= ENTRY =================

if __name__ == "__main__":
    main()
