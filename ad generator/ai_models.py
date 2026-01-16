from openai import OpenAI
from dotenv import load_dotenv
import os
import base64
from PIL import Image
import io

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def generate_ad_image(prompt: str) -> Image.Image:
    """
    Generate an ad image using OpenAI image generation.
    """

    result = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result.data[0].b64_json
    image_bytes = base64.b64decode(image_base64)

    return Image.open(io.BytesIO(image_bytes)).convert("RGB")
