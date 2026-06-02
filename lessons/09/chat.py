from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from openai import OpenAI

llm_base_url = "http://localhost:8080/v1"
qdrant_url = "http://localhost:6333"
llm_model = "google/gemma-4-e4b"
collection_name = "plato-republic.pdf"

embedding_model = OpenAIEmbeddings(
    model="nomic-embed-text-v1.5",
    base_url=llm_base_url,
    api_key="lm-studio",
    check_embedding_ctx_length=False,
)

vector_db = QdrantVectorStore.from_existing_collection(
    url=qdrant_url,
    collection_name=collection_name,
    embedding=embedding_model,
)

openai_client = OpenAI(
    base_url=llm_base_url,
    api_key="lm-studio",
)


def format_result(result) -> str:
    return (
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page_label', 'N/A')}\n"
        f"Source: {result.metadata.get('source', 'N/A')}"
    )


def build_system_prompt(query: str) -> str:
    results = vector_db.similarity_search(query=query, k=5)
    context = "\n\n---\n\n".join(format_result(r) for r in results)

    return f"""
                You are a knowledgeable assistant helping users explore a PDF document.
                Answer the user's question using ONLY the context below. If the answer isn't in the context, say so clearly.
                Always reference the page number(s) where the information was found.
                Be concise and direct.

                Context:
                {context}
            """


print("PDF Chat ready. Type 'exit' to quit.\n")

messages = []

while True:
    user_query = input("You: ").strip()

    if not user_query:
        continue
    if user_query.lower() in ("exit", "quit"):
        break

    messages.append({"role": "user", "content": user_query})

    response = openai_client.chat.completions.create(
        model=llm_model,
        messages=[
            {"role": "system", "content": build_system_prompt(user_query)},
            *messages,
        ],
    )

    answer = response.choices[0].message.content
    messages.append({"role": "assistant", "content": answer})
    print(f"\n🤖: {answer}\n")
