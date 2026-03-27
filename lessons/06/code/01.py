## System Prompting

from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")


BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    messages=[
        {
            "role": "system",
            # SYSTEM PROMPT:
            # This sets the behavior/personality/rules for the AI.
            # It tells the model:
            # - You are ONLY a math expert
            # - Only answer math-related questions
            # - If question is not math, say "sorry" and refuse
            #
            # This is VERY IMPORTANT because it controls how the AI behaves.
            "content": "You are an expert in Maths and only and only Maths related questions. If the query is not related to maths just say sorry and do not answer that.",
        },
        {
            "role": "user",
            # USER PROMPT:
            # This is the actual question asked by the user
            # This question is NOT math-related (it's programming)
            "content": "Hey, Can you code a python program that can print Hello",
        },
    ],
)


print(response.choices[0].message.content)
