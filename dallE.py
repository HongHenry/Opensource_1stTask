import openai
import requests
from PIL import Image
from io import BytesIO

# Replace YOUR_API_KEY with your actual API key
openai.api_key = "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"

# Set the prompt for DALL-E to generate an image
prompt = "Draw a banana in a suit playing a guitar"

# Generate the image using DALL-E
response = openai.Completion.create(
  engine="image-alpha-002",
  prompt=prompt,
  max_tokens=0,
  nft=True
)

# Get the URL of the generated image
image_url = response.choices[0].text.strip()

# Download the image and display it
image_data = requests.get(image_url).content
img = Image.open(BytesIO(image_data))
img.show()