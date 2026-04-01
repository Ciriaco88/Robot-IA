import speech_recognition as sr
import sounddevice as sd
import numpy as np

def test_microphone_stable():
    recognizer = sr.Recognizer()
    fs = 44100
    duration = 5  # Duración de escucha en segundos
    device_index = 0  # Usamos el dispositivo 0 que confirmamos con debug_record
    
    print("--- DIAGNÓSTICO DE AUDIO ESTABLE (sounddevice) ---")
    
    try:
        print(f"🎤 Usando dispositivo [{device_index}]...")
        print(f">>> Grabando {duration} segundos... ¡HABLA AHORA!")
        
        # Grabamos audio directo
        audio_data = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()
        
        print(">>> Audio capturado. Procesando reconocimiento con Google...")
        
        # Convertimos los datos capturados a un formato que sr.Recognizer entienda
        audio_segment = sr.AudioData(audio_data.tobytes(), fs, 2)
        
        # Reconocimiento
        text = recognizer.recognize_google(audio_segment, language="es-ES")
        print(f"\n✅ RESULTADO DEL TEST: \"{text}\"")
        print("\nEl robot ya puede oírte correctamente.")

    except sr.UnknownValueError:
        print("\n❌ Error: No se entendió el audio. Prueba a hablar más claro.")
    except Exception as e:
        print(f"\n❌ ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    test_microphone_stable()