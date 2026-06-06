import base64
from openai import OpenAI

LLM_BASE_URL = "http://localhost:11434/v1"
LLM_API_KEY = "ollama"
LLM_MODEL = "gemma4:e2b"

IMAGE_PATH = "test.jpg"


client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)


def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


base64_image = encode_image(IMAGE_PATH)


response = client.responses.create(
    model=LLM_MODEL,
    input=[
        {
            "role": "user",
            "content": [
                {"type": "input_text", "text": "what's in this image?"},
                {
                    "type": "input_image",
                    "image_url": f"data:image/jpeg;base64,{base64_image}",
                },
            ],
        }
    ],
)

print(response.output_text)
