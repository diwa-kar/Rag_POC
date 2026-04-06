# 📄 PDF Chatbot (RAG-based) – Streamlit App

## 🚀 Overview

This project is a Retrieval-Augmented Generation (RAG) based chatbot that allows users to upload a PDF and interact with it through natural language queries.

The system extracts content from the PDF, converts it into embeddings, stores it in a vector database, retrieves relevant chunks, and generates grounded answers with citations.

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-link>
cd <repo-name>
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key
```

### 4. Run the application

```bash
streamlit run app.py
```

---

## 🧠 System Architecture

### 1. Chunking Strategy

* Used **RecursiveCharacterTextSplitter**
* Chunk size: ~500–800 tokens
* Overlap: ~50–100 tokens
* Reason: Maintains context continuity while optimizing retrieval

---

### 2. Embeddings

* Model: `text-embedding-3-small` (OpenAI)
* Dimension: 1536
* Reason: Good balance between performance and cost

---

### 3. Vector Database

* Used: FAISS
* Storage: Local (`./storage/`)
* Reason: Fast similarity search and easy local setup

---

### 4. Retrieval Strategy

* Top-K similarity search (k=3–5)
* Reason: Ensures relevant context without overwhelming the LLM

---

### 5. RAG Pipeline

* Retrieve relevant chunks
* Construct prompt with:

  * context
  * chat history
  * user query
* Generate grounded response with citations

---

### 6. Conversation Memory

* Maintained using Streamlit session state
* Chat history appended and passed in prompt
* Enables follow-up question handling

---

## 💬 Features

* Upload and process any PDF
* Chat interface with history
* Context-aware answers
* Source citations (page + chunk)
* Handles follow-up questions
* Graceful handling of irrelevant queries

---

## ⚠️ Known Limitations

* Complex PDFs (tables/images) may lose structure
* Long documents may need better chunking strategies
* No reranking (can be improved)
* Depends on embedding quality

---

## 📊 Optional Evaluation

Tested with 5–10 questions:

* Retrieval accuracy: High
* Citation correctness: Verified manually
* Follow-up handling: Works as expected

---

## 📁 Folder Structure

```
.
├── app.py
├── backend/
├── storage/
├── requirements.txt
└── README.md
```

---

## 🎥 Demo

Includes:

* PDF upload
* 5+ queries
* citations
* follow-up interaction

---

## 🧾 Prompt Logs

Attached separately as required.

---
