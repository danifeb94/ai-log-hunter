# 🤖 Super Agent BMC: Local RAG with OCR & Vision

Asisten AI cerdas berbasis lokal yang dirancang khusus untuk membantu **Automation Developer** dalam menganalisis dokumen teknis dan log sistem (seperti BMC Atrium Orchestrator) secara cepat, akurat, dan 100% private.

## 🚀 Fitur Utama
- **Hybrid OCR + LLM**: Menganalisis log dari screenshot terminal/GUI dengan presisi tinggi menggunakan Tesseract OCR & Llama 3.
- **Multi-Format RAG**: Mendukung pembacaan dokumen teknis dalam format PDF, PPTX, DOCX, XLSX, dan TXT.
- **Automated RCA Report**: Menghasilkan laporan *Root Cause Analysis* (RCA) profesional dalam format PDF hanya dengan satu klik.
- **Privacy First**: Seluruh proses berjalan secara lokal di perangkat (Tested on Intel NUC 14 Pro) menggunakan Ollama.

## 🛠️ Tech Stack
- **Framework**: Streamlit, LangChain
- **AI Engine**: Ollama (Llama 3, Llava)
- **Vector DB**: FAISS
- **OCR Engine**: Tesseract OCR
- **Document Processing**: fpdf2, openpyxl, python-docx

## 📋 Struktur Laporan RCA
Setiap analisis log secara otomatis dibagi menjadi 4 bagian standar industri:
1. **Detail Temuan**: Identifikasi pesan error asli.
2. **Analisis Logika**: Penjelasan teknis mengapa error terjadi.
3. **Langkah Perbaikan**: Panduan solusi step-by-step.
4. **Catatan Keamanan**: Peringatan terkait kredensial atau akses sistem.