from google import genai
from google.genai import types
from app.config import settings
import base64

client = genai.Client(api_key=settings.google_api_key)

def generate_image_sync(prompt: str) -> str:
    """Helper sincrono per generare immagini con Imagen 3"""
    response = client.models.generate_images(
    model="gemini-2.5-flash-image",
    prompt=prompt,
    config={"number_of_images": 1, "aspect_ratio": "16:9"}
)
    image_bytes = response.generated_images[0].image.image_bytes
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    return f"data:image/png;base64,{b64}"