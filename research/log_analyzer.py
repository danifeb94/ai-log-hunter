import ollama
import os

def baca_dan_analisa(nama_file):
    # 1. Membaca file log asli
    if not os.path.exists(nama_file):
        return "Error: File log tidak ditemukan!"
    
    with open(nama_file, 'r') as file:
        isi_log = file.read()

    print(f"--- Memulai analisis file: {nama_file} ---")
    
    # 2. Instruksi Agentic (System Prompt)
    perintah_system = (
        "Anda adalah AI Ops Engineer senior. Analisis log berikut. "
        "Abaikan baris 'INFO' atau 'DEBUG'. Fokus hanya pada 'WARNING', 'ERROR', dan 'CRITICAL'. "
        "Buat laporan singkat berisi: Masalah Utama, Tingkat Bahaya, dan Solusi Teknis dalam Bahasa Indonesia."
    )

    # 3. Memanggil Ollama
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': perintah_system},
        {'role': 'user', 'content': f"Berikut adalah data log-nya:\n\n{isi_log}"},
    ])
    
    return response['message']['content']

# Eksekusi Program
file_input = "server_logs.txt"
file_output = "analysis_report.txt"

hasil_analisis = baca_dan_analisa(file_input)

# 4. Menyimpan hasil ke file baru
with open(file_output, 'w', encoding='utf-8') as f:
    f.write(hasil_analisis)

print(f"\n✅ Analisis selesai! Laporan telah disimpan di: {file_output}")
print("\nIsi Laporan Singkat:\n")
print(hasil_analisis[:300] + "...") # Menampilkan cuplikan hasil