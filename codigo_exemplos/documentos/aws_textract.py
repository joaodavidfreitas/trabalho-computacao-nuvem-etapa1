import boto3

client = boto3.client(
    "textract",
    region_name="us-west-2"
)

with open("documento.png", "rb") as file:
    document_bytes = file.read()

response = client.analyze_document(
    Document={
        "Bytes": document_bytes
    },
    FeatureTypes=[
        "FORMS",
        "TABLES"
    ]
)

for block in response["Blocks"]:
    print(block["BlockType"])
