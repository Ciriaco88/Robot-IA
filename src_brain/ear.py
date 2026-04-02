import os
import sys
import json
import queue
import numpy as np
import sounddevice as sd
from vosk import Model, KaldiRecognizer

class FractalEar:
    def __init__(self, device_index=None, sample_rate=44100):
        """
        Inicializa el oído con Vosk y una colas para streaming.
        44100Hz es compatible con casi todo el hardware.
        """
        self.device_index = device_index
        self.sample_rate = sample_rate
        self.audio_queue = queue.Queue()
        
        # Determinar ruta del modelo
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        model_path = os.path.join(base_dir, "models", "vosk-model-small-es-0.42")
        
        if not os.path.exists(model_path):
            print(f"⚠️ Alerta: Modelo Vosk no encontrado en {model_path}")
            self.model = None
        else:
            self.model = Model(model_path)
            # Re-inicializamos el reconocedor con la tasa real
            self.rec = KaldiRecognizer(self.model, self.sample_rate)
            print(f"🎤 Oído inicializado (Interactivo) - Rate: {sample_rate}Hz")

    def _audio_callback(self, indata, frames, time, status):
        """Callback para capturar audio desde el stream de sounddevice."""
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(bytes(indata))

    def listen(self):
        """Escucha en tiempo real y detecta automáticamente cuándo dejas de hablar."""
        if not self.model:
            return None

        # Limpiar la cola de ruidos previos
        with self.audio_queue.mutex:
            self.audio_queue.queue.clear()

        print("\n👂 Escuchando (Di algo)... ", end="", flush=True)
        
        try:
            with sd.RawInputStream(samplerate=self.sample_rate, 
                                blocksize=8000, 
                                device=self.device_index, 
                                dtype='int16',
                                channels=1, 
                                callback=self._audio_callback):
                
                while True:
                    data = self.audio_queue.get()
                    if self.rec.AcceptWaveform(data):
                        # Frase completa detectada
                        result = json.loads(self.rec.Result())
                        text = result.get("text", "").strip()
                        if text:
                            print(f"\r✅ Entendido: {text}")
                            return text
                        else:
                            print("\r👂 Escuchando (Di algo)... ", end="", flush=True)
                    else:
                        # Resultado parcial (feedback visual)
                        partial = json.loads(self.rec.PartialResult())
                        partial_text = partial.get("partial", "").strip()
                        if partial_text:
                            sys.stdout.write(f"\r👂 Entendiendo: {partial_text}...")
                            sys.stdout.flush()

        except KeyboardInterrupt:
            return None
        except Exception as e:
            print(f"\n❌ Error en escucha interactiva: {e}")
            return None

if __name__ == "__main__":
    # Test rápido interactivo
    ear = FractalEar()
    while True:
        res = ear.listen()
        if res == "salir": break
        if res: print(f"-> Robot recibió: {res}")