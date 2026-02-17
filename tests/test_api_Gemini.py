import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(dotenv_path="../config/.env")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

print("--- LISTA DE MODELOS DISPONIBLES ---")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"ID: {m.name}")
except Exception as e:
    print(f"Error de conexión o API Key: {e}")