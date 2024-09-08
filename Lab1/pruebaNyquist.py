import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write
from scipy.signal import resample  # Importar la función de remuestreo

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

# Remuestrear el audio a una frecuencia más alta
high_sample_rate = 96000  # Nueva tasa de muestreo más alta
remuestreado_audio = resample(audio, int(duration * high_sample_rate))

# Guardar el audio remuestreado
write("audio_remuestreado.wav", high_sample_rate, remuestreado_audio.astype(np.float32))

def ver_longitudes(audio_original, audio_reducido, audio_remuestreado):
    print(f"Longitud del audio original: {len(audio_original)} muestras")
    print(f"Longitud del audio reducido: {len(audio_reducido)} muestras")
    print(f"Longitud del audio remuestreado: {len(audio_remuestreado)} muestras")

# Ver las longitudes de los arrays de sonido
ver_longitudes(audio, reduced_audio, remuestreado_audio)

# Graficar los tres audios
time_original = np.linspace(0., duration, audio.shape[0])
time_reduced = np.linspace(0., duration, reduced_audio.shape[0])
time_remuestreado = np.linspace(0., duration, remuestreado_audio.shape[0])

plt.figure(figsize=(12, 9))

plt.subplot(3, 1, 1)
plt.plot(time_original, audio)
plt.title("Audio Original")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.subplot(3, 1, 2)
plt.plot(time_reduced, reduced_audio)
plt.title("Audio Reducido Aleatoriamente")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.subplot(3, 1, 3)
plt.plot(time_remuestreado, remuestreado_audio)
plt.title("Audio Remuestreado")
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

# Reproducir el audio remuestreado
print("Reproduciendo audio remuestreado por encima")
sd.play(remuestreado_audio, high_sample_rate)
sd.wait()
print("Reproducción finalizada.")
