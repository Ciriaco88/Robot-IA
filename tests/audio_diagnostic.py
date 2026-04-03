import sounddevice as sd
import numpy as np
import sys
import time

SAMPLE_RATE = 44100
CHANNELS = 1
DURATION_PER_DEVICE = 2 # segundos por dispositivo

def get_rms(device_index):
    """Captura una pequeña ráfaga de audio y devuelve el RMS."""
    try:
        data = sd.rec(int(SAMPLE_RATE * 0.5), samplerate=SAMPLE_RATE, 
                      channels=CHANNELS, device=device_index, blocking=True)
        return np.sqrt(np.mean(data**2))
    except Exception:
        return -1

def main():
    print("--- BUSCADOR DE MICROFONO ---")
    print("Vamos a probar todos los dispositivos de entrada para encontrar el correcto.\n")
    
    devices = sd.query_devices()
    input_devices = [i for i, d in enumerate(devices) if d['max_input_channels'] > 0]
    
    print(f"{'ID':<4} | {'RMS':<8} | {'Nivel':<12} | {'Nombre del Dispositivo'}")
    print("-" * 60)
    
    for idx in input_devices:
        name = devices[idx]['name']
        rms = get_rms(idx)
        
        if rms < 0:
            status = "ERROR"
            bar = ""
        elif rms > 0.9:
            status = "SATURADO"
            bar = "!!!!!!!!!!!!"
        else:
            status = f"{rms:.4f}"
            bar = "█" * int(rms * 50)
            
        print(f"{idx:<4} | {status:<8} | {bar:<12} | {name}")
        time.sleep(0.1)

    print("\n--- DIAGNÓSTICO ---")
    print("1. Si un dispositivo tiene RMS > 0.9 (SATURADO), suele ser ruido o el canal equivocado.")
    print("2. Si tiene RMS < 0.001, está silenciado o no tiene nada conectado.")
    print("3. Busca uno que tenga un RMS bajo (ej. 0.0100) y que cambie si haces ruido.")
    
if __name__ == "__main__":
    main()
