# 🚀 AI Log Hunter: Super Agent BMC
**Asisten AI Lokal Berbasis RAG untuk Otomasi & Manajemen Pengetahuan**

`AI Log Hunter` adalah sistem asisten cerdas yang berevolusi dari pencari log menjadi mesin pencari pengetahuan teknis (Knowledge Management). Proyek ini dioptimalkan untuk berjalan secara lokal di **Intel NUC 14 Pro (Core Ultra 5)** menggunakan model **Llama 3** untuk menjamin keamanan data.



## 🌟 Fitur Utama
* **Multi-Format RAG (Retrieval-Augmented Generation)**: Mampu membedah dan memahami dokumen standardisasi internal dalam format `.pptx` (PowerPoint) dan `.txt`.
* **Hybrid Search Intelligence**: Agent secara otomatis beralih ke pencarian web (DuckDuckGo) jika solusi tidak ditemukan dalam basis data dokumen lokal.
* **Selective Persistent Memory**: AI secara mandiri mengekstrak fakta teknis penting dari percakapan dan menyimpannya ke dalam `knowledge_base.txt` untuk pembelajaran kontinu.
* **Senior Engineer Persona**: Diprogram dengan instruksi sistem untuk bertindak sebagai **Senior Automation Engineer** yang memberikan solusi teknis dalam Bahasa Indonesia.
* **Privacy Focused**: Seluruh proses indexing dan inferensi dilakukan 100% secara lokal, memastikan dokumen sensitif tidak pernah keluar dari infrastruktur pribadi.

## 🛠️ Tech Stack
* **LLM Engine**: [Ollama](https://ollama.com/) (Llama 3).
* **Framework**: LangChain (Core, Classic, & Community).
* **Vector Database**: FAISS (Facebook AI Similarity Search).
* **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`.
* **Compute**: Intel NUC 14 Pro (Core Ultra 5 125H).

## 📂 Struktur Proyek
- `docs/`: Penyimpanan dokumen teknis internal (Standardisasi & Manual).
- `super_agent_bmc.py`: Script utama yang mengintegrasikan RAG, Web Search, dan Memory.
- `knowledge_base.txt`: Basis pengetahuan yang dibangun secara otomatis oleh AI.
- `ai-env/`: Lingkungan virtual Python 3.13 terisolasi.

## 🚀 Cara Penggunaan
1. Aktifkan environment: `.\ai-env\Scripts\activate`
2. Pastikan dokumen teknis sudah ada di folder `docs/`.
3. Jalankan agent: `python .\super_agent_bmc.py`

## 📈 Roadmap
- [x] Integrasi pembaca file PowerPoint (.pptx).
- [x] Fitur pencarian web otomatis sebagai fallback.
- [x] Implementasi memori teknis berkelanjutan.
- [ ] **Next**: Implementasi Web UI menggunakan Streamlit.