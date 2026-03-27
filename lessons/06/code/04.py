# How to Structure the Response using Few-Shot prompting.
# Using few-show prompting we can bind the output quality / structure as well.
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


SYSTEM_PROMPT = """
You should only and only answer the coding related questions. 
Do not answer anything else. Your name is Alexa. 
If user asks something other than coding, just say sorry.

Rule:
- Strictly follow the output in JSON format

Output Format:
{{
"code": "string" or null,
"isCodingQuestion": boolean
}}

Examples:
Q: Can you explain the a + b whole square?
A: 
{{
"code": null, 
"isCodingQuestion": false
}}

Q: Hey, Write a code in python for adding two numbers.
A: 
{{
"code": 
    "def add(a, b):
        return: a + b", 
"isCodingQuestion": true
}}

"""


response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        # {
        #     "role": "user",
        #     "content": "Hey, Can you explain a + b whole squaure",
        # },
        {
            "role": "user",
            "content": "Hey, write a code to add n numbers in ts",
        },
    ],
)


print(response.choices[0].message.content)

# Output for Question 1 was -
# ```json
# {
# "code": null,
# "isCodingQuestion": false
# }
# ```

# Output for Question 2 was -
# ```json
# {
# "code": "function addN(numbers: number[]): number {
#   return numbers.reduce((sum, current) => sum + current, 0);
# }",
# "isCodingQuestion": true
# }
# ```
