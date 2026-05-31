# Weather Agent — How It Works

## Overview

This agent uses **native function calling** via the OpenAI-compatible Gemini API. Instead of prompting the model to output JSON tool calls as text, we declare tools as structured schemas and let the API handle routing.

---

## Tool Schema

We define what tools exist and what arguments they accept. The model reads the `description` fields to decide when and how to call a tool. When the user asks about weather, the model automatically knows to call `get_weather` and what city to pass.

---

## API Call with Tools

We pass the tool schemas on every API call alongside the message history. `tool_choice="auto"` lets the model decide whether to respond normally or invoke a tool based on the user's message.

---

## Handling the Response

The model signals its intent via `finish_reason`. If it's `"stop"`, the model produced a final text answer and we print it. If it's `"tool_calls"`, the model wants to call one or more tools — we extract the tool name and arguments from the structured `tool_calls` object on the response message.

---

## Executing the Tool

We look up the tool name in `TOOL_MAP` and call the matching Python function with the arguments the model provided. The function hits the `wttr.in` API and returns the current weather as a string.

---

## Sending the Result Back

After executing the tool, we append the result to `messages` using `role="tool"`. The `tool_call_id` links the result back to the specific tool call the model made. We then loop and call the API again — now the model has the real weather data and produces a final answer.

---

## Message History

Every API call includes the full conversation history. This gives the model context across turns and is how it connects the tool result to the original question. The history grows with each turn: system prompt → user message → model's tool request → tool result → model's final answer.

---

## Why Native Function Calling

With the old manual approach, we had to prompt the model to output a specific JSON format, then parse it with regex. This was fragile — the model would sometimes break the format, return `None`, or output multiple JSON objects.

Native function calling eliminates all of that. The tool schema is declared in the API call, the model returns a guaranteed structured `tool_calls` object, and no regex or prompt engineering is needed.
