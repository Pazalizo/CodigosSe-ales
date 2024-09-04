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

# Añadir ruido blanco
noise = np.random.normal(0, 0.05, audio.shape)
audio_with_noise = audio + noise

# Guardar la señal de audio con ruido
write(filename, fs, audio_with_noise)

# Implementación del Filtro de Media Móvil con ventana de 50 y promedio de 25 muestras
def moving_average_filter(signal, N, M):
    filtered_signal = np.zeros_like(signal)
    half_window = N // 2
    for i in range(len(signal)):
        start = max(i - half_window, 0)
        end = min(i + half_window + 1, len(signal))
        if end - start > M:  # Si el rango de la ventana es mayor que M, se recorta
            start = end - M
        filtered_signal[i] = np.mean(signal[start:end])
    print(f"la senal filtrada es: {filtered_signal}")
    return filtered_signal

N = 50  # Tamaño de la ventana
M = 50  # Número de muestras a promediar dentro de la ventana
filtered_audio = moving_average_filter(audio_with_noise.flatten(), N, M)
print(f"la senal sin filtrar es: {audio_with_noise}")

# Reproducir la señal sin filtrar
print("Reproduciendo señal sin filtrar...")
sd.play(audio_with_noise, fs)
sd.wait()

# Reproducir la señal filtrada
print("Reproduciendo señal filtrada...")
sd.play(filtered_audio, fs)
sd.wait()

# Guardar la señal filtrada
write("filtered_audio.wav", fs, filtered_audio)

# Graficar señales
time = np.linspace(0, duration, len(audio_with_noise))

plt.figure(figsize=(10, 6))

plt.subplot(3, 1, 1)
plt.plot(time, audio)
plt.title("Señal Original")

plt.subplot(3, 1, 2)
plt.plot(time, audio_with_noise)
plt.title("Señal con Ruido")

plt.subplot(3, 1, 3)
plt.plot(time, filtered_audio)
plt.title("Señal Filtrada")

plt.tight_layout()
plt.show()
