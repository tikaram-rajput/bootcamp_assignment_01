import os
import requests

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL = os.getenv("HF_VISION_MODEL")

HEADERS = {
    "Authorization": f"Bearer {HF_TOKEN}"
}


def summarize_image(image_bytes):
    try:
        url = f"https://api-inference.huggingface.co/models/{MODEL}"

        response = requests.post(url, headers=HEADERS, data=image_bytes, timeout=20)

        result = response.json()

        if isinstance(result, list):
            return result[0]["generated_text"]

        return "Image description unavailable"

    except Exception:
        return "Image processing failed"