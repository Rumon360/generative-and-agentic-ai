from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)

response = client.models.generate_content(
    model="gemini-2.5-flash-lite", contents="Hey There"
)

print(response.text)
