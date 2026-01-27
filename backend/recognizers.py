from presidio_analyzer import PatternRecognizer, Pattern

class PANRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="PAN",
            patterns=[Pattern("PAN", r"\b[A-Z]{5}[0-9]{4}[A-Z]\b", 0.9)]
        )

class AadhaarRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="AADHAAR",
            patterns=[Pattern("AADHAAR", r"\b\d{4}\s\d{4}\s\d{4}\b", 0.85)]
        )

class VoterIDRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="VOTER_ID",
            patterns=[Pattern("VOTER_ID", r"\b[A-Z]{3}[0-9]{7}\b", 0.8)]
        )

class OrgIDRecognizer(PatternRecognizer):
    def __init__(self):
        super().__init__(
            supported_entity="ORG_ID",
            patterns=[Pattern("ORG_ID", r"\bORG[0-9]{5}\b", 0.8)]
        )
