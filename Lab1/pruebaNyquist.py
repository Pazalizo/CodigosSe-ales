import numpy as np
import sounddevice as sd
from scipy.signal import resample

# Configuración de parámetros
fs_original = 44100       # Frecuencia de muestreo original
duration = 5              # Duración de la grabación en segundos
num_samples_reducido = 10000  # Número de muestras deseadas para el audio reducido

# Grabar audio
print("Grabando audio...")
audio = sd.rec(int(duration * fs_original), samplerate=fs_original, channels=1, dtype='float32')
sd.wait()
print("Grabación completada.")

# Reducir el número de muestras a 10000 (submuestreo)
audio_reducido = resample(audio, num_samples_reducido)

# Re-muestrear el audio reducido a la longitud original
audio_reducido_resampleado = resample(audio_reducido, int(duration * fs_original))

# Reproducir el audio reducido re-muestreado
print("Reproduciendo audio reducido...")
sd.play(audio_reducido_resampleado, samplerate=fs_original)
sd.wait()
print("Reproducción completada.")
