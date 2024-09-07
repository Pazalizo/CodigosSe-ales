import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import matplotlib.pyplot as plt

# Parámetros de grabación
fs = 44100  # Frecuencia de muestreo
duration = 5  # Duración en segundos
filename = "audio_with_noise.wav"

# Grabación de la señal de audio
print("Grabando...")
audio = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float64')
sd.wait()  # Esperar a que termine la grabación
print("Grabación completada.")

# Implementación del Filtro de Media Móvil con ventana de 50 y promedio de 25 muestras
def filtro_media_movil(signal, M):
    N = len(signal)
    y = np.zeros(N)
    for n in range(N+1):
        if n <= M:
            # No hay suficientes datos previos, conservar el valor original
            y[n-1] = signal[n-1]
        else:
            # Calcular el promedio de M puntos
            y[n-1] = np.mean(signal[n - M -1: n-1])
    return y

M = 50  # Número de muestras a promediar dentro de la ventana
filtered_audio = filtro_media_movil(audio.flatten(), M)


# Reproducir la señal sin filtrar
print("Reproduciendo señal sin filtrar...")
sd.play(audio, fs)
sd.wait()

# Reproducir la señal filtrada
print("Reproduciendo señal filtrada...")
sd.play(filtered_audio, fs)
sd.wait()

# Guardar la señal filtrada
write("filtered_audio.wav", fs, filtered_audio)

# Graficar señales
time = np.linspace(0, duration, len(audio))

plt.figure(figsize=(10, 6))

plt.subplot(2, 1, 1)
plt.plot(time, audio)
plt.title("Señal Original")

plt.subplot(2, 1, 2)
plt.plot(time, filtered_audio)
plt.title("Señal Filtrada")

plt.tight_layout()
plt.show()
