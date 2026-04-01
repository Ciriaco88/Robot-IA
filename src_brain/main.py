import sys
import os

# Detectar el directorio base del proyecto de forma dinámica
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.append(base_dir)

from brain import FractalBrain
from ear import FractalEar
from voice import FractalVoice

def main():
    # 1. Inicializar órganos
    print("--- INICIALIZANDO FRACTAL-BOT (Generación 3) ---")
    cerebro = FractalBrain()
    oido = FractalEar()
    voz = FractalVoice()
    
    print("\n✅ Sistemas listos. Ya puedes hablar con el robot.")
    print("(Di 'salir' o pulsa Ctrl+C para terminar)\n")

    try:
        while True:
            # 2. Fase de Escucha
            texto_usuario = oido.listen()
            
            if texto_usuario:
                print(f"\n👤 Tú: {texto_usuario}")
                
                # Comprobar si el usuario quiere salir
                if any(palabra in texto_usuario.lower() for palabra in ["salir", "exit", "apagar"]):
                    msg_despedida = "Entendido. Cerrando sistemas... Adiós."
                    print(f"🤖 Robot: {msg_despedida}")
                    voz.speak(msg_despedida)
                    break
                
                # 3. Fase de Pensamiento (Streaming en consola)
                print("🤖 Robot: ", end="", flush=True)
                respuesta_completa = ""
                for trozo in cerebro.think(texto_usuario):
                    print(trozo, end="", flush=True)
                    respuesta_completa += trozo
                print() # Salto de línea
                
                # 4. Fase de Habla
                if respuesta_completa:
                    voz.speak(respuesta_completa)
            else:
                # Si no detectó voz o no entendió
                continue

    except KeyboardInterrupt:
        print("\n\nParada de emergencia detectada. Adiós.")

if __name__ == "__main__":
    main()