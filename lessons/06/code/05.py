# Chain-of-Thought (CoT) for Reasoning Prompting
# We want out model to be more accurate, so we want our model to think first
# before answering which can be achieved using CoT
from dotenv import load_dotenv
from openai import OpenAI
import os
import json

load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")
BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)


SYSTEM_PROMPT = """
    You're an expert AI Assistant in resolving user queries using chain of thought.
    You work on START, PLAN and OUTPUT steps.
    You need to first PLAN what needs to be done. The PLAN can be multiple steps.
    Once you think enough PLAN has been done, finally you can give an OUTPUT.

    Rules:
    - Strictly Follow the given JSON output format
    - Only run one step at a time.
    - The sequence of steps is START (where user gives an input), PLAN (That can
    be multiple times) and finally OUTPUT (which is going to be displayed to the user).

    Output JSON Format:
    { "step": "START" | "PLAN" | "OUTPUT", "content": "string" }

    Example:
    START: Hey, can you solve 2 + 3 * 5 / 10
    PLAN: {"step": "PLAN", "content": "Seems like the user is interested in maths problem."}
    PLAN: {"step": "PLAN", "content": "Looking at the problem, we should solve this using BODMAS method"}
    PLAN: {"step": "PLAN", "content": "Yes, The BODMAS is correct thing to be done here"}
    PLAN: {"step": "PLAN", "content": "First we must multiply 3 * 5 which is 15"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 15 / 10"}
    PLAN: {"step": "PLAN", "content": "We must perform divide that is 15 / 10 = 1.5"}
    PLAN: {"step": "PLAN", "content": "Now the new equation is 2 + 1.5"}
    PLAN: {"step": "PLAN", "content": "Now Finally let perform the add which is 3.5"}
    PLAN: {"step": "PLAN", "content": "Great, we have solved and finally left with 3.5 as answer"}
    OUTPUT: {"step": "OUTPUT", "content": "3.5"}
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash-lite",
    response_format={"type": "json_object"},
    messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": "Hey, write a code to add n numbers in js",
        },
        # Manually keep adding messages to the History
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "PLAN",
                    "content": "The user wants a JavaScript code snippet to add 'n' numbers. I should provide a function that accepts an array of numbers and returns their sum.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "PLAN",
                    "content": "The user wants a JavaScript code snippet to add 'n' numbers. I should provide a function that accepts an array of numbers and returns their sum.",
                }
            ),
        },
        {
            "role": "assistant",
            "content": json.dumps(
                {
                    "step": "OUTPUT",
                    "content": "```javascript\nfunction sumNumbers(numbers) {\n  let sum = 0;\n  for (let i = 0; i < numbers.length; i++) {\n    sum += numbers[i];\n  }\n  return sum;\n}\n\n// Example usage:\nconst myNumbers = [1, 2, 3, 4, 5];\nconst total = sumNumbers(myNumbers);\nconsole.log(total); // Output: 15\n```",
                }
            ),
        },
    ],
)


print(response.choices[0].message.content)
