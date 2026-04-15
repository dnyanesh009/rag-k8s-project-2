

# 🚀 AI RAG Platform on Kubernetes (FastAPI + Weaviate + Ollama)

A production-style Retrieval-Augmented Generation (RAG) system built using FastAPI, Weaviate vector database, SentenceTransformers, and Ollama-based local LLMs, deployed with Kubernetes.

This project demonstrates how to design and deploy a scalable AI inference system using modern DevOps and cloud-native practices.

---

## 🧠 Overview

This system enables semantic search and AI-powered responses using a fully local stack (no external API dependency).

It combines:
- Vector search for retrieving relevant context
- Local LLM for generating answers
- Kubernetes for orchestration and scalability

---

## 🏗️ Architecture

```
            ┌───────────────┐
            │     User      │
            └──────┬────────┘
                   │
            ┌──────▼────────┐
            │   FastAPI     │
            │  (RAG API)    │
            └──────┬────────┘
                   │
     ┌─────────────▼─────────────┐
     │ SentenceTransformer       │
     │ (Embedding Model)         │
     └─────────────┬─────────────┘
                   │
            ┌──────▼────────┐
            │   Weaviate    │
            │  Vector DB    │
            └──────┬────────┘
                   │
            ┌──────▼────────┐
            │   Context     │
            └──────┬────────┘
                   │
            ┌──────▼────────┐
            │   Ollama      │
            │  (phi3 LLM)   │
            └──────┬────────┘
                   │
            ┌──────▼────────┐
            │   Response    │
            └───────────────┘
```

---

## ⚙️ Tech Stack

### Backend & AI
- FastAPI (Python API framework)
- SentenceTransformers (Embeddings)
- Ollama (Local LLM runtime)
- phi3 / llama3 (LLM models)

### Data Layer
- Weaviate (Vector database)

### DevOps & Platform
- Docker (Containerization)
- Kubernetes (Deployment & orchestration)
- KIND (Local Kubernetes cluster)

---

## 🚀 Features

- 🔍 Semantic search using vector embeddings  
- 📦 Document storage in Weaviate  
- 🤖 Local LLM inference (no API cost)  
- 🧠 Full RAG pipeline implementation  
- ☸️ Kubernetes-native deployment  
- 📈 Scalable API (replicas + autoscaling)  
- 🔒 Fully local (privacy-first system)  

---

## 📁 Project Structure

```

rag-system/
├── app/
│   ├── main.py
│   ├── requirements.txt
│   ├── Dockerfile
│
├── k8s/
│   ├── api-deployment.yaml
│   ├── api-service.yaml
│   ├── weaviate.yaml
│   ├── ollama.yaml
│
├── README.md

````

---

## 🧱 Setup Instructions

### 1. Clone Repository

```bash
git clone https://github.com/<your-username>/rag-system.git
cd rag-system
````

---

### 🐳 2. Build and Push Docker Image

```bash
docker build -t <your-dockerhub>/rag-api ./app
docker push <your-dockerhub>/rag-api
```

---

### ☸️ 3. Deploy on Kubernetes

Apply all manifests:

```bash
kubectl apply -f k8s/
```

---

### 🔌 4. Access API

```bash
kubectl port-forward svc/rag-api-service 8000:80
```

---

## 🧪 API Usage

### 🔹 Store Document

```bash
curl -X POST http://localhost:8000/store \
-H "Content-Type: application/json" \
-d '{"text": "Kubernetes is a container orchestration system"}'
```

---

### 🔹 Semantic Search

```bash
curl "http://localhost:8000/search?q=Kubernetes"
```

---

### 🔹 Ask AI (RAG)

```bash
curl -G "http://localhost:8000/ask" \
--data-urlencode "q=What is Kubernetes"
```

---

## 📊 Sample Response

```json
{
  "question": "What is Kubernetes?",
  "answer": "Kubernetes is an open-source platform used to manage containerized applications...",
  "context_used": "Kubernetes is a container orchestration system"
}
```

---

## 📈 Scaling & Production Features

### 🔹 Horizontal Scaling

```bash
kubectl scale deployment rag-api --replicas=3
```

---

### 🔹 Autoscaling (HPA)

```bash
kubectl autoscale deployment rag-api --cpu-percent=50 --min=2 --max=5
```

---

### 🔹 Health Checks

* Readiness probe configured for API availability
* Ensures zero-downtime deployments

---

## 💡 Key Engineering Concepts

* Retrieval-Augmented Generation (RAG)
* Vector similarity search
* LLM inference pipelines
* Microservices architecture
* Kubernetes orchestration
* Stateless API design
* Scalable AI infrastructure

---

## 🚀 Future Enhancements

* Helm charts for deployment
* Ingress controller + domain routing
* Prometheus + Grafana monitoring
* GPU-based model serving
* Multi-model routing (OpenAI + local fallback)
* Frontend UI (Chat interface)

---

## 👨‍💻 Author

Dnyanesh More

Senior DevOps / Platform Engineer

---

## ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
