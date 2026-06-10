from mem0 import Memory
from openai import OpenAI
import json
from dotenv import load_dotenv

LLM_API_KEY = "ollama"
LLM_BASE_URL = "http://localhost:11434"
LLM_MODEL = "mistral:7b"
EMBEDDER_MODEL = "nomic-embed-text:v1.5"

load_dotenv()

client = OpenAI(
    base_url=LLM_BASE_URL + "/v1",
    api_key=LLM_API_KEY,
)

config = {
    "embedder": {
        "provider": "ollama",
        "config": {
            "model": EMBEDDER_MODEL,
            "ollama_base_url": LLM_BASE_URL,
        },
    },
    "llm": {
        "provider": "ollama",
        "config": {
            "model": LLM_MODEL,
            "ollama_base_url": LLM_BASE_URL,
        },
    },
    "vector_store": {
        "provider": "qdrant",
        "config": {
            "host": "localhost",
            "port": 6333,
            "collection_name": "memory",
            "embedding_model_dims": 768,
        },
    },
}

mem_client = Memory.from_config(config)

user_id = "rumon"

while True:
    user_query = input("> ")

    search_result = mem_client.search(
        query=user_query,
        top_k=3,
        filters={"user_id": user_id}
    )

    results = (
        search_result.get("results", search_result)
        if isinstance(search_result, dict)
        else search_result
    )

    memories = [f"ID: {mem.get('id')}\nMemory: {mem.get('memory')}" for mem in results]

    print("Relevant Memories: ", memories)

    SYSTEM_PROMPT = f"""
    You are a helpful assistant. Use the following context to personalize your responses.
    Never mention memories, context, or that you have stored information about the user.
    Speak directly to the user in second person.
    Keep your response to 3 lines or fewer.

    {json.dumps(memories)}
    """

    response = client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_query},
        ],
    )

    ai_response = response.choices[0].message.content

    print("AI: ", ai_response)

    mem_client.add(
        messages=[
            {"role": "user", "content": user_query},
            {"role": "assistant", "content": ai_response},
        ],
        user_id=user_id,
    )

    print("Memory has been saved...")