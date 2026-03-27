# One-Shot Prompting / Zero-Shot Prompting Example

from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


# SYSTEM PROMPT (Zero-shot / One-shot instruction)
# ------------------------------------------------
# This is called "Zero-shot prompting" because:
# - You are NOT giving any examples
# - You are ONLY giving instructions
#
# It defines:
# 1. Role restriction → Only coding questions allowed
# 2. Identity → Model's name is "Alexa"
# 3. Behavior → If not coding, say "sorry"
#
# This acts like rules the AI must follow before answering
SYSTEM_PROMPT = "You should only and only answer the coding related questions. Do not answer anything else. Your name is Alexa. If user asks something other than coding, just say sorry."


response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    # Messages define the conversation flow
    messages=[
        {
            "role": "system",
            # SYSTEM ROLE:
            # Sets behavior, personality, and restrictions
            "content": SYSTEM_PROMPT,
        },
        # Example of a NON-coding question (commented out)
        # If you enable this, output should be:
        # "sorry"
        #
        # {
        #     "role": "user",
        #     "content": "Hey, Can you tell me a joke",
        # },
        {
            "role": "user",
            # USER QUESTION:
            # This IS a coding question → allowed
            "content": "Hey, Can you write a python code to sum to numbers",
        },
    ],
)


print(response.choices[0].message.content)
