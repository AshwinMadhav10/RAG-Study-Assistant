import os
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
from groq import Groq
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings

# Load environment variables
load_dotenv()

# Initialize global singletons
chroma_client = chromadb.PersistentClient(path="./vecDB1")
embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")


def extraction(file_path: str) -> str:
    """Extract and return plain text from a PDF file."""
    text = extract_text(file_path)
    return text


def vectordbadd(text: str, subject: str) -> list[str]:
    """Chunk text, embed it, and store in ChromaDB under the given subject."""
    collection = chroma_client.get_or_create_collection(name=subject)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    chunks = splitter.split_text(text)

    embeddings = embedder.embed_documents(chunks)

    existing = len(collection.get()["ids"])
    ids = [f"id{existing + i + 1}" for i in range(len(chunks))]

    collection.add(embeddings=embeddings, documents=chunks, ids=ids)
    return ids


def vectordbget(subject: str, query: str, top_k: int = 3) -> list[str]:
    """Retrieve the top-k most relevant chunks for a query from ChromaDB."""
    collection = chroma_client.get_or_create_collection(name=subject)
    query_embedding = embedder.embed_query(query)
    results = collection.query(query_embeddings=[query_embedding], n_results=top_k)
    return results["documents"][0]


def llm(prompt: str, context: list[str]) -> str:
    """Generate a detailed, context-aware answer using Groq LLM."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    content = (
        "Answer the following question using only the data below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {prompt}\n\n"
        "Instructions:\n"
        "- If the question is unrelated to the provided context, reply with something like "
        "'This question is outside the scope of the uploaded document.'\n"
        "- Provide a detailed and elaborated answer.\n"
        "- Mention where the information is found (e.g., Paragraph 3, Line 6) in brackets "
        "on a new line after the answer.\n"
        "- Avoid using markdown formatting.\n\n"
        "Answer:"
    )

    completion = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[{"role": "user", "content": content}],
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True,
    )

    full_answer = ""
    for chunk in completion:
        full_answer += chunk.choices[0].delta.content or ""
    return full_answer
