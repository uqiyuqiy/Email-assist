import os
import google.generativeai as genai
from dotenv import load_dotenv

# Buka brankas untuk mengambil kunci
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)

print("Mencari model AI yang tersedia untukmu...\n")

# Meminta daftar model langsung dari server Google
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)