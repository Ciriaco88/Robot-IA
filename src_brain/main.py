import sys
import os

# Añadimos la carpeta src_brain al camino de búsqueda de Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'src_brain'))

from brain import FractalBrain
from ear import FractalEar

def main():
    # 1. Inicializar órganos
    print("--- INICIALIZANDO FRACTAL-BOT (Generación 3) ---")
    cerebro = FractalBrain()
    oido = FractalEar()
    
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
                    print("🤖 Robot: Entendido. Cerrando sistemas...")
                    break
                
                # 3. Fase de Pensamiento y Respuesta
                print("🤖 Robot: ", end="", flush=True)
                for trozo in cerebro.think(texto_usuario):
                    print(trozo, end="", flush=True)
                print("\n") # Salto de línea al terminar la respuesta
            else:
                # Si no detectó voz o no entendió
                continue

    except KeyboardInterrupt:
        print("\n\nParada de emergencia detectada. Adiós.")

if __name__ == "__main__":
    main()