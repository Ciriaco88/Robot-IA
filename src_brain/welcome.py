import time
import sys
import os

# Añadimos el directorio raíz para importar src_brain.mouth
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src_brain.mouth import FractalMouth

def main():
    print("🤖 Iniciando sistemas de Fractal-Bot...")
    
    # Inicializamos la boca del robot
    mouth = FractalMouth()
    
    # Mensaje de bienvenida con una pausa inicial para despertar el Bluetooth
    # Usamos puntos suspensivos al principio para dar tiempo al canal de audio.
    frase_bienvenida = (
        "... . "
        "Sistemas en línea. "
        "Hola Jose. "
        "Mi cerebro Gemini está operativo y mi oído ha sido calibrado. "
        "Estoy listo para tus órdenes."
    )
    
    print(f"\n📢 Robot: {frase_bienvenida}")
    
    # Empezamos a hablar
    exito = mouth.say(frase_bienvenida)
    
    if exito:
        print("\n✅ Rutina de bienvenida completada.")
    else:
        print("\n❌ Error en la rutina de bienvenida.")

if __name__ == "__main__":
    main()
