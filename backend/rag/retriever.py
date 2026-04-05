import faiss
import pickle
import numpy as np
from openai import OpenAI
import os
from dotenv import load_dotenv
from sentence_transformers import CrossEncoder

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_MODEL = "text-embedding-3-small"

# Cross-encoder reranker (high impact)
reranker = CrossEncoder("BAAI/bge-reranker-base")


# ---------------- Load Index ---------------- #

def load_index(path="storage/index"):
    index = faiss.read_index(f"{path}.faiss")

    with open(f"{path}.pkl", "rb") as f:
        docs = pickle.load(f)

    return index, docs


# ---------------- Query Embedding ---------------- #

def embed_query(query):
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=[query]
    )

    vec = np.array([response.data[0].embedding]).astype("float32")

    # Normalize for cosine similarity
    faiss.normalize_L2(vec)

    return vec


# ---------------- Reranking ---------------- #

def rerank(query, docs):
    pairs = [(query, d["content"]) for d in docs]

    scores = reranker.predict(pairs)

    ranked = sorted(zip(docs, scores), key=lambda x: x[1], reverse=True)

    return [doc for doc, _ in ranked]


# ---------------- Retrieval ---------------- #

def retrieve(query, k=10):
    index, docs = load_index()

    query_vec = embed_query(query)

    # Step 1: Get larger candidate pool
    D, I = index.search(query_vec, 50)

    candidate_docs = [docs[i] for i in I[0] if i < len(docs)]

    # Step 2: Rerank candidates (major improvement)
    reranked_docs = rerank(query, candidate_docs)

    # Step 3: Return top-k
    return reranked_docs[:k]