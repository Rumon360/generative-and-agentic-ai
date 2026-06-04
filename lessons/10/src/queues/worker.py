from openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from ..config import (
    LLM_BASE_URL,
    LLM_API_KEY,
    LLM_MODEL,
    EMBEDDING_MODEL,
    QDRANT_URL,
    COLLECTION_NAME,
)

openai_client = OpenAI(
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
)

embedding_model = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    check_embedding_ctx_length=False,
)

_vector_db = None


def get_vector_db():
    global _vector_db
    if _vector_db is None:
        _vector_db = QdrantVectorStore.from_existing_collection(
            url=QDRANT_URL,
            collection_name=COLLECTION_NAME,
            embedding=embedding_model,
        )
    return _vector_db


def format_result(result) -> str:
    return (
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page_label', 'N/A')}\n"
        f"Source: {result.metadata.get('source', 'N/A')}"
    )


def build_system_prompt(query: str) -> str:
    results = get_vector_db().similarity_search(query=query, k=5)
    context = "\n\n---\n\n".join(format_result(r) for r in results)

    return f"""
                You are a knowledgeable assistant helping users explore a PDF document.
                Answer the user's question using ONLY the context below. If the answer isn't in the context, say so clearly.
                Always reference the page number(s) where the information was found.
                Be concise and direct.

                Context:
                {context}
            """


def process_query(query: str):
    print(f"Processing query: {query}")
    system_prompt = build_system_prompt(query)

    response = openai_client.chat.completions.create(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    )
    print(f"Raw response: {response}")
    content = response.choices[0].message.content or ""
    print(f"Response: {content}")
    return content
