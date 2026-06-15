from openai import OpenAI
from app.config import settings

openai_image_client = OpenAI(api_key=settings.openai_api_key)


def generate_image_sync(prompt: str):
    """Helper sincrono per generare immagini con gpt-image-1"""
    response = openai_image_client.images.generate(
        model="gpt-image-1", prompt=prompt, size="1024x1024", n=1
    )
    return f"data:image/png;base64,{response.data[0].b64_json}"
