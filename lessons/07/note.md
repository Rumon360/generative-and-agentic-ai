## Prompt Styles

Prompt styles define **how you structure instructions** when interacting with a Large Language Model (LLM). A well-structured prompt improves clarity, control, and output quality.

---

## Types of Prompting

1. **Alpaca** – Instruction-based format used in Meta’s LLaMA ecosystem
2. **ChatML** – Role-based conversational format
3. **Instruct** – Minimal instruction → response format

---

## 1. Alpaca Prompt Format

```text
### Instruction:
<SYSTEM_PROMPT>

### Input:
<USER_QUERY>

### Response:
<MODEL_OUTPUT>
```

### Explanation

- **Instruction**: Defines the task or behavior
- **Input**: User query or additional context
- **Response**: Model’s output

---

## 2. ChatML Prompt Format

ChatML is designed for **multi-turn conversations** and separates messages by roles.

```text
<|system|>
<SYSTEM_PROMPT>

<|user|>
<USER_QUERY>

<|assistant|>
<MODEL_OUTPUT>
```

### Explanation

- **system**: Sets behavior, tone, or rules for the model
- **user**: Contains the user’s message or query
- **assistant**: The model’s reply

### Notes

- Supports **multi-turn dialogue** by repeating user/assistant blocks
- Widely used in chat-based AI systems
- Helps maintain **context and conversation flow**

---

## 3. Instruct Prompt Format

The simplest and most direct format, often used in early instruction-tuned models.

```text
Instruction: <TASK_DESCRIPTION>
Response: <MODEL_OUTPUT>
```

### Example

```text
Instruction: Summarize the following paragraph.
Response: <MODEL_OUTPUT>
```

### Explanation

- **Instruction**: Clearly states the task
- **Response**: Expected output from the model

### Notes

- Minimal structure
- Best for **single-turn tasks**
- Easy to use but less flexible than ChatML
