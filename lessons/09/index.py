from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

pdf_name = "plato-republic.pdf"
pdf_path = Path(__file__).parent / pdf_name

qdrant_url = "http://localhost:6333"
llm_base_url = "http://localhost:8080/v1"

# Load the PDF file
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)

# Vector Embeddings via LM Studio (OpenAI-compatible)
embedding_model = OpenAIEmbeddings(
    model="nomic-embed-text-v1.5",
    base_url=llm_base_url,
    api_key="lm-studio",
    check_embedding_ctx_length=False,
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=qdrant_url,
    collection_name="go-lang-docs",
)

print("Indexing complete!")
