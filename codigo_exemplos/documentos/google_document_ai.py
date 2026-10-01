from google.api_core.client_options import ClientOptions
from google.cloud import documentai


def process_document(
    project_id,
    location,
    processor_id,
    file_path
):
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    name = (
        f"projects/{project_id}/"
        f"locations/{location}/"
        f"processors/{processor_id}"
    )

    with open(file_path, "rb") as file:
        content = file.read()

    raw_document = documentai.RawDocument(
        content=content,
        mime_type="application/pdf"
    )

    request = documentai.ProcessRequest(
        name=name,
        raw_document=raw_document
    )

    result = client.process_document(
        request=request
    )

    return result.document


document = process_document(
    "PROJECT_ID",
    "us",
    "PROCESSOR_ID",
    "documento.pdf"
)

print(document.text)
