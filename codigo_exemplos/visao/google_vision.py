from google.cloud import vision

client = vision.ImageAnnotatorClient()

with open("foto.jpg", "rb") as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.label_detection(
    image=image
)

for label in response.label_annotations:
    print(
        label.description,
        label.score
    )

if response.error.message:
    raise RuntimeError(response.error.message)
