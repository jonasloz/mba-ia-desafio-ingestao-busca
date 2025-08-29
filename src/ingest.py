import os
from langchain_postgres import PGVector
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()
for k in ("PDF_PATH", "OPENAI_EMBEDDING_MODEL","OPENAI_API_KEY","PG_VECTOR_COLLECTION_NAME", "DATABASE_URL"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 100
PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    docs = PyPDFLoader(str(PDF_PATH)).load()

    splits = split_docs(docs)
    
    enriched = enrich(splits)    

    ids = [f"doc-{i}" for i in range(len(enriched))]

    store(enriched, ids)

def store(enriched, ids):
    embeddings = OpenAIEmbeddings(model=os.getenv("OPENAI_EMBEDDING_MODEL"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True,
    )

    store.add_documents(documents=enriched, ids=ids)

def enrich(splits):
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in ("", None)}
        )
        for d in splits
    ]
    
    return enriched

def split_docs(docs):
    splits = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP, add_start_index=False).split_documents(docs)
    if not splits:
        raise SystemExit(0)
    return splits


if __name__ == "__main__":
    ingest_pdf()