import fitz  # PyMuPDF
from langchain_text_splitters import RecursiveCharacterTextSplitter

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text()
        pages.append({"text": text, "page": i + 1})

    return pages

def chunk_documents(pages):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=200
    )

    docs = []

    for page in pages:
        chunks = splitter.split_text(page["text"])

        for i, chunk in enumerate(chunks):  # 👈 ADD enumerate here
            docs.append({
                "content": chunk,
                "page": page["page"],
                "chunk_id": f"p{page['page']}_c{i}"  # 👈 ADD THIS
            })

    return docs