"""
test_speak.py - Test de síntesis de voz con Piper-TTS
=====================================================
El usuario escribe un texto por consola y Piper-TTS lo convierte en voz,
reproduciéndolo por el altavoz.

Requisitos:
  - pip install piper-tts sounddevice numpy
  - Modelo de voz descargado (.onnx + .onnx.json), por ejemplo:
      es_ES-sharvard-medium.onnx
    Descárgalo de:
      https://huggingface.co/rhasspy/piper-voices/tree/main/es/es_ES

Uso:
  python tests/test_speak.py
"""

import sys

import numpy as np
import sounddevice as sd
from piper.voice import PiperVoice

# ─── CONFIGURACIÓN ────────────────────────────────────────────────────────────
MODEL_PATH = "models/es_ES-sharvard-medium.onnx"
# ──────────────────────────────────────────────────────────────────────────────


def speak(voice: PiperVoice, text: str) -> None:
    """Sintetiza 'text' con Piper y lo reproduce por el altavoz.

    voice.synthesize() devuelve un iterable de AudioChunk, cada uno con:
      - audio_float_array : np.ndarray float32 en rango [-1, 1]
      - sample_rate       : int (Hz)
    """
    audio_chunks = []
    sample_rate = None

    for chunk in voice.synthesize(text):
        audio_chunks.append(chunk.audio_float_array)
        if sample_rate is None:
            sample_rate = chunk.sample_rate

    if not audio_chunks:
        print("  ⚠️  No se generó audio.")
        return

    audio = np.concatenate(audio_chunks)
    duration = len(audio) / sample_rate
    print(f"  🔊 Reproduciendo... ({duration:.1f}s @ {sample_rate}Hz)")

    sd.play(audio, samplerate=sample_rate)
    sd.wait()


def main() -> None:
    print("=" * 55)
    print("  🤖 Fractal-Bot — Test de Voz (Piper-TTS)")
    print("=" * 55)
    print(f"  Modelo : {MODEL_PATH}")
    print("  Escribe 'salir' o pulsa Ctrl+C para terminar.\n")

    # Cargar el modelo una sola vez
    try:
        voice = PiperVoice.load(MODEL_PATH)
        print("  ✅ Modelo cargado correctamente.\n")
    except Exception as e:
        print(f"  ❌ Error al cargar el modelo: {e}")
        print("  Asegúrate de que el archivo .onnx existe en la ruta indicada.")
        sys.exit(1)

    while True:
        try:
            text = input("📝 Texto > ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\n  👋 Saliendo...")
            break

        if not text:
            continue

        if text.lower() in ("salir", "exit", "quit"):
            print("  👋 Saliendo...")
            break

        try:
            speak(voice, text)
        except Exception as e:
            print(f"  ❌ Error al sintetizar: {e}")


if __name__ == "__main__":
    main()
