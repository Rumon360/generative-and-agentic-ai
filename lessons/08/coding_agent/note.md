# Coding Agent — How It Works

## Overview

This is a ReAct-style AI agent that can execute shell commands and write files on your system. It works by sending messages back and forth with a local LLM (via LM Studio), following a PLAN → OBSERVE → OUTPUT loop until the task is complete.

---

## Tools

The agent has two tools the model can invoke:

**`run_command(cmd)`** — runs a shell command via `subprocess` and returns the output. The `cwd` variable pins every command to the directory where the script was launched, since `cd` does not persist between subprocess calls.

**`write_file(path, content)`** — writes a file to disk using Python's `open()`. Automatically creates parent directories. This is used instead of `echo` because `echo` on Windows cmd.exe does not handle `\n` as real newlines.

---

## System Prompt

Instructs the model to respond with exactly one JSON object per turn, in one of three formats:

- **Planning step** — model thinks out loud, no tool called
- **Tool call** — model requests a tool with arguments
- **Output** — model gives the final answer to the user

The prompt also tells the model to stop after each tool call and wait for the result before continuing.

---

## `parse_response`

Since the model may wrap its JSON in markdown code fences or add text before/after it, `parse_response` extracts the first valid JSON object using balanced brace matching rather than a simple `json.loads`. This makes parsing resilient to model formatting quirks.

---

## Main Loop

The loop runs up to `MAX_ITERATIONS` times. Each iteration:

1. Calls the LLM with the current message history
2. Strips and validates the response
3. Parses the first JSON object from the response
4. Appends the assistant message to history
5. If `step == "OUTPUT"` → prints final answer and exits
6. If `"tool" in step` → calls the tool, prints the result, appends it as a user `OBSERVE` message, and loops
7. If neither → it's a plain planning step, appended to history, and loops

The retry block around the API call handles rate limit errors (HTTP 429) by waiting and retrying up to 3 times before exiting.

---

## Message History

Every message (system, user, assistant, observations) is kept in `messages` and sent on every API call. This gives the model full context of what has happened so far — what was planned, what tools ran, and what they returned.

---

## Example Flow

```
User: create a todo app in a todo_app folder

→ PLAN: "I will create the files using write_file"
→ PLAN + tool: write_file("todo_app/index.html", "...")
   OBSERVE: File written: .../todo_app/index.html (1243 bytes)
→ PLAN + tool: write_file("todo_app/style.css", "...")
   OBSERVE: File written: .../todo_app/style.css (890 bytes)
→ PLAN + tool: write_file("todo_app/script.js", "...")
   OBSERVE: File written: .../todo_app/script.js (2105 bytes)
→ OUTPUT: "I've created the todo app in the todo_app folder..."
```
