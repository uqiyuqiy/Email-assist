import os
import imaplib
import email
from email.header import decode_header
from dotenv import load_dotenv
from google import genai  # <-- Kita menggunakan alat baru dari Google di sini!

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
IMAP_SERVER = "imap.gmail.com"

# 1. Membangunkan Otak AI dengan cara baru
client = genai.Client(api_key=GEMINI_API_KEY)

def ambil_teks_email(msg):
    """Fungsi untuk membongkar email dan mengambil teks utamanya."""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                try:
                    return part.get_payload(decode=True).decode('utf-8', 'ignore')
                except:
                    pass
    else:
        try:
            return msg.get_payload(decode=True).decode('utf-8', 'ignore')
        except:
            pass
    return ""

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
        
        if jumlah_email > 0:
            print("Membaca 2 pesan terbaru dan meminta AI merangkum...\n")
            print("=" * 60)
            
            dua_email_terbaru = email_ids[-2:] 
            
            for e_id in dua_email_terbaru:
                res, msg_data = mail.fetch(e_id, '(RFC822)')
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # Ambil Pengirim & Judul
                        pengirim = msg.get("From")
                        judul, encoding = decode_header(msg.get("Subject"))[0]
                        if isinstance(judul, bytes):
                            judul = judul.decode(encoding if encoding else "utf-8")
                            
                        print(f"Dari  : {pengirim}")
                        print(f"Judul : {judul}")
                        
                        # Ambil Isi Teks
                        isi_pesan = ambil_teks_email(msg)
                        
                        # --- AI BERAKSI DI SINI ---
                        if isi_pesan:
                            print("🤖 AI sedang membaca dan berpikir...")
                            prompt = f"Rangkum inti dari isi email berikut dalam 1-2 kalimat pendek dengan bahasa Indonesia yang santai: \n\n{isi_pesan[:1000]}"
                            
                            try:
                                # Menggunakan model canggih dari daftarmu: gemini-2.5-flash
                                respon_ai = client.models.generate_content(
                                    model='gemini-3.5-flash-lite', 
                                    contents=prompt
                                )
                                print(f"✨ Rangkuman AI: {respon_ai.text.strip()}")
                            except Exception as e:
                                print(f"❌ AI kebingungan. Error asli: {e}")
                        else:
                            print("✨ Rangkuman AI: (Tidak ada teks untuk dirangkum)")
                            
                        print("=" * 60)

        mail.logout()
        
    except Exception as e:
        print(f"❌ Gagal terhubung. Pesan error: {e}")

if __name__ == "__main__":
    cek_kotak_masuk()