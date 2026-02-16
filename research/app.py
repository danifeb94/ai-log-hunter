import ollama

def tanya_ai(pertanyaan):
    print("--- Menghubungi AI Lokal... ---")
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': pertanyaan,
        },
    ])
    return response['message']['content']

# Test jalankan
hasil = tanya_ai("Sebutkan 3 alasan kenapa Python bagus untuk belajar AI")
print("\nJawaban AI:\n")
print(hasil)
