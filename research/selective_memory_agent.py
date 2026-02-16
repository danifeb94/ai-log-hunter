from langchain_ollama import OllamaLLM

model = OllamaLLM(model="llama3")

def simpan_poin_penting(user_input, ai_response):
    # Prompt khusus untuk meringkas informasi teknis
    summary_prompt = (
        f"Ekstrak hanya fakta teknis penting (seperti IP, nama server, error code, atau langkah solusi) "
        f"dari percakapan ini tanpa kata-kata pembuka:\n"
        f"USER: {user_input}\n"
        f"AI: {ai_response}\n"
        f"Fakta Teknis:"
    )
    
    summary = model.invoke(summary_prompt).strip()
    
    # Simpan ke file berbeda agar lebih rapi
    with open("knowledge_base.txt", "a") as f:
        f.write(f"- {summary}\n")
    return summary

# Eksekusi
pertanyaan = "Saya baru saja mengubah timeout pada BMC-Prod-01 menjadi 60 detik."
print("--- AI sedang memproses informasi baru... ---")

jawaban = model.invoke(f"Konteks: Anda asisten teknis. Jawab singkat: {pertanyaan}")
fakta = simpan_poin_penting(pertanyaan, jawaban)

print(f"\nJawaban AI: {jawaban}")
print(f"✅ Fakta yang berhasil diingat: {fakta}")