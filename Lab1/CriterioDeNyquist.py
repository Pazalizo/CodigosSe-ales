import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
from scipy.io.wavfile import write, read

# Configuración
duration = 5  # Duración en segundos
sample_rate = 44100  # Tasa de muestreo en Hz
output_sample_rate = 21000  # Nueva tasa de muestreo

# Grabar audio
print("Grabando...")
audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)
sd.wait()  # Espera a que termine la grabación
print("Grabación finalizada.")

# Guardar el audio grabado
write("audio_original.wav", sample_rate, audio)

# Reducción de puntos (submuestreo)
reduced_audio = audio[::int(sample_rate/output_sample_rate)]

# Guardar el audio reducido
write("audio_reducido.wav", output_sample_rate, reduced_audio)

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
plt.title("Audio Reducido")
plt.xlabel("Tiempo [s]")
plt.ylabel("Amplitud")

plt.tight_layout()
plt.show()

# Reproducir el audio reducido
print("Reproduciendo audio reducido...")
sd.play(reduced_audio, output_sample_rate)
sd.wait()
print("Reproducción finalizada.")
