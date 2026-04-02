import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

class FractalBrain:
    def __init__(self):
        # 1. Rutas relativas seguras
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(base_dir, "config", ".env")
        rules_path = os.path.join(base_dir, "config", "system_rules.txt")

        load_dotenv(dotenv_path=env_path)
        
        # 2. Inicialización de cliente y modelo
        self.client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model_id = "gemini-2.5-flash"
        
        # 3. Carga de reglas y creación de sesión persistente
        self.system_instruction = self._load_rules(rules_path)
        
        self.chat_session = self.client.chats.create(
            model=self.model_id,
            config={
                'system_instruction': self.system_instruction,
                'temperature': 0.4,       # Respuesta más predecible y rápida
                'max_output_tokens': 100, # Garantizamos brevedad para el motor de voz
                'top_p': 0.8,
                'top_k': 40,
            }
        )

    def _load_rules(self, path):
        """Lee tus reglas de personalidad de forma segura."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "Eres Fractal-Bot. Robot analítico y breve."

    def think(self, user_input):
        """Usa el método específico para streaming en la nueva SDK."""
        try:
            # Cambiamos send_message(..., stream=True) por send_message_stream
            response = self.chat_session.send_message_stream(user_input)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        except Exception as e:
            yield f"Error en mi núcleo: {e}"

# --- MODO CONSOLA---
if __name__ == "__main__":
    # PRIMERO creamos el cerebro
    brain = FractalBrain() 
    
    # AHORA ya podemos imprimir su ID
    print(f"--- FRACTAL BOT ONLINE ({brain.model_id}) ---")
    print("Escribe 'salir' para apagar.")
    
    while True:
        user_text = input("\nTú: ")
        
        # Verificación de salida
        if user_text.lower() in ["salir", "exit", "apagar"]:
            print("Cerrando sistemas... Adiós, humano.")
            break
        
        # Procesamiento de respuesta
        print("Robot: ", end="")
        for text_chunk in brain.think(user_text):
            print(text_chunk, end="", flush=True)
        print() # Salto de línea al final