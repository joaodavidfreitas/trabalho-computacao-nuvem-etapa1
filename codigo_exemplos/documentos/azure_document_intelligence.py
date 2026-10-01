import os

from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient

client = DocumentIntelligenceClient(
    endpoint=os.environ["DOCUMENTINTELLIGENCE_ENDPOINT"],
    credential=AzureKeyCredential(
        os.environ["DOCUMENTINTELLIGENCE_API_KEY"]
    )
)

with open("documento.pdf", "rb") as file:
    poller = client.begin_analyze_document(
        "prebuilt-layout",
        body=file
    )

result = poller.result()

for page in result.pages:
    print(
        "Page:",
        page.page_number
    )

    if page.lines:
        for line in page.lines:
            print(line.content)
