import speech_recognition as sr
import multiprocessing
import pyttsx3
from utils import wave
from openai import OpenAI

LLM_API_KEY = "ollama"
LLM_BASE_URL = "http://localhost:11434/v1"
LLM_MODEL = "mistral:7b"


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
"""


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


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
            )

            ai_response = response.choices[0].message.content
            print("AI:", ai_response, "\n")

            messages.append({"role": "assistant", "content": ai_response})

            p = multiprocessing.Process(target=speak, args=(ai_response,))
            p.start()
            p.join()


if __name__ == "__main__":
    main()
