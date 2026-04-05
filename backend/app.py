from fastapi import FastAPI, UploadFile, File
import shutil
import os

from rag.utils import extract_text_from_pdf, chunk_documents
from rag.ingest import embed_documents, store_faiss
from rag.retriever import retrieve
from rag.llm import generate_answer

from rag.memory import add_message, get_history
from rag.query_rewriter import rewrite_query

app = FastAPI()


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_text_from_pdf(file_path)
    docs = chunk_documents(pages)

    embeddings = embed_documents(docs)
    store_faiss(docs, embeddings)

    return {"message": "PDF processed successfully", "chunks": len(docs)}


@app.post("/query")
async def query_pdf(session_id: str, query: str):

    history = get_history(session_id)

    # Rewrite query for better retrieval
    rewritten_query = rewrite_query(query, history)

    contexts = retrieve(rewritten_query, k=10)

    answer = generate_answer(rewritten_query, contexts, history)

    # Store memory
    add_message(session_id, "user", query)
    add_message(session_id, "assistant", answer)

    return {
        "answer": answer,
        "sources": [
            {
                "page": c["page"],
                "snippet": c["content"][:200],
                "chunk_id": c["chunk_id"]
            }
            for c in contexts
        ]
    }