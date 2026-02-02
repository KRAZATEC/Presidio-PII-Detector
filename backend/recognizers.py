from presidio_analyzer import PatternRecognizer, Pattern


# ===================== PAN =====================

class PANRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="PAN",
                regex=r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",
                score=0.9
            )
        ]
        super().__init__(
            supported_entity="PAN",
            patterns=patterns
        )


# ===================== AADHAAR =====================

class AadhaarRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="AADHAAR",
                regex=r"\b\d{4}\s\d{4}\s\d{4}\b",
                score=0.85
            )
        ]
        super().__init__(
            supported_entity="AADHAAR",
            patterns=patterns
        )


# ===================== VOTER ID =====================

class VoterIDRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="VOTER_ID",
                regex=r"\b[A-Z]{3}[0-9]{7}\b",
                score=0.8
            )
        ]
        super().__init__(
            supported_entity="VOTER_ID",
            patterns=patterns
        )


# ===================== ORGANIZATION ID (GENERIC) =====================

class OrgIDRecognizer(PatternRecognizer):
    def __init__(self):
        patterns = [
            Pattern(
                name="ORG_ID_GENERIC",
                # Matches:
                # ORG12345, EMP-90876, COMP_00123, STAFF99, ID-778899
                regex=r"\b[A-Z]{2,10}[-_ ]?\d{2,10}\b",
                score=0.8
            )
        ]
        super().__init__(
            supported_entity="ORG_ID",
            patterns=patterns
        )
