from openai import OpenAI
from dotenv import load_dotenv
import os
import requests
import json

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "City name, e.g. 'Toronto'",
                    }
                },
                "required": ["city"],
            },
        },
    }
]

SYSTEM_PROMPT = "You are a helpful weather assistant. Use the get_weather tool whenever the user asks about weather. Never make up weather data."


def get_weather(city: str) -> str:
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%c+%t", timeout=10)
        if response.status_code == 200:
            return response.text.strip()
        return "Failed to fetch weather."
    except Exception as e:
        return f"Weather service error: {str(e)}"


TOOL_MAP = {"get_weather": get_weather}


def run_agent(messages: list):
    while True:
        response = client.chat.completions.create(
            model="gemini-2.5-flash-lite",
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
        )

        choice = response.choices[0]
        messages.append(choice.message)

        # No tool call — final answer
        if choice.finish_reason == "stop":
            print(f"\n🤖: {choice.message.content}")
            break

        # Execute tool calls
        if choice.finish_reason == "tool_calls":
            for tool_call in choice.message.tool_calls:
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)

                print(f"\n🔧 Calling {name}({args})")

                result = TOOL_MAP[name](**args) if name in TOOL_MAP else f"Unknown tool: {name}"

                print(f"   Result: {result}")

                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                })


def main():
    print("Weather Agent ready. Type 'exit' to quit.\n")

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("> ").strip()

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            break

        messages.append({"role": "user", "content": user_input})
        run_agent(messages)
        print()


if __name__ == "__main__":
    main()
