from langchain_ollama import OllamaLLM

# Inisialisasi model melalui LangChain
model = OllamaLLM(model="llama3")

print("--- Menghubungi AI melalui LangChain ---")
respons = model.invoke("Sebutkan satu keunggulan Intel NUC 14 Pro untuk AI.")
print(respons)