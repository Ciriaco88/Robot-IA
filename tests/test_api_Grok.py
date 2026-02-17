import os
from openai import OpenAI  # Grok usa el estándar de OpenAI
from dotenv import load_dotenv

class FractalBrain:
    def __init__(self):
        # 1. Rutas relativas seguras
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(base_dir, "config", ".env")
        rules_path = os.path.join(base_dir, "config", "system_rules.txt")

        load_dotenv(dotenv_path=env_path)
        
        # 2. Inicialización de cliente y modelo para xAI
        # Asegúrate de tener XAI_API_KEY en tu .env
        self.client = OpenAI(
            api_key=os.getenv("XAI_API_KEY"),
            base_url="https://api.x.ai/v1",
        )
        
        # El modelo equivalente a Flash en velocidad es 'grok-beta' 
        # o 'grok-2-1212' (según disponibilidad de tu cuenta)
        self.model_id = "grok-beta" 
        
        # 3. Carga de reglas y preparación del historial
        self.system_instruction = self._load_rules(rules_path)
        
        # Grok (vía OpenAI SDK) no tiene un objeto "chat_session" persistente como Gemini,
        # así que manejamos el historial manualmente para mantener el contexto.
        self.messages = [
            {"role": "system", "content": self.system_instruction}
        ]

    def _load_rules(self, path):
        """Lee tus reglas de personalidad de forma segura."""
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "Eres Fractal-Bot. Robot analítico y breve."

    def think(self, user_input):
        """Streaming adaptado a la API de xAI."""
        try:
            # Añadimos el mensaje del usuario al historial
            self.messages.append({"role": "user", "content": user_input})
            
            # Petición con streaming
            stream = self.client.chat.completions.create(
                model=self.model_id,
                messages=self.messages,
                stream=True,
                temperature=0.7, # Puedes ajustar para ganar milisegundos
            )
            
            full_response = ""
            for chunk in stream:
                # Extraemos el contenido del fragmento
                content = chunk.choices[0].delta.content
                if content:
                    full_response += content
                    yield content
            
            # Guardamos la respuesta del bot para mantener la memoria fractal
            self.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            yield f"Error en mi núcleo (Grok): {e}"

# --- MODO CONSOLA (Se mantiene igual) ---
if __name__ == "__main__":
    brain = FractalBrain() 
    print(f"--- FRACTAL BOT ONLINE (MODO GROK: {brain.model_id}) ---")
    print("Escribe 'salir' para apagar.")
    
    while True:
        user_text = input("\nTú: ")
        if user_text.lower() in ["salir", "exit", "apagar"]:
            print("Cerrando sistemas... Adiós, humano.")
            break
        
        print("Robot: ", end="")
        for text_chunk in brain.think(user_text):
            print(text_chunk, end="", flush=True)
        print()