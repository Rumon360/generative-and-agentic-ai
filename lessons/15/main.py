import speech_recognition as sr
import multiprocessing
import pyttsx3
from utils import wave
from utils.tools import TOOLS, TOOL_FUNCTIONS
from openai import OpenAI
import json

LLM_API_KEY = "ollama"
LLM_BASE_URL = "http://localhost:11434/v1"
LLM_MODEL = "mistral:7b"
EXTRACT_CITY_PROMPT = """
    Extract the city name from this text. Reply with ONLY the city name, nothing else. If no city is found, reply with "unknown".
    Text: {text}
"""


client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)


SYSTEM_PROMPT = """
    You are a friendly voice assistant. Your responses will
    be spoken aloud using text-to-speech.

    Rules:
    - Keep responses short and conversational (1-3 sentences).
    - Never use markdown, bullet points, code blocks, or special formatting.
    - Avoid abbreviations, URLs, or anything that sounds unnatural when spoken.
    - Use natural spoken language — write how you'd actually talk.
    - If the transcript seems garbled or unclear, politely ask the user to repeat.
    - You have tools available. USE them by making tool calls, do NOT describe or simulate calling them in text.
    - When the user asks about weather, call the get_weather tool. When they ask for a Kanye quote, call the get_kanye_quote tool.
"""


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def extract_city(text):
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[{"role": "user", "content": EXTRACT_CITY_PROMPT.format(text=text)}],
    )
    return response.choices[0].message.content.strip()


def detect_tool_from_text(text):
    lower = text.lower()
    if "weather" in lower:
        city = extract_city(text)
        if city and city.lower() != "unknown":
            result = TOOL_FUNCTIONS["get_weather"](city)
            return f"Here is the weather data for {city}: {result}. Summarize this naturally for the user."
    return None


def main():
    r = sr.Recognizer()
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Voice Assistant ready! Say 'quit' or 'exit' to stop.\n")

    while True:
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            r.pause_threshold = 0.8

            print("🎤 Listening...")

            wave.start()
            audio = r.listen(source)
            wave.stop()

            print("Processing Audio...")

            try:
                stt = r.recognize_google(audio)
            except sr.UnknownValueError:
                print("Couldn't understand, try again.\n")
                continue

            print("You said:", stt)

            if stt.lower().strip() in ("quit", "exit", "stop"):
                print("Goodbye!")
                break

            messages.append({"role": "user", "content": stt})

            response = client.chat.completions.create(
                model=LLM_MODEL,
                messages=messages,
                tools=TOOLS,
            )

            message = response.choices[0].message

            if message.tool_calls:
                messages.append(message)
                for tool_call in message.tool_calls:
                    fn = TOOL_FUNCTIONS[tool_call.function.name]
                    args = json.loads(tool_call.function.arguments)
                    result = fn(**args)
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": result,
                    })

                response = client.chat.completions.create(
                    model=LLM_MODEL,
                    messages=messages,
                )
                ai_response = response.choices[0].message.content
            else:
                tool_result = detect_tool_from_text(stt)
                if tool_result:
                    messages.append({"role": "user", "content": tool_result})
                    response = client.chat.completions.create(
                        model=LLM_MODEL,
                        messages=messages,
                    )
                    ai_response = response.choices[0].message.content
                else:
                    ai_response = message.content

            print("AI:", ai_response, "\n")

            messages.append({"role": "assistant", "content": ai_response})

            p = multiprocessing.Process(target=speak, args=(ai_response,))
            p.start()
            p.join()


if __name__ == "__main__":
    main()
