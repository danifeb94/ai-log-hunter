# 📁 Research & Development
Folder ini berisi berbagai skrip eksperimental, prototipe awal, dan hasil pengujian selama pengembangan **Super Agent BMC**.

## 🧪 Eksperimen Utama
Di sini saya menguji beberapa fungsionalitas inti sebelum diintegrasikan ke dalam skrip produksi:

* **Manajemen Memori AI**: Melalui `memory_agent.py` dan `selective_memory_agent.py`, saya mengeksperimen cara AI menyimpan fakta teknis secara permanen.
* **Analisis Log**: Skrip `log_analyzer.py` digunakan untuk menguji kemampuan AI dalam membedah `server_logs.txt` secara otomatis.
* **Pengolahan Multi-File**: Prototipe awal untuk membaca berbagai format dokumen sebelum difinalisasi di sistem RAG utama.
* **Unit Testing**: Pengujian library LangChain dilakukan di `test_langchain.py` untuk memastikan kompatibilitas dengan Python 3.13.

## ⚠️ Catatan
File di folder ini bersifat eksperimental. Untuk menjalankan sistem yang sudah stabil dan siap digunakan, silakan merujuk pada `super_agent_bmc.py` di direktori utama.