from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

text = "My email is test@gmail.com and phone is 9876543210"

results = analyzer.analyze(
    text=text,
    language="en"
)

for r in results:
    print(r)
