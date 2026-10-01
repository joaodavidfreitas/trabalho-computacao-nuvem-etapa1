import boto3

client = boto3.client(
    "rekognition",
    region_name="us-east-1"
)

response = client.detect_labels(
    Image={
        "S3Object": {
            "Bucket": "meu-bucket",
            "Name": "foto.jpg"
        }
    },
    MaxLabels=10,
    MinConfidence=80
)

for label in response["Labels"]:
    print(
        label["Name"],
        label["Confidence"]
    )
