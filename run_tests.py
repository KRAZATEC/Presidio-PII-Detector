import os
import requests

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8000")

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_DIR = os.path.join(ROOT_DIR, "TEST")

TEXT_FILES = [
    "TEST_1.txt",
    "TEST_2.txt",
    "TEST_3.txt",
    "EDGE_TEST.txt",
    "NEG_TEST.txt",
]

PDF_FILES = [
    "TEST_PDF.pdf",
]


def call_analyze(text, threshold=0.5):
    resp = requests.post(
        f"{BACKEND_URL}/analyze",
        json={"text": text, "threshold": threshold},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def call_mask(text, threshold=0.5):
    resp = requests.post(
        f"{BACKEND_URL}/mask",
        json={"text": text, "threshold": threshold},
        timeout=20,
    )
    resp.raise_for_status()
    return resp.json()


def call_upload_pdf(path, threshold=0.5):
    with open(path, "rb") as f:
        files = {"file": (os.path.basename(path), f, "application/pdf")}
        resp = requests.post(
            f"{BACKEND_URL}/upload-pdf",
            files=files,
            data={"threshold": str(threshold)},
            timeout=60,
        )
    resp.raise_for_status()
    return resp.json()


def run_text_tests():
    print("======== TEXT TESTS ========")
    for fname in TEXT_FILES:
        path = os.path.join(TEST_DIR, fname)
        if not os.path.isfile(path):
            print(f"[SKIP] {fname} not found at {path}")
            continue

        print(f"\n--- FILE: {fname} ---")
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        print("\nInput:")
        print(text)

        try:
            res_analyze = call_analyze(text)
            print("\n/analyze response:")
            print(res_analyze)
        except Exception as e:
            print(f"\nERROR in /analyze: {e}")

        try:
            res_mask = call_mask(text)
            print("\n/mask response:")
            print(res_mask)
        except Exception as e:
            print(f"\nERROR in /mask: {e}")

        print("\n---------------------------")


def run_pdf_tests():
    print("\n======== PDF TESTS ========")
    for fname in PDF_FILES:
        path = os.path.join(TEST_DIR, fname)
        if not os.path.isfile(path):
            print(f"[SKIP] {fname} not found at {path}")
            continue

        print(f"\n--- PDF FILE: {fname} ---")
        try:
            res_pdf = call_upload_pdf(path)
            print("\n/upload-pdf response:")
            print(res_pdf)
        except Exception as e:
            print(f"\nERROR in /upload-pdf: {e}")

        print("\n---------------------------")


def main():
    print("Presidio PII Detector – Automated Test Runner")
    print(f"BACKEND_URL = {BACKEND_URL}")
    print(f"TEST_DIR    = {TEST_DIR}")
    print()

    run_text_tests()
    run_pdf_tests()

    print("\n======== DONE ========")


if __name__ == "__main__":
    main()
