import os
import ssl
import streamlit as st
import pytesseract
from PIL import Image
from fpdf import FPDF
from datetime import datetime

# --- 1. KONFIGURASI TESSERACT OCR ---
# Pastikan path ini sesuai dengan lokasi instalasi di Windows Anda
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- 2. BYPASS SSL & HUGGINGFACE FIX ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

os.environ['CURL_CA_BUNDLE'] = ''

# --- 3. IMPORT LIBRARIES AI ---
from langchain_ollama import OllamaLLM
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import (
    DirectoryLoader, UnstructuredPowerPointLoader, 
    TextLoader, PyPDFLoader, Docx2txtLoader, UnstructuredExcelLoader
)
from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from duckduckgo_search import DDGS

# --- 4. TEMPLATE LAPORAN RCA (PROFESSIONAL) ---
class RCA_Report(FPDF):
    def header(self):
        self.set_font("Arial", "B", 15)
        self.cell(0, 10, "Laporan Root Cause Analysis (RCA)", ln=True, align="C")
        self.set_font("Arial", "I", 9)
        self.cell(0, 10, "Dihasilkan oleh: Super Agent BMC (Intel NUC 14 Pro)", ln=True, align="C")
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Halaman {self.page_no()}", align="C")

    def chapter_title(self, title):
        self.set_font("Arial", "B", 12)
        self.set_fill_color(200, 220, 255)
        self.cell(0, 10, title, ln=True, align="L", fill=True)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 7, body)
        self.ln(5)

# --- 5. KONFIGURASI DASHBOARD ---
st.set_page_config(page_title="Super Agent BMC - Final", page_icon="🤖", layout="wide")
DOCS_PATH = "./docs"
if not os.path.exists(DOCS_PATH):
    os.makedirs(DOCS_PATH)

@st.cache_resource
def load_llm():
    return OllamaLLM(model="llama3")

@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

def build_vectorstore():
    embeddings = load_embeddings()
    loaders = [
        DirectoryLoader(DOCS_PATH, glob="**/*.pptx", loader_cls=UnstructuredPowerPointLoader),
        DirectoryLoader(DOCS_PATH, glob="**/*.txt", loader_cls=TextLoader),
        DirectoryLoader(DOCS_PATH, glob="**/*.pdf", loader_cls=PyPDFLoader),
        DirectoryLoader(DOCS_PATH, glob="**/*.docx", loader_cls=Docx2txtLoader),
        DirectoryLoader(DOCS_PATH, glob="**/*.xlsx", loader_cls=UnstructuredExcelLoader)
    ]
    docs = []
    for loader in loaders:
        try: docs.extend(loader.load())
        except: pass
    return FAISS.from_documents(docs, embeddings) if docs else None

# --- 6. SIDEBAR: KONTROL ---
with st.sidebar:
    st.header("🤖 Control Panel")
    st.info(f"User: Dani\nDevice: Intel NUC 14 Pro")
    
    st.divider()
    st.subheader("📁 Database Knowledge")
    uploaded_files = st.file_uploader(
        "Upload Dokumen/Log (PDF, PPTX, IMG, dll)", 
        type=["pptx", "pdf", "docx", "xlsx", "txt", "jpg", "png", "jpeg"],
        accept_multiple_files=True
    )
    
    if st.button("Sync Knowledge"):
        if uploaded_files:
            for f in uploaded_files:
                if f.type.startswith("image/"):
                    st.session_state.last_image = f
                else:
                    with open(os.path.join(DOCS_PATH, f.name), "wb") as out:
                        out.write(f.getbuffer())
            st.success("Sinkronisasi Berhasil!")
            st.session_state.vectorstore = build_vectorstore()
            st.rerun()

# --- 7. CHAT UI ---
st.title("🤖 Super Agent BMC")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = build_vectorstore()
if "last_image" not in st.session_state:
    st.session_state.last_image = None

if st.session_state.last_image:
    with st.expander("🖼️ Log Screenshot Aktif", expanded=True):
        st.image(st.session_state.last_image, use_container_width=True)

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- 8. LOGIKA PROSES & EXPORT ---
if prompt := st.chat_input("Tanyakan tentang log atau dokumen..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Menganalisis..."):
            response = ""
            
            # OCR + LLM Hybrid Analysis
            if st.session_state.last_image and ("gambar" in prompt.lower() or "log" in prompt.lower()):
                img = Image.open(st.session_state.last_image)
                extracted_text = pytesseract.image_to_string(img, config='--psm 6')
                
                analysis_prompt = f"""Anda Senior Automation Engineer. Analisis log ini:
{extracted_text}
Pertanyaan: {prompt}
Format: 1. DETAIL TEMUAN, 2. ANALISIS LOGIKA, 3. LANGKAH PERBAIKAN, 4. CATATAN KEAMANAN."""
                response = load_llm().invoke(analysis_prompt)
            
            # RAG Analysis
            elif st.session_state.vectorstore:
                retriever = st.session_state.vectorstore.as_retriever(search_kwargs={"k": 3})
                qa_chain = RetrievalQA.from_chain_type(
                    llm=load_llm(), chain_type="stuff", retriever=retriever,
                    chain_type_kwargs={"prompt": PromptTemplate(template="Context: {context}\nQ: {question}\nAns:", input_variables=["context", "question"])}
                )
                response = qa_chain.invoke(prompt)['result']

            # Web Search Fallback
            if not response or "tidak tahu" in response.lower():
                with DDGS() as ddgs:
                    web_res = [r['body'] for r in ddgs.text(prompt, max_results=3)]
                response = load_llm().invoke(f"Rangkum hasil web ini dalam Bahasa Indonesia: {' '.join(web_res)}")

            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})

            # --- FITUR EXPORT PDF (STABLE VERSION) ---
            st.divider()
            try:
                pdf = RCA_Report()
                pdf.add_page()
                pdf.chapter_title("Hasil Analisis Root Cause Analysis")
                
                # Pembersihan teks untuk PDF
                clean_text = response.encode('latin-1', 'replace').decode('latin-1')
                pdf.chapter_body(clean_text)
                
                pdf.set_font("Arial", "I", 8)
                pdf.cell(0, 10, f"Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", ln=True)
                
                # FIX: Konversi bytearray ke bytes murni agar Streamlit menerima data
                pdf_output = bytes(pdf.output()) 
                
                st.download_button(
                    label="📥 Download Laporan RCA (PDF)",
                    data=pdf_output,
                    file_name=f"RCA_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="final_pdf_download"
                )
            except Exception as e:
                st.error(f"Gagal membuat PDF: {e}")