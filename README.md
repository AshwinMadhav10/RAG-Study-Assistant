# 📚 SmartStudy RAG Assistant

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Storage-8A2BE2)](https://www.trychroma.com/)
[![LLM](https://img.shields.io/badge/Groq-LLM-orange)](https://groq.com/)
[![Embeddings](https://img.shields.io/badge/HuggingFace-Embeddings-yellow)](https://huggingface.co/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

A **Retrieval-Augmented Generation (RAG)** powered study assistant that transforms your PDFs into **interactive AI knowledge bases**.
Upload course materials, textbooks, or research papers and ask natural language questions — the assistant retrieves and explains answers **directly from your document context**.

---

## 🖥️ Screenshots

### Upload Page (Light Mode)
![Upload Page](https://github.com/user-attachments/assets/6a70724f-14b6-48cd-8f41-155d42348a12)

### Query Page (Light Mode)
![Query Page](https://github.com/user-attachments/assets/d4cbd993-bb46-4528-b21c-2e61b29df4d9)

### Query Page (Dark Mode)
![Dark Mode](https://github.com/user-attachments/assets/f2ba4f73-aa29-4f6c-b04e-dd9262581b36)

---

## 🌍 Overview

The **SmartStudy RAG Assistant** bridges the gap between **traditional PDFs** and **modern AI learning**.
It extracts, embeds, and intelligently queries PDF content — turning static files into searchable, context-aware knowledge systems.

🧠 **Powered by:**

- **FastAPI** for the web backend
- **Groq LLM** for reasoning and contextual question-answering
- **ChromaDB** for vector similarity search
- **HuggingFace Transformers** for high-quality text embeddings

---

## ⚡ Core Highlights

✅ **Smart PDF Uploading** – Categorize files by subject (Physics, Chemistry, Mathematics, Biology, etc.)  
✅ **Text Extraction** – Extracts readable text using `pdfminer.six`  
✅ **Semantic Chunking** – Breaks documents into manageable, meaningful parts  
✅ **Vector Storage** – Embeds and stores chunks using `ChromaDB`  
✅ **Contextual Question Answering** – Powered by `Groq LLM`  
✅ **FastAPI Backend** – Secure and scalable API handling  
✅ **Dark / Light Mode** – One-click theme toggle with localStorage persistence  
✅ **Query History** – Saves your last 5 queries per session for quick reuse  
✅ **Persistent Local Storage** – Saves subjects across browser sessions  
✅ **Real-time Progress Bar** – Visual feedback during PDF upload  

---

## 🧠 Tech Stack

| Layer | Technology | Role |
|-------|-----------|------|
| **Framework** | [FastAPI](https://fastapi.tiangolo.com/) | Backend web API |
| **Language** | Python 3.10+ | Core logic |
| **Embeddings** | [Sentence-Transformers (all-MiniLM-L6-v2)](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2) | Converts text → vector |
| **Vector DB** | [ChromaDB](https://www.trychroma.com/) | Stores document embeddings |
| **LLM API** | [Groq](https://groq.com/) | Generates answers from document context |
| **PDF Parser** | [pdfminer.six](https://pypi.org/project/pdfminer.six/) | Extracts text from PDFs |
| **Frontend** | HTML, CSS, JavaScript | Lightweight responsive UI |
| **Splitter** | [LangChain RecursiveCharacterTextSplitter](https://python.langchain.com/docs/modules/data_connection/document_transformers/) | Text segmentation |

---

## 🧩 System Workflow

### 📥 Upload Flow

1. User uploads a PDF and selects a subject.
2. FastAPI extracts text via `pdfminer.six`.
3. Text is split into chunks (1,000 chars + 150 overlap).
4. Embeddings generated via HuggingFace.
5. Chunks + embeddings stored in ChromaDB under the chosen subject.

### 💬 Query Flow

1. User selects a subject and enters a question.
2. Query is embedded → top-k relevant chunks fetched from ChromaDB.
3. Context + question sent to Groq LLM.
4. Detailed, paragraph-referenced answer returned to the UI.

---

## 📁 Project Structure

```
📦 RAG-Study-Assistant/
├── main.py                 # FastAPI application entry point
├── RAG.py                  # Core RAG logic (extract, embed, query, LLM)
├── templates/
│   ├── index.html          # Upload page (with dark mode & custom subjects)
│   └── query.html          # Query page (with dark mode & query history)
├── static/
│   └── css/
│       └── styles.css      # Purple-themed stylesheet with dark mode support
├── savepdf/                # Uploaded PDFs (git-ignored)
├── vecDB1/                 # Persistent ChromaDB vector store (git-ignored)
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── README.md               # This file
```

---

## 🛠️ Installation Guide

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AshwinMadhav10/RAG-Study-Assistant.git
cd RAG-Study-Assistant
```

### 2️⃣ Create a Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Key

Copy `.env.example` to `.env` and add your Groq API key:

```bash
cp .env.example .env
```

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at [https://console.groq.com](https://console.groq.com).

### 5️⃣ Launch the Application

```bash
uvicorn main:app --reload
```

Access it at 👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧩 Example Use Case

1. **Upload:** `Thermodynamics.pdf` under *Physics*
2. **Query:** "Explain the second law of thermodynamics"
3. **Response:**
   ```
   The second law states that the total entropy of an isolated system always increases...

   (Mentioned in Paragraph 3 of your document)
   ```

---

## 🚀 Key Functions Explained

### `extraction(file_path)`
Extracts and returns plain text from a PDF file using `pdfminer.six`.

### `vectordbadd(text, subject)`
Splits text into 1,000-character chunks (150 overlap), generates embeddings via HuggingFace, and persists them in ChromaDB under the given subject collection.

### `vectordbget(subject, query, top_k=3)`
Splits the user query and retrieves the top-k semantically similar document chunks from ChromaDB.

### `llm(prompt, context)`
Builds a structured prompt combining the retrieved context and user question, then streams a detailed answer from the Groq LLM (`llama3-70b-8192`).

---

## ✨ Changes vs Original

This fork of [HassanCodesIt/RAG-Study-Assistant](https://github.com/HassanCodesIt/RAG-Study-Assistant) includes the following improvements:

| Feature | Original | This Fork |
|---------|----------|-----------|
| Color theme | Blue | **Purple / Indigo** |
| Dark mode | ❌ | ✅ One-click toggle |
| Query history | ❌ | ✅ Last 5 queries, clickable |
| Default subjects | physics, chemistry | **+ mathematics, biology** |
| Footer | ❌ | ✅ Tech-stack footer |
| Page subtitle | ❌ | ✅ Descriptive subtitles |
| LLM model | openai/gpt-oss-20b | **llama3-70b-8192** |
| Code style | Compact | **Typed, documented functions** |
| `.env.example` | ❌ | ✅ Included |
| `.gitignore` | ❌ | ✅ Included |

---

## ⚡ Performance Notes

- Lightweight model (`all-MiniLM-L6-v2`) ensures CPU efficiency.
- Persistent ChromaDB enables quick reloads without re-embedding.
- Streamed Groq responses minimise time-to-first-token.
- Minimal, dependency-free frontend ensures fast load times.

---

## 🔮 Future Enhancements

- Multi-file per subject support
- PDF-level metadata and file tracking
- Authentication for multi-user access
- Support for local models (Ollama / DeepSeek)
- Chat-style conversation memory
- Export answers as PDF/Markdown

---

## 🧾 License

**MIT License © 2025** — Feel free to fork, modify, and expand this project.

---

## 🙌 Acknowledgments

- [LangChain](https://www.langchain.com/)
- [ChromaDB](https://www.trychroma.com/)
- [HuggingFace Transformers](https://huggingface.co/)
- [Groq LLM](https://groq.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [pdfminer.six](https://pypi.org/project/pdfminer.six/)
- Original project by [HassanCodesIt](https://github.com/HassanCodesIt/RAG-Study-Assistant)

> 🧩 *Built with FastAPI, Groq, HuggingFace, and caffeine ☕ — making PDFs talk intelligently.*
