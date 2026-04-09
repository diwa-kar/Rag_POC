# 📄 PDF Chatbot (RAG-based) – Streamlit App

## 🚀 Overview

This project is a Retrieval-Augmented Generation (RAG) based chatbot that allows users to upload a PDF and interact with it through natural language queries.

The system extracts content from the PDF, converts it into embeddings, stores it in a vector database, retrieves relevant chunks, and generates grounded answers with citations.

---

## 🛠️ Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/diwa-kar/Rag_POC.git
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
# for both front and backend
```

### 3. Set environment variables

Create a `.env` file:

```
OPENAI_API_KEY=your_api_key
```

### 4. Run the application

```bash
# backend
uvicorn app:app --reload
# frontend
streamlit run streamlit_app.py
```

---

## 🧠 System Architecture

### 1. Chunking Strategy

* Used **RecursiveCharacterTextSplitter**
* Chunk size: 600 tokens
* Overlap: 200 tokens
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

* Top-K similarity search (k=20)
* Reason: Ensures relevant context without overwhelming the LLM

---

### 5. RAG Pipeline

* Retrieve relevant chunks
* Construct prompt with:

  * context
  * chat history
  * user query
* Generate grounded response with citations
* gpt-4o-mini model has been used for generation

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
RAG_POC/
│
├── backend/
│   ├── rag/
│   │   ├── ingest.py
│   │   ├── llm.py
│   │   ├── memory.py
│   │   ├── query_rewriter.py
│   │   ├── retriever.py
│   │   ├── utils.py
│   │   ├── __pycache__/
│   │
│   ├── storage/
│   │   ├── index.faiss
│   │   ├── index.pkl
│   │
│   ├── uploads/
│   │   └── <uploaded_pdfs>
│   │
│   ├── app.py
│   ├── .env
│   └── requirements.txt
│
├── frontend/
│   ├── streamlit_app.py
│   └── requirements.txt
│
├── .gitignore
└── README.md
```


## 🎥 Demo

Includes:

* PDF upload
* 5 queries
* citations
* follow-up interaction

---

