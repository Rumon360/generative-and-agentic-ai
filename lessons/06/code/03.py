# Few-Shot Prompting
# Widely used - Better than zero / one shot prompting
# Here we give examples along with the instructions
# Defination: The model is provided with a few examples before asking
# it to generate a response.

from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


# Few-Shot Prompting: Give direct instructions and few examples to the model
# These examples increases the accuracy of the output.
SYSTEM_PROMPT = """
You should only and only answer the coding related questions. 
Do not answer anything else. Your name is Alexa. 
If user asks something other than coding, just say sorry.

Examples:
Q: Can you explain the a + b whole square?
A: Sorry, I can only help with Coding related questions.

Q: Hey, Write a code in python for adding two numbers.
A: def add(a, b):
    return: a + b

"""


response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "If $3(x - 5) = 2(x + 1)$, find the value of $x$.",
        },
    ],
)


print(response.choices[0].message.content)
