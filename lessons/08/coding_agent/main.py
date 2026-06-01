import json
import os
import re
import subprocess
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key="lm-studio",
    base_url="http://localhost:8080/v1",
)

cwd = os.getcwd()


def run_command(cmd: str) -> str:
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=30, cwd=cwd
        )
        output = (result.stdout + result.stderr).strip()
        return output if output else "(no output)"
    except subprocess.TimeoutExpired:
        return "Error: command timed out"
    except Exception as e:
        return f"Error: {str(e)}"


def write_file(path: str, content: str) -> str:
    full_path = os.path.join(cwd, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {full_path} ({len(content)} bytes)"


available_tools = {
    "run_command": run_command,
    "write_file": write_file,
}


SYSTEM_PROMPT = """
You are an expert AI assistant that resolves user queries step by step.

You work in steps: PLAN then OUTPUT.
- PLAN: Think about what to do, or call a tool. Can repeat multiple times.
- OUTPUT: Give the final answer. Only once, when done.

CRITICAL: Return EXACTLY one JSON object per response. Never return multiple.

Available tools:
- run_command(cmd: str): Executes a shell command on the user's Windows system. Use Windows commands (mkdir, dir, etc). Do NOT use 'cd' alone — it does not persist between calls. Use full paths or combined commands instead (e.g. "mkdir todo_app").
- write_file(path: str, content: str): Writes content to a file. Creates parent directories automatically (no need to mkdir first). Always use this for creating files. Never use 'echo' or 'run_command' to write files.

JSON formats:

Planning:
{"step": "PLAN", "content": "what you are thinking"}

Run a command:
{"step": "PLAN", "tool": "run_command", "arguments": {"cmd": "mkdir todo_app"}}

Create a file:
{"step": "PLAN", "tool": "write_file", "arguments": {"path": "todo_app/index.html", "content": "<!DOCTYPE html>..."}}

Final answer:
{"step": "OUTPUT", "content": "your answer here"}

Rules:
- Return EXACTLY one JSON object per response
- After every tool call, STOP and wait for the OBSERVE response
- Never fabricate OBSERVE results
- Never skip ahead — one step at a time
"""


MAX_ITERATIONS = 25


def parse_response(raw: str) -> dict:
    raw = re.sub(r"```(?:json)?", "", raw).strip()
    for match in re.finditer(r"\{", raw):
        start = match.start()
        depth = 0
        for i, ch in enumerate(raw[start:], start):
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(raw[start : i + 1])
                    except json.JSONDecodeError:
                        pass
                    break
    return json.loads(raw)

messages = [{"role": "system", "content": SYSTEM_PROMPT}]

user_query = input("> ")

messages.append({"role": "user", "content": f"START: {user_query}"})

for _ in range(MAX_ITERATIONS):
    content = ""
    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="google/gemma-4-e4b",
                messages=messages,
            )
            content = (response.choices[0].message.content or "").strip()
            if content:
                break
            print(f"\n⚠️ Empty response, retrying ({attempt + 1}/3)...")
        except Exception as e:
            if "429" in str(e) and attempt < 2:
                wait = 10 * (attempt + 1)
                print(f"\n⏳ Rate limited. Retrying in {wait}s...")
                time.sleep(wait)
            else:
                print(f"\n❌ API error: {e}")
                exit(1)

    if not content:
        print("\n❌ Model returned no content")
        break

    print(f"\nAssistant:\n{content}")

    try:
        step = parse_response(content)
    except (json.JSONDecodeError, ValueError):
        print("\n❌ Model returned invalid response")
        break

    messages.append({"role": "assistant", "content": content})

    if step["step"] == "OUTPUT":
        print(f"\n🤖: {step['content']}")
        break

    if "tool" in step:
        tool_name = step["tool"]
        tool_args = step.get("arguments", {})

        if tool_name not in available_tools:
            print(f"\n❌ Unknown tool: {tool_name}")
            break

        observation = available_tools[tool_name](**tool_args)

        print(f"\nOBSERVE:\n{observation}")

        messages.append({"role": "user", "content": f"OBSERVE:\n{observation}"})
else:
    print(f"\n❌ Reached max iterations ({MAX_ITERATIONS})")
