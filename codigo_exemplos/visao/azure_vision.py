import os

from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential

client = ImageAnalysisClient(
    endpoint=os.environ["VISION_ENDPOINT"],
    credential=AzureKeyCredential(
        os.environ["VISION_KEY"]
    )
)

with open("foto.jpg", "rb") as image_file:
    image_data = image_file.read()

result = client.analyze(
    image_data=image_data,
    visual_features=[
        VisualFeatures.TAGS,
        VisualFeatures.OBJECTS
    ]
)

for tag in result.tags.list:
    print(
        tag.name,
        tag.confidence
    )
