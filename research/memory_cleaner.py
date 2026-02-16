import os

def reset_memori(file_path):
    if os.path.exists(file_path):
        # Opsi 1: Menghapus total file
        os.remove(file_path)
        # Opsi 2: Membuat file baru yang kosong (opsional)
        with open(file_path, 'w') as f:
            f.write("") 
        print(f"✅ Ingatan di '{file_path}' telah dibersihkan secara total.")
    else:
        print("Sistem tidak menemukan ingatan yang perlu dihapus.")

# Jalankan pembersihan
reset_memori("chat_history.txt")