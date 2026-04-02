import sys
import os

# Añadimos el directorio raíz al path para poder importar src_brain
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src_brain.ear import FractalEar

def test_microphone_vosk():
    print("--- DIAGNÓSTICO DE AUDIO INTERACTIVO (Vosk Local) ---")
    
    try:
        # Inicializamos el oído real del robot
        oido = FractalEar()
        
        print("\nPrueba de escucha interactiva:")
        print(">>> HABLA AHORA (di una frase corta o 'hola robot')")
        
        # Usamos el método real que usa el robot
        text = oido.listen()
        
        if text:
            print(f"\n✅ TEST EXITOSO: Has dicho: \"{text}\"")
            print("El reconocimiento local está funcionando perfectamente.")
        else:
            print("\n⚠️ No se detectó ninguna frase. Revisa tu micro o habla más alto.")

    except Exception as e:
        print(f"\n❌ ERROR TÉCNICO: {e}")
        print("Asegúrate de haber descargado el modelo en models/vosk-model-small-es-0.42")

if __name__ == "__main__":
    test_microphone_vosk()