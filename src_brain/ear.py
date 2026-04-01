import speech_recognition as sr
import sounddevice as sd
import numpy as np
import io

class FractalEar:
    def __init__(self, device_index=0, sample_rate=44100):
        self.recognizer = sr.Recognizer()
        self.device_index = device_index
        self.sample_rate = sample_rate
        print(f"🎤 Oído inicializado (sounddevice) - Micro: {device_index}")

    def listen(self, duration=4):
        """Escucha ráfagas de audio usando sounddevice."""
        print("👂 Escuchando...")
        try:
            # Captura de audio
            # Usamos int16 porque SpeechRecognition lo prefiere
            audio_data = sd.rec(int(duration * self.sample_rate), 
                                samplerate=self.sample_rate, 
                                channels=1, 
                                dtype='int16')
            sd.wait()
            
            # Verificar si hay señal mínima (evitamos procesar silencio total)
            if np.max(np.abs(audio_data)) < 100:
                return None

            print("🧠 Procesando voz...")
            # Convertimos a AudioData de SpeechRecognition
            # width=2 para int16
            audio_segment = sr.AudioData(audio_data.tobytes(), self.sample_rate, 2)
            
            text = self.recognizer.recognize_google(audio_segment, language="es-ES")
            return text
            
        except sr.UnknownValueError:
            return None # No entendió nada
        except Exception as e:
            # Capturamos timeouts o errores de hardware
            return None

if __name__ == "__main__":
    # Test rápido local
    ear = FractalEar()
    result = ear.listen()
    print(f"Resultado: {result}")