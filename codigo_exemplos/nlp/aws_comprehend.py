import boto3

client = boto3.client(
    "comprehend",
    region_name="us-east-1"
)

response = client.detect_sentiment(
    Text="This movie was excellent.",
    LanguageCode="en"
)

print("Sentiment:", response["Sentiment"])
print("Scores:", response["SentimentScore"])
