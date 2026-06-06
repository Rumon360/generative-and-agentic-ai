from typing_extensions import TypedDict
from typing import Optional, Literal

from langgraph.graph import StateGraph, START, END
from openai import OpenAI

LLM_BASE_URL = "http://localhost:11434/v1"
LLM_API_KEY = "ollama"
LLM_MODEL = "mistral:7b"

client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)


class State(TypedDict):
    user_query: str
    llm_output: Optional[str]
    retries: int


MAX_RETRIES = 3


def chatbot(state: State):
    print("\n\nChatbot:", state)
    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "user",
                "content": state["user_query"],
            }
        ],
    )

    return {
        **state,
        "llm_output": response.choices[0].message.content,
    }


def evaluate_response(
    state: State,
) -> Literal["chatbot", "endnode"]:
    print("\n\nEvaluate:", state)

    if state["retries"] >= MAX_RETRIES:
        return "endnode"

    eval_response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an evaluator.\n"
                    "Return ONLY GOOD or BAD.\n"
                    "GOOD = answer correctly addresses the question.\n"
                    "BAD = answer is incorrect or incomplete."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Question:\n{state['user_query']}\n\n"
                    f"Answer:\n{state['llm_output']}"
                ),
            },
        ],
    )

    verdict = eval_response.choices[0].message.content.strip().upper()

    print("Verdict:", verdict)

    if "GOOD" in verdict:
        return "endnode"

    state["retries"] += 1
    return "chatbot"


def endnode(state: State):
    print("\n\nEndNode:", state)
    return state


graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("endnode", endnode)

graph_builder.add_edge(START, "chatbot")

graph_builder.add_conditional_edges(
    "chatbot",
    evaluate_response,
)

graph_builder.add_edge("endnode", END)

graph = graph_builder.compile()

result = graph.invoke(
    {
        "user_query": "What is 2 + 2?",
        "llm_output": None,
        "retries": 0,
    }
)

print(result["llm_output"])
