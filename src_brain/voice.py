import os
import sys
import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

class FractalVoice:
    def __init__(self, model_relative_path="models/es_ES-sharvard-medium.onnx"):
        # Determinar la ruta base del proyecto (un nivel arriba de src_brain)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.model_path = os.path.join(base_dir, model_relative_path)
        
        try:
            self.voice = PiperVoice.load(self.model_path)
            print(f"  ✅ Voz cargada: {os.path.basename(self.model_path)}")
        except Exception as e:
            print(f"  ❌ Error al cargar voz Piper: {e}")
            self.voice = None

    def speak(self, text: str):
        """Sintetiza y reproduce el texto."""
        if not self.voice:
            print(f"🤖 Robot: {text} (Voz no disponible)")
            return

        audio_chunks = []
        sample_rate = None

        try:
            for chunk in self.voice.synthesize(text):
                audio_chunks.append(chunk.audio_float_array)
                if sample_rate is None:
                    sample_rate = chunk.sample_rate

            if not audio_chunks:
                return

            audio = np.concatenate(audio_chunks)
            sd.play(audio, samplerate=sample_rate)
            sd.wait()
        except Exception as e:
            print(f"  ❌ Error en síntesis de voz: {e}")
