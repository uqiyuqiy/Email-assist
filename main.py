import os
import imaplib
from dotenv import load_dotenv

# 1. Membuka brankas rahasia (.env)
load_dotenv()

# 2. Mengambil kunci dan alamat email
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

def cek_kotak_masuk():
    print("Mencoba terhubung ke server Google...")
    
    try:
        # Mengetuk pintu server Google
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        
        # Masuk menggunakan sandi khusus aplikasi
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ Berhasil login ke email!")
        
        # Masuk ke folder Inbox (Kotak Masuk)
        mail.select('inbox')
        
        # Mencari email yang statusnya belum dibaca (UNSEEN)
        status, messages = mail.search(None, 'UNSEEN')
        
        # Menghitung jumlahnya
        email_ids = messages[0].split()
        jumlah_email = len(email_ids)
        
        print(f"📬 Kamu memiliki {jumlah_email} email yang belum dibaca.")
        
        # Keluar dari server dengan aman
        mail.logout()
        
    except Exception as e:
        print(f"❌ Gagal terhubung. Pesan error: {e}")

# Menjalankan fungsi di atas
if __name__ == "__main__":
    cek_kotak_masuk()
