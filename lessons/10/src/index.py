from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from src.config import LLM_BASE_URL, LLM_API_KEY, EMBEDDING_MODEL, QDRANT_URL, COLLECTION_NAME

pdf_path = Path(__file__).parent.parent / COLLECTION_NAME

# Load the PDF file
loader = PyPDFLoader(file_path=str(pdf_path))
docs = loader.load()

# Split the docs into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)
chunks = text_splitter.split_documents(documents=docs)

# Vector Embeddings via LM Studio (OpenAI-compatible)
embedding_model = OpenAIEmbeddings(
    model=EMBEDDING_MODEL,
    base_url=LLM_BASE_URL,
    api_key=LLM_API_KEY,
    check_embedding_ctx_length=False,
)

vector_store = QdrantVectorStore.from_documents(
    documents=chunks,
    embedding=embedding_model,
    url=QDRANT_URL,
    collection_name=COLLECTION_NAME,
)

print("Indexing complete!")
