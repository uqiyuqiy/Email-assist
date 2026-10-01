import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

def cek_kotak_masuk():
    print("Mencoba terhubung ke server Google...")
    
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        print("✅ Berhasil login ke email!\n")
        
        mail.select('inbox')
        status, messages = mail.search(None, 'UNSEEN')
        
        email_ids = messages[0].split()
        jumlah_email = len(email_ids)
        
        print(f"📬 Kamu memiliki {jumlah_email} email yang belum dibaca.\n")
        
        # --- FITUR BARU MULAI DARI SINI ---
        if jumlah_email > 0:
            print("Membaca 3 pesan terbaru...")
            print("-" * 40)
            
            # Mengambil maksimal 3 ID email terakhir (yang paling baru)
            tiga_email_terbaru = email_ids[-3:] 
            
            for e_id in tiga_email_terbaru:
                # Mengambil data mentah dari email tersebut
                res, msg_data = mail.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        # Mengubah data mentah menjadi pesan yang bisa dibaca
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Mengambil alamat Pengirim
                        pengirim = msg.get("From")
                        
                        # Mengambil Judul dan menerjemahkannya ke teks biasa
                        judul, encoding = decode_header(msg.get("Subject"))[0]
                        if isinstance(judul, bytes):
                            judul = judul.decode(encoding if encoding else "utf-8")
                            
                        print(f"Dari  : {pengirim}")
                        print(f"Judul : {judul}")
                        print("-" * 40)

        mail.logout()
        
    except Exception as e:
        print(f"❌ Gagal terhubung. Pesan error: {e}")

if __name__ == "__main__":
    cek_kotak_masuk()
    