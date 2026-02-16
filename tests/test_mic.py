import speech_recognition as sr

def test_microphone():
    recognizer = sr.Recognizer()
    
    print("--- DIAGNÓSTICO DE AUDIO ---")
    
    # 1. Listar dispositivos (Para ver si Xubuntu ve tu micro)
    mic_list = sr.Microphone.list_microphone_names()
    print(f"\nDispositivos encontrados: {len(mic_list)}")
    for i, name in enumerate(mic_list):
        print(f" [{i}] - {name}")

    # 2. Intentar escuchar
    try:
        with sr.Microphone() as source:
            print("\n>>> Ajustando ruido ambiental... (Silencio 1 seg)")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            
            print(">>> Di algo ahora mismo...")
            audio = recognizer.listen(source, timeout=3)
            
            print(">>> ¡Audio capturado! Intentando reconocer con Google...")
            # Usamos Google solo para ver si el flujo de datos es correcto
            text = recognizer.recognize_google(audio, language="es-ES")
            print(f"\nResultado del test: \"{text}\"")
            print("\n✅ EL OÍDO FUNCIONA PERFECTAMENTE.")

    except sr.WaitTimeoutError:
        print("\n❌ ERROR: El micro no detectó sonido (Timeout).")
    except Exception as e:
        print(f"\n❌ ERROR TÉCNICO: {e}")

if __name__ == "__main__":
    test_microphone()