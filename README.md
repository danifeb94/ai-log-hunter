# AI Log Hunter: Automated System Diagnosis Agent

## 📌 Deskripsi Proyek
AI Log Hunter adalah agen otomasi berbasis AI yang dirancang untuk membantu System Administrator dalam menganalisis file log server yang berantakan. Menggunakan model Llama 3 yang berjalan secara lokal, alat ini mampu menyaring ribuan baris log dan memberikan laporan diagnosa teknis dalam Bahasa Indonesia.

## 🛠️ Tech Stack
- **Language:** Python 3.13
- **AI Engine:** Ollama (Local LLM)
- **Model:** Llama 3
- **Environment:** Intel NUC 14 Pro (Core Ultra 5 125H)

## 🚀 Fitur Utama
- **Noise Filtering:** Mengabaikan log INFO/DEBUG dan fokus pada error kritis.
- **Contextual Analysis:** Memahami error spesifik seperti BMC Service Timeout dan Database Link Failure.
- **Automated Reporting:** Menghasilkan file laporan `.txt` yang siap digunakan untuk tim operasional.

## 📋 Cara Menjalankan
1. Pastikan **Ollama** sudah terinstal dan menjalankan model Llama 3.
2. Clone repository ini.
3. Buat virtual environment:
   ```bash
   python -m venv ai-env
   source ai-env/bin/activate  # atau .\ai-env\Scripts\activate di Windows
4. Instal dependensi: pip install ollama
5. Jalankan: python log_analyzer.py