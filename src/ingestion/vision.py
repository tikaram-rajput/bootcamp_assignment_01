import base64
import requests
import os

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

URL = "https://openrouter.ai/api/v1/chat/completions"


def summarize_image(image_bytes: bytes):
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    response = requests.post(
        URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "qwen/qwen3.6-plus:free",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Explain this automotive technical diagram in detail."
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/png;base64,{base64_image}"
                        }
                    ]
                }
            ]
        }
    )

    return response.json()["choices"][0]["message"]["content"]