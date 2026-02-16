import os
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPowerPointLoader, TextLoader
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_classic.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# --- CONFIGURASI & INISIALISASI ---
MODEL_NAME = "llama3"
DOCS_PATH = "./docs"
MEMORY_FILE = "knowledge_base.txt"

print(f"--- Memulai Super Agent di Intel NUC 14 Pro... ---")

# 1. Inisialisasi Model & Tools
llm = OllamaLLM(model=MODEL_NAME)
search = DuckDuckGoSearchRun()
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# 2. Setup RAG (Membaca Dokumen Lokal)
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

print("--- Mengindeks dokumen teknis (PPTX/TXT)... ---")
loader = DirectoryLoader(DOCS_PATH, glob="./*", loader_cls=UnstructuredPowerPointLoader) 
docs = loader.load()

if docs:
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    # Template Persona Senior Engineer & Bahasa Indonesia
    template = """Anda adalah Senior Automation Engineer ahli BMC Atrium Orchestrator.
    Berikan jawaban teknis yang padat dan solutif.
    WAJIB MENJAWAB DALAM BAHASA INDONESIA.
    
    Konteks: {context}
    Pertanyaan: {question}
    Jawaban:"""
    
    QA_PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    local_qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )
else:
    print("⚠️ Folder docs kosong. Agent hanya akan menggunakan Web Search.")
    local_qa = None

# 3. Fungsi Memori Selektif (Menyimpan Fakta)
def update_memory(question, answer):
    summary_prompt = f"Ekstrak fakta teknis singkat dari: T: {question} J: {answer}. Fakta:"
    fact = llm.invoke(summary_prompt).strip()
    with open(MEMORY_FILE, "a") as f:
        f.write(f"- {fact}\n")
    return fact

# 4. Logika Utama Agent
def run_agent(query):
    print(f"\nUser: {query}")
    
    # Langkah A: Cek Dokumen Lokal
    response = ""
    if local_qa:
        res = local_qa.invoke(query)
        response = res['result']
    
    # Langkah B: Jika jawaban lokal tidak memadai, cari di Web
    if not response or "tidak tahu" in response.lower() or "not explicitly" in response.lower():
        print("🌐 Mencari referensi tambahan di internet...")
        web_res = search.run(query)
        # Minta AI merangkum hasil web dalam Bahasa Indonesia
        response = llm.invoke(f"Rangkum ini dalam Bahasa Indonesia sebagai Senior Engineer: {web_res}")
    
    # Langkah C: Simpan ke Memori
    fact_saved = update_memory(query, response)
    
    print(f"AI: {response}")
    print(f"📌 Fakta tersimpan: {fact_saved}")

# --- EKSEKUSI ---
if __name__ == "__main__":
    # Contoh pertanyaan tentang dokumen Standardisasi BMC AO
    run_agent("Apa standar penamaan workflow di Telkomsel AO?")
    
    # Contoh pertanyaan umum teknis (Web Search)
    run_agent("Bagaimana solusi error ORA-12154 pada Oracle 19c?")