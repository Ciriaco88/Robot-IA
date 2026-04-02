import os
import json
import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class FractalEar:
    def __init__(self, device_index=0, sample_rate=16000):
        """
        Inicializa el oído usando Vosk para procesamiento local.
        Vosk funciona mejor con 16000Hz.
        """
        self.device_index = device_index
        self.sample_rate = sample_rate
        
        # Determinar ruta del modelo
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "vosk-model-small-es-0.42")
        
        if not os.path.exists(model_path):
            print(f"⚠️ Alerta: Modelo Vosk no encontrado en {model_path}")
            self.model = None
        else:
            self.model = Model(model_path)
            self.rec = KaldiRecognizer(self.model, self.sample_rate)
            print(f"🎤 Oído inicializado (Vosk Local) - Micro: {device_index}")

    def listen(self, duration=4):
        """Escucha audio y lo convierte a texto localmente."""
        if not self.model:
            print("❌ Error: No se puede escuchar sin el modelo Vosk cargado.")
            return None

        print("👂 Escuchando (Vosk)...")
        try:
            # Captura de audio (mono, int16 para Vosk)
            audio_data = sd.rec(int(duration * self.sample_rate), 
                                samplerate=self.sample_rate, 
                                channels=1, 
                                dtype='int16')
            sd.wait()
            
            # Verificar señal mínima
            if np.max(np.abs(audio_data)) < 100:
                return None

            print("🧠 Procesando voz localmente...")
            
            # Procesar con Vosk
            if self.rec.AcceptWaveform(audio_data.tobytes()):
                result = json.loads(self.rec.Result())
            else:
                result = json.loads(self.rec.FinalResult())
            
            text = result.get("text", "").strip()
            return text if text else None
            
        except Exception as e:
            print(f"❌ Error en reconocimiento local: {e}")
            return None

if __name__ == "__main__":
    # Test rápido local
    ear = FractalEar()
    result = ear.listen()
    print(f"Resultado: {result}")