from langchain_ollama import OllamaLLM

# 1. Inisialisasi model
model = OllamaLLM(model="llama3")

def jalankan_agen_dengan_memori(file_path, user_input):
    # 2. Membaca ingatan lama
    with open(file_path, 'r') as file:
        context = file.read()

    # 3. Menyusun prompt dengan konteks
    prompt = (
        f"Berikut adalah riwayat percakapan sebelumnya:\n{context}\n\n"
        f"Pertanyaan Terbaru: {user_input}\n"
        f"Jawaban:"
    )

    print(f"--- AI sedang berpikir di NUC 14 Pro... ---")
    response = model.invoke(prompt)

    # 4. MENYIMPAN INGATAN BARU (Append ke file)
    with open(file_path, 'a') as file:
        file.write(f"\nUSER: {user_input}\n")
        file.write(f"AI: {response}\n")

    return response

# Contoh Penggunaan Aktif
pertanyaan = "Berdasarkan masalah database tadi, apa saran perbaikan untuk port 8080?"
hasil = jalankan_agen_dengan_memori("chat_history.txt", pertanyaan)

print(f"\nJawaban AI: {hasil}")
print(f"\n✅ Ingatan baru telah disimpan ke chat_history.txt")