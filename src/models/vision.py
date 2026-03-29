import google.generativeai as genai
from config.config import VISION_API_KEY

genai.configure(api_key=VISION_API_KEY)

model = genai.GenerativeModel("gemini-pro-vision")

def summarize_image(image_bytes):

    response = model.generate_content([
        "Describe this automotive engineering diagram in detail.",
        {"mime_type": "image/png", "data": image_bytes}
    ])

    return response.text