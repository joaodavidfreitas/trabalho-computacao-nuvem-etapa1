from google.cloud import language_v2

client = language_v2.LanguageServiceClient()

document = language_v2.Document(
    content="This movie was excellent.",
    type_=language_v2.Document.Type.PLAIN_TEXT,
    language_code="en"
)

response = client.analyze_sentiment(
    request={"document": document}
)

print(
    "Score:",
    response.document_sentiment.score
)

print(
    "Magnitude:",
    response.document_sentiment.magnitude
)
