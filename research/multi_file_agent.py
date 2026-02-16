import os
from langchain_classic.chains import RetrievalQA 
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import DirectoryLoader, TextLoader, UnstructuredPowerPointLoader

# Inisialisasi Loader untuk berbagai tipe file
loaders = {
    ".txt": TextLoader,
    ".pptx": UnstructuredPowerPointLoader
}

def create_loader(file_path):
    ext = os.path.splitext(file_path)[1]
    if ext in loaders:
        return loaders[ext](file_path)
    return None

print("--- Mengindeks dokumen di folder 'docs'... ---")
# Load dokumen dari folder docs
docs = []
for file in os.listdir('./docs'):
    loader = create_loader(os.path.join('./docs', file))
    if loader:
        docs.extend(loader.load())

# Setup Vector Store & LLM
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)
llm = OllamaLLM(model="llama3")

# Chain Tanya Jawab menggunakan modul Classic
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever()
)

query = "Apa standar penamaan workflow yang dijelaskan dalam dokumen?"
print(f"\nUser: {query}")
print("AI: ", qa_chain.invoke(query))