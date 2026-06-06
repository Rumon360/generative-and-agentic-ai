from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain_ollama import ChatOllama

LLM_BASE_URL = "http://localhost:11434"
LLM_API_KEY = "ollama"
LLM_MODEL = "gemma4:e2b"

llm = ChatOllama(model=LLM_MODEL, base_url=LLM_BASE_URL)


class State(TypedDict):
    messages: Annotated[list, add_messages]


def chatbot(state: State):
    response = llm.invoke(state.get("messages"))
    return {"messages": [response]}


def samplenode(state: State):
    print("\n\nInside samplenode node", state)
    return {"messages": ["Sample message appended"]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("samplenode", samplenode)


graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", "samplenode")
graph_builder.add_edge("samplenode", END)

graph = graph_builder.compile()

updated_state = graph.invoke(
    State({"messages": ["This is a message from the start node"]})
)

print("\n\nUpdated State:", updated_state)
