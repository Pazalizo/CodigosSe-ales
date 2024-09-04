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

# Implementación del Filtro de Media Móvil
def moving_average_filter(signal, window_size):
    filtered_signal = np.zeros_like(signal)
    for i in range(len(signal)):
        if i < window_size:
            filtered_signal[i] = np.mean(signal[:i+1])
        else:
            filtered_signal[i] = np.mean(signal[i-window_size+1:i+1])
    return filtered_signal

window_size = 50 #valor de M
filtered_audio = moving_average_filter(audio_with_noise.flatten(), window_size)

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
