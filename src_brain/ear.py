import speech_recognition as sr

class FractalEar:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        # Ajuste de sensibilidad al ruido ambiental
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

    def listen(self):
        print("👂 Escuchando...")
        with self.microphone as source:
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
                print("🧠 Procesando voz...")
                text = self.recognizer.recognize_google(audio, language="es-ES")
                return text
            except sr.UnknownValueError:
                return None # No entendió nada
            except Exception as e:
                print(f"Error en oído: {e}")
                return None