import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

# Configuración
duration = 5  # Duración en segundos
sample_rate = 44100  # Tasa de muestreo en Hz
output_sample_rate = 5000  # Tasa de muestreo objetivo

# Grabar audio
print("Grabando...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()  # Espera a que termine la grabación
print("Grabación finalizada.")

# Guardar el audio grabado
write("audio_original.wav", sample_rate, audio)

# Reducción de puntos (submuestreo aleatorio)
total_samples = int(duration * output_sample_rate)
indices = np.sort(np.random.choice(len(audio), total_samples, replace=False))
reduced_audio = audio[indices]
 
# Guardar el audio reducido
write("audio_reducido_aleatorio.wav", output_sample_rate, reduced_audio)

def ver_longitudes(audio_original, audio_reducido):
    print(f"Longitud del audio original: {len(audio_original)} muestras")
    print(f"Longitud del audio reducido: {len(audio_reducido)} muestras")

# Ver las longitudes de los arrays de sonido
ver_longitudes(audio, reduced_audio)

# Graficar ambos audios
time_original = np.linspace(0., duration, audio.shape[0])
time_reduced = np.linspace(0., duration, reduced_audio.shape[0])

plt.figure(figsize=(12, 6))

plt.subplot(2, 1, 1)
plt.plot(time_original, audio)
plt.title("Audio Original")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.subplot(2, 1, 2)
plt.plot(time_reduced, reduced_audio)
plt.title("Audio Reducido Aleatoriamente")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.tight_layout()
plt.show()

# Reproducir el audio reducido
print("Reproduciendo audio reducido...")
sd.play(reduced_audio, output_sample_rate)
sd.wait()

# Reproducir el audio original
print("Reproduciendo audio original...")
sd.play(audio, sample_rate)
sd.wait()
print("Reproducción finalizada.")
