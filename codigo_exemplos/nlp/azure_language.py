import os

from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

client = TextAnalyticsClient(
    endpoint=os.environ["AZURE_LANGUAGE_ENDPOINT"],
    credential=AzureKeyCredential(
        os.environ["AZURE_LANGUAGE_KEY"]
    )
)

documents = [
    "This movie was excellent."
]

results = client.analyze_sentiment(documents)

for document in results:
    if not document.is_error:
        print("Sentiment:", document.sentiment)
        print("Scores:", document.confidence_scores)
