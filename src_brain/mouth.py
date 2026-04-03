import os
import sys
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

class FractalMouth:
    def __init__(self, model_filename="es_ES-sharvard-medium.onnx"):
        """
        Inicializa la 'boca' del robot usando Piper-TTS.
        Busca el modelo en el directorio 'models/'.
        """
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, "models", model_filename)
        
        if not os.path.exists(self.model_path):
            print(f"⚠️ Alerta: Modelo de voz no encontrado en {self.model_path}")
            self.voice = None
        else:
            try:
                self.voice = PiperVoice.load(self.model_path)
                print(f"🔊 Boca inicializada (Piper-TTS) - Modelo: {model_filename}")
            except Exception as e:
                print(f"❌ Error al cargar el modelo de voz: {e}")
                self.voice = None

    def say(self, text, wait=True):
        """
        Sintetiza y reproduce el texto.
        Si 'wait' es True, bloquea hasta que termine de hablar.
        """
        if not self.voice:
            print(f"🤖 (Mudo) El robot diría: {text}")
            return False
        
        try:
            audio_chunks = []
            sample_rate = None

            # Generamos el audio
            for chunk in self.voice.synthesize(text):
                audio_chunks.append(chunk.audio_float_array)
                if sample_rate is None:
                    sample_rate = chunk.sample_rate

            if not audio_chunks:
                return False

            # Concatenamos y reproducimos
            audio = np.concatenate(audio_chunks)
            sd.play(audio, samplerate=sample_rate)
            
            if wait:
                sd.wait()
            
            return True

        except Exception as e:
            print(f"❌ Error en síntesis de voz: {e}")
            return False

if __name__ == "__main__":
    # Test rápido de la clase
    mouth = FractalMouth()
    mouth.say("Probando la clase de voz del robot. Uno, dos, tres.")
