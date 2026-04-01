import sounddevice as sd
import numpy as np
import wave
import os

def record_test():
    fs = 44100  # Sample rate
    seconds = 3  # Duration of recording
    filename = "debug_audio.wav"
    
    print("--- TEST DE GRABACIÓN DIRECTA (sounddevice) ---")
    print(f"🎤 Grabando {seconds} segundos... ¡HABLA YA!")
    
    try:
        # Grabamos audio
        myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait until recording is finished
        
        print(f"✅ Grabación finalizada.")
        
        # Guardamos el archivo usando wave (estándar)
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2) # 2 bytes para int16
            wf.setframerate(fs)
            wf.writeframes(myrecording.tobytes())
        
        # Verificar si hay señal (si no es todo ceros)
        max_val = np.max(np.abs(myrecording))
        print(f"📊 Amplitud máxima detectada: {max_val}")
        
        if max_val < 50: # En int16, 50 es casi nada
            print("⚠️ ADVERTENCIA: La grabación parece estar en SILENCIO ABSOLUTO.")
        else:
            print("🎉 ¡Se ha detectado señal de audio!")
            
        print(f"\nEl archivo '{filename}' ha sido creado en la raíz del proyecto.")
        
    except Exception as e:
        print(f"❌ ERROR CRÍTICO: {e}")

if __name__ == "__main__":
    record_test()
