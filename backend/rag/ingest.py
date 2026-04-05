import os
import pickle
import faiss
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-small"


# ---------------- Embedding ---------------- #

def embed_documents(docs, batch_size=100):
    embeddings = []

    for i in range(0, len(docs), batch_size):
        batch_docs = docs[i:i + batch_size]

        texts = [
            f"Page {doc['page']}: {doc['content']}"
            for doc in batch_docs
        ]

        response = client.embeddings.create(
            model=EMBED_MODEL,
            input=texts
        )

        batch_embeddings = [e.embedding for e in response.data]
        embeddings.extend(batch_embeddings)

    # ✅ CRITICAL FIX
    return np.array(embeddings).astype("float32")


# ---------------- Storage ---------------- #

def store_faiss(docs, embeddings, path="storage/index"):
    dim = embeddings.shape[1]  # should be 1536

    # ✅ Normalize embeddings (critical for cosine similarity)
    faiss.normalize_L2(embeddings)

    # ✅ Use Inner Product (cosine similarity)
    index = faiss.IndexFlatIP(dim)

    index.add(embeddings)

    os.makedirs("storage", exist_ok=True)

    faiss.write_index(index, f"{path}.faiss")

    with open(f"{path}.pkl", "wb") as f:
        pickle.dump(docs, f)