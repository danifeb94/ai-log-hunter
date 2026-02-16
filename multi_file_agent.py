import os
from langchain_community.document_loaders import DirectoryLoader, UnstructuredPowerPointLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM
from langchain.chains import RetrievalQA

# Pastikan folder docs ada
if not os.path.exists('./docs'):
    os.makedirs('./docs')
    print("Folder './docs' dibuat. Silakan masukkan file PPTX/TXT Anda ke sana.")

# 1. Load Dokumen (Mendukung TXT dan PPTX)
print("--- Mengindeks dokumen di folder 'docs' (NUC 14 Pro Power)... ---")
loader = DirectoryLoader('./docs', glob="./*", loader_cls=TextLoader) 
# Catatan: Unstructured akan otomatis mendeteksi .pptx jika library sudah terinstal
docs = loader.load()

if not docs:
    print("⚠️ Tidak ada dokumen ditemukan di folder './docs'.")
else:
    # 2. Embedding Lokal (Ringan & Cepat di NUC)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 3. Model Llama 3
    llm = OllamaLLM(model="llama3")

    # 4. Chain Tanya Jawab
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    # 5. Uji Coba Pencarian Berdasarkan File PPTX
    query = "Apa standar penamaan workflow menurut dokumen standardisasi BMC AO?"
    print(f"\nUser: {query}")
    print("-" * 30)
    print("AI: ", qa_chain.run(query))