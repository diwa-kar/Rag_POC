import streamlit as st
import requests
import uuid

# Backend URL
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="PDF Chatbot", layout="wide")

# -------------------------------
# Session Initialization
# -------------------------------
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------------------
# Sidebar - PDF Upload
# -------------------------------
st.sidebar.title("📄 Upload PDF")

uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

if st.sidebar.button("Ingest PDF"):
    if uploaded_file is not None:
        with st.spinner("Processing PDF..."):
            files = {"file": uploaded_file.getvalue()}

            response = requests.post(
                f"{BACKEND_URL}/upload",
                files={"file": uploaded_file}
            )

            if response.status_code == 200:
                st.sidebar.success("✅ PDF ingested successfully")
            else:
                st.sidebar.error("❌ Failed to process PDF")
    else:
        st.sidebar.warning("Please upload a PDF first")

# -------------------------------
# Main Chat UI
# -------------------------------
st.title("💬 Chat with your PDF")

# Display chat history
for chat in st.session_state.chat_history:
    with st.chat_message(chat["role"]):
        st.markdown(chat["content"])

        # Show citations if assistant
        if chat["role"] == "assistant" and "sources" in chat:
            with st.expander("📚 Sources"):
                for src in chat["sources"]:
                    st.markdown(
                        f"**Page {src['page']} | {src['chunk_id']}**\n\n"
                        f"{src['snippet']}..."
                    )

# -------------------------------
# Chat Input
# -------------------------------
user_input = st.chat_input("Ask something about the PDF...")

if user_input:
    # Add user message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    with st.spinner("Thinking..."):
        response = requests.post(
            f"{BACKEND_URL}/query",
            params={
                "session_id": st.session_state.session_id,
                "query": user_input
            }
        )

    if response.status_code == 200:
        data = response.json()

        answer = data["answer"]
        sources = data.get("sources", [])

        # Add assistant response
        st.session_state.chat_history.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

        with st.chat_message("assistant"):
            st.markdown(answer)

            if sources:
                with st.expander("📚 Sources"):
                    for src in sources:
                        st.markdown(
                            f"**Page {src['page']} | {src['chunk_id']}**\n\n"
                            f"{src['snippet']}..."
                        )

    else:
        st.error("❌ Error fetching response from backend")