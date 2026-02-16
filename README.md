# 🚀 AI Log Hunter: Super Agent BMC
**Asisten AI Lokal Berbasis RAG untuk Otomasi & Manajemen Pengetahuan**

`AI Log Hunter` telah berevolusi dari sekadar alat pencari log menjadi **Super Agent** berbasis RAG (Retrieval-Augmented Generation). Proyek ini dirancang untuk berjalan 100% secara lokal pada **Intel NUC 14 Pro (Core Ultra 5)** menggunakan model **Llama 3** melalui Ollama, memastikan keamanan data teknis internal tetap terjaga.



## 🌟 Fitur Utama
* **Multi-Format RAG Engine**: Mampu mengekstraksi dan memahami informasi dari dokumen standardisasi dalam format `.pptx` (PowerPoint) dan `.txt` menggunakan FAISS Vector Database.
* **Hybrid Search Intelligence**: Agent secara otomatis melakukan fallback ke **Web Search (DuckDuckGo)** jika informasi tidak ditemukan di dokumen lokal.
* **Selective Persistent Memory**: AI secara cerdas meringkas fakta teknis dari percakapan dan menyimpannya ke `knowledge_base.txt` untuk referensi instan di masa depan.
* **Senior Engineer Persona**: Dikonfigurasi dengan instruksi sistem untuk merespon dalam Bahasa Indonesia dengan gaya **Senior Automation Engineer** yang solutif.
* **Privacy-First Design**: Memanfaatkan indexing lokal sehingga dokumen sensitif tidak pernah keluar ke jaringan internet publik.

## 🛠️ Tech Stack
* **LLM Engine**: Ollama (Llama 3)
* **Framework**: LangChain (Core, Classic, & Community)
* **Vector DB**: FAISS (Facebook AI Similarity Search)
* **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
* **Hardware Optimization**: Intel NUC 14 Pro (Core Ultra 5 125H)

## 📂 Struktur Proyek
- `super_agent_bmc.py`: Script inti integrasi RAG, Web Search, dan Memory.
- `docs/`: (Ignored) Folder untuk penyimpanan dokumen teknis internal.
- `knowledge_base.txt`: (Ignored) Basis pengetahuan dinamis hasil ekstraksi AI.
- `ai-env/`: (Ignored) Lingkungan virtual Python 3.13.

## 🚀 Cara Menjalankan
1. Aktifkan virtual environment: `.\ai-env\Scripts\activate`
2. Pastikan dokumen teknis Anda berada di folder `docs/`.
3. Jalankan Agent: `python .\super_agent_bmc.py`



## 📈 Roadmap
- [x] Implementasi RAG untuk file PowerPoint (.pptx).
- [x] Integrasi Web Search Fallback (DuckDuckGo).
- [x] Fitur Persistent Memory (Fakta Teknis Otomatis).
- [ ] **Next Step**: Membangun Dashboard Web menggunakan Streamlit.