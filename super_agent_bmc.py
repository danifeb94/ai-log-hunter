import os
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPowerPointLoader, TextLoader
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from duckduckgo_search import DDGS 

# --- KONFIGURASI ---
MODEL_NAME = "llama3"
DOCS_PATH = "./docs"
MEMORY_FILE = "knowledge_base.txt"

print(f"--- Memulai Super Agent BMC (NUC 14 Pro) ---")

# 1. Inisialisasi Model & Custom Search
llm = OllamaLLM(model=MODEL_NAME)
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def web_search_custom(query):
    with DDGS() as ddgs:
        results = [r['body'] for r in ddgs.text(query, max_results=3)]
        return "\n".join(results)

# 2. Setup RAG (Logika Multi-Loader yang Diperbaiki)
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

print("--- Mengindeks dokumen teknis secara selektif... ---")
docs = []

# Loader untuk PPTX (Standardisasi BMC)
loader_pptx = DirectoryLoader(DOCS_PATH, glob="**/*.pptx", loader_cls=UnstructuredPowerPointLoader)
docs.extend(loader_pptx.load())

# Loader untuk TXT (Catatan Teknis/Knowledge Base)
loader_txt = DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader)
docs.extend(loader_txt.load())



if docs:
    vectorstore = FAISS.from_documents(docs, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    
    template = """SISTEM: Anda adalah Senior Automation Engineer ahli BMC Atrium Orchestrator. 
    TUGAS: Jawab pertanyaan berdasarkan KONTEKS yang diberikan.
    ATURAN BAHASA: JAWABLAH 100% DALAM BAHASA INDONESIA. 
    DILARANG MENJAWAB DALAM BAHASA INGGRIS meskipun konteksnya berbahasa Inggris. 
    Terjemahkan istilah teknis jika diperlukan, atau gunakan istilah teknis yang umum di Indonesia.

    KONTEKS: {context}
    PERTANYAAN: {question}
    
    JAWABAN (Bahasa Indonesia):"""
    
    QA_PROMPT = PromptTemplate(template=template, input_variables=["context", "question"])
    local_qa = RetrievalQA.from_chain_type(
        llm=llm, 
        chain_type="stuff", 
        retriever=retriever,
        chain_type_kwargs={"prompt": QA_PROMPT}
    )
else:
    print("⚠️ Tidak ada dokumen valid ditemukan.")
    local_qa = None

# 3. Fungsi Memori & Logika Agent
def update_memory(question, answer):
    summary_prompt = f"Ekstrak fakta teknis singkat (max 1 kalimat) dari: T: {question} J: {answer}. Fakta:"
    fact = llm.invoke(summary_prompt).strip()
    with open(MEMORY_FILE, "a") as f:
        f.write(f"- {fact}\n")
    return fact

def run_agent(query):
    print(f"\nUser: {query}")
    response = ""
    
    if local_qa:
        res = local_qa.invoke(query)
        response = res['result']
    
    if not response or "tidak tahu" in response.lower() or "not explicitly" in response.lower():
        print("🌐 Mencari referensi tambahan di internet...")
        try:
            web_res = web_search_custom(query)
            response = llm.invoke(f"Rangkum hasil pencarian ini dalam Bahasa Indonesia dengan gaya Senior Engineer: {web_res}")
        except Exception as e:
            response = f"Maaf, ada kendala koneksi: {e}"
    
    fact_saved = update_memory(query, response)
    print(f"AI: {response}")
    print(f"📌 Fakta teknis baru disimpan ke {MEMORY_FILE}")

# --- EKSEKUSI ---
if __name__ == "__main__":
    run_agent("Apa standar penamaan workflow di Telkomsel AO?")
    run_agent("Bagaimana cara troubleshooting service automation engine yang timeout?")