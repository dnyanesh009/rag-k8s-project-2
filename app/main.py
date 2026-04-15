from fastapi import FastAPI
import weaviate
from sentence_transformers import SentenceTransformer
import requests

app = FastAPI()

# -----------------------------
# Connect to Weaviate
# -----------------------------
client = weaviate.Client(url="http://localhost:8080")

# -----------------------------
# Embedding model (lightweight)
# -----------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# -----------------------------
# Init schema
# -----------------------------
def init_schema():
    try:
        client.schema.get("Document")
    except:
        class_obj = {
            "class": "Document",
            "vectorizer": "none"
        }
        client.schema.create_class(class_obj)

init_schema()

# -----------------------------
# Home
# -----------------------------
@app.get("/")
def home():
    return {"message": "RAG system running (local LLM + Weaviate)"}

# -----------------------------
# Store documents
# -----------------------------
@app.post("/store")
def store(data: dict):
    vector = model.encode(data["text"]).tolist()

    client.data_object.create(
        {"text": data["text"]},
        "Document",
        vector=vector
    )

    return {"status": "stored"}

# -----------------------------
# Search (vector DB only)
# -----------------------------
@app.get("/search")
def search(q: str):
    vector = model.encode(q).tolist()

    result = client.query.get("Document", ["text"]) \
        .with_near_vector({"vector": vector}) \
        .with_limit(3) \
        .do()

    return result


# -----------------------------
# Local LLM function (Ollama)
# -----------------------------
def ask_local_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3",   # ⚡ lightweight model
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]

# -----------------------------
# RAG endpoint
# -----------------------------
@app.get("/ask")
def ask(q: str):

    # 1. Convert query → vector
    vector = model.encode(q).tolist()

    # 2. Retrieve relevant docs
    result = client.query.get("Document", ["text"]) \
        .with_near_vector({"vector": vector}) \
        .with_limit(3) \
        .do()

    docs = result["data"]["Get"]["Document"]

    context = "\n".join([d["text"] for d in docs])

    # 3. Build prompt
    prompt = f"""
You are a helpful assistant.

Use ONLY the context below to answer:

Context:
{context}

Question:
{q}

Answer clearly:
"""

    # 4. Call local LLM (phi3)
    answer = ask_local_llm(prompt)

    return {
        "question": q,
        "answer": answer,
        "context_used": context
    }