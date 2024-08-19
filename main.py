import tkinter as tk
import sounddevice as sd
import numpy as np
from scipy.io import wavfile
import pygame
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Reproductor de Audio")

        self.mixer = pygame.mixer
        self.mixer.init()

        self.duracion_label = tk.Label(root, text="Duración del audio (segundos):")
        self.duracion_label.pack()
        self.duracion_entry = tk.Entry(root)
        self.duracion_entry.pack()

        self.frecuencia_label = tk.Label(root, text="Frecuencia de muestreo (Hz):")
        self.frecuencia_label.pack()
        self.frecuencia_entry = tk.Entry(root)
        self.frecuencia_entry.pack()

        self.criterio_nyquist_label = tk.Label(root, text="Criterio de Nyquist:")
        self.criterio_nyquist_label.pack()
        self.criterio_nyquist_entry = tk.Entry(root)
        self.criterio_nyquist_entry.pack()

        self.grabar_button = tk.Button(root, text="Grabar", command=self.grabar_audio)
        self.grabar_button.pack()

        self.audio_sin_filtro = None
        self.audio_file_sin_filtro = ""  # Archivo de audio sin filtro seleccionado por el usuario

        self.audio_filtrado = None
        self.audio_file_filtrado = ""  # Archivo de audio filtrado seleccionado por el usuario

        self.audio_encima_nyquist = None
        self.audio_file_encima_nyquist = ""  # Archivo de audio encima de Nyquist seleccionado por el usuario

        self.audio_debajo_nyquist = None
        self.audio_file_debajo_nyquist = ""  # Archivo de audio debajo de Nyquist seleccionado por el usuario

        self.titulo_label = tk.Label(root, text="Archivo de audio: ")
        self.titulo_label.pack()

        self.play_button_sin_filtro = tk.Button(root, text="Reproducir sin filtro", command=self.play_audio_sin_filtro)
        self.play_button_sin_filtro.pack()
        self.play_button_sin_filtro.pack_forget()  # Ocultar el botón inicialmente

        self.play_button_filtrado = tk.Button(root, text="Reproducir filtrado", command=self.play_audio_filtrado)
        self.play_button_filtrado.pack()
        self.play_button_filtrado.pack_forget()  # Ocultar el botón inicialmente

        self.play_button_encima_nyquist = tk.Button(root, text="Reproducir encima de Nyquist", command=self.play_audio_encima_nyquist)
        self.play_button_encima_nyquist.pack()
        self.play_button_encima_nyquist.pack_forget()  # Ocultar el botón inicialmente

        self.play_button_debajo_nyquist = tk.Button(root, text="Reproducir debajo de Nyquist", command=self.play_audio_debajo_nyquist)
        self.play_button_debajo_nyquist.pack()
        self.play_button_debajo_nyquist.pack_forget()  # Ocultar el botón inicialmente

        self.comparar_button = tk.Button(root, text="Comparar Gráficas", command=self.comparar_graficas)
        self.comparar_button.pack_forget()
    
    def filtroMediaMovil(self, audio, ventana):
        if ventana % 2 == 0:
            ventana = ventana + 1

        # Calcula la mitad de la longitud de la ventana.
        mitad_ventana = ventana // 2

        # Crea una copia de la señal de audio para almacenar la señal filtrada.
        audio_filtrado = np.copy(audio)

        # Aplica el filtro de media móvil.
        for i in range(mitad_ventana, len(audio) - mitad_ventana):
            ventana_actual = audio[i - mitad_ventana : i + mitad_ventana + 1]
            audio_filtrado[i] = np.mean(ventana_actual)
        return audio_filtrado
    
    def criterioNyquist(self, audio, fs, criterio_nyquist):
        encima = fs * criterio_nyquist
        debajo = int(fs / criterio_nyquist)

        audio_encima = np.linspace(-1, 1, len(audio), endpoint=False)
        archivo_audio_encima_nyquist = "audio_encima.wav"
        wavfile.write(archivo_audio_encima_nyquist, encima, audio_encima)

        audio_debajo = np.linspace(-1, 1, len(audio), endpoint=False)
        archivo_audio_debajo_nyquist = "audio_debajo.wav"
        wavfile.write(archivo_audio_debajo_nyquist, debajo, audio_debajo)

    def play_audio_sin_filtro(self):
        if self.audio_sin_filtro:
            self.audio_sin_filtro.play()
    def play_audio_filtrado(self):
        if self.audio_filtrado:
            self.audio_filtrado.play()
    def play_audio_encima_nyquist(self):
        if self.audio_encima_nyquist:
            self.audio_encima_nyquist.play()
    def play_audio_debajo_nyquist(self):
        if self.audio_debajo_nyquist:
            self.audio_debajo_nyquist.play()

    def grabar_audio(self):
        duracion = float(self.duracion_entry.get())
        frecuencia_muestreo = int(self.frecuencia_entry.get())
        criterio_nyquist = int(self.criterio_nyquist_entry.get())

        print(f"Grabando audio durante {duracion} segundos...")
        audio = sd.rec(int(duracion * frecuencia_muestreo), samplerate=frecuencia_muestreo, channels=1)
        sd.wait()

        print("\nAudio grabado")
        print("Duración: " + str(len(audio) / frecuencia_muestreo) + "s" + "\tFrecuencia: " + str(frecuencia_muestreo) + "\tPuntos de datos: " + str(len(audio)) + "\n")

        archivo_audio_sin_filtro = "grabacion_sin_filtro.wav"
        wavfile.write(archivo_audio_sin_filtro, frecuencia_muestreo, audio)

        print(f"Audio sin filtro grabado y guardado en '{archivo_audio_sin_filtro}'")

        self.audio_file_sin_filtro = archivo_audio_sin_filtro  # Actualizar el nombre del archivo de audio sin filtro
        self.load_audio_sin_filtro()  # Cargar el nuevo archivo grabado sin filtro
        self.play_button_sin_filtro.pack()  # Mostrar el botón "Reproducir sin filtro"

        # Aplicar filtro de media móvil
        audio_filtrado = self.filtroMediaMovil(audio, 20)
        archivo_audio_filtrado = "grabacion_filtrada.wav"
        wavfile.write(archivo_audio_filtrado, frecuencia_muestreo, audio_filtrado)

        print(f"Audio filtrado grabado y guardado en '{archivo_audio_filtrado}'")

        self.audio_file_filtrado = archivo_audio_filtrado  # Actualizar el nombre del archivo de audio filtrado
        self.load_audio_filtrado()  # Cargar el nuevo archivo grabado filtrado
        self.play_button_filtrado.pack()  # Mostrar el botón "Reproducir filtrado"

        self.audio_encima_nyquist = self.filtroMediaMovil(audio, frecuencia_muestreo)

        # self.criterioNyquist(audio, frecuencia_muestreo, criterio_nyquist)
        # Generar audio encima de Nyquist
        audio_encima = np.linspace(-1, 1, int(duracion * frecuencia_muestreo), endpoint=False)
        archivo_audio_encima_nyquist = "audio_encima.wav"
        wavfile.write(archivo_audio_encima_nyquist, frecuencia_muestreo, audio_encima)

        self.audio_file_encima_nyquist = archivo_audio_encima_nyquist
        #self.load_audio_encima_nyquist()
        #self.play_button_encima_nyquist.pack()

        # Generar audio dabajo Nyquist
        audio_debajo = np.linspace(-1, 1, int(duracion * frecuencia_muestreo * criterio_nyquist), endpoint=False)
        archivo_audio_debajo_nyquist = "audio_debajo.wav"
        wavfile.write(archivo_audio_debajo_nyquist, int(frecuencia_muestreo * criterio_nyquist), audio_debajo)

        file_path = "C:/Users/ASUS/UNIRUTAS/grabacion_filtrada.wav"
        fs, audio_data = wavfile.read(file_path)

        print("presione enter para reproducir audio debajo de Nyquist")
        input()
        sd.play(audio_data, int(frecuencia_muestreo / criterio_nyquist))
        sd.wait()

        print("presione enter para reproducir audio encima de Nyquist")
        input()
        sd.play(audio_data, frecuencia_muestreo * criterio_nyquist)
        sd.wait()

        self.audio_file_debajo_nyquist = archivo_audio_debajo_nyquist
        #self.load_audio_debajo_nyquist()
        #self.play_button_debajo_nyquist.pack()


        self.comparar_button.pack()  # Mostrar el botón "Comparar Gráficas"

    def load_audio_sin_filtro(self):
        try:
            self.audio_sin_filtro = self.mixer.Sound(self.audio_file_sin_filtro)
            self.titulo_label.config(text=f"Archivo de audio sin filtro: {self.audio_file_sin_filtro}")
        except pygame.error:
            print("Error: No se pudo cargar el archivo de audio sin filtro.")

    def load_audio_filtrado(self):
        try:
            self.audio_filtrado = self.mixer.Sound(self.audio_file_filtrado)
            self.titulo_label.config(text=f"Archivo de audio filtrado: {self.audio_file_filtrado}")
        except pygame.error:
            print("Error: No se pudo cargar el archivo de audio filtrado.")

    def load_audio_encima_nyquist(self):
        try:
            self.audio_encima_nyquist = self.mixer.Sound(self.audio_file_encima_nyquist)
            self.titulo_label.config(text=f"Archivo de audio encima de Nyquist: {self.audio_file_encima_nyquist}")
        except pygame.error:
            print("Error: No se pudo cargar el archivo de audio encima de Nyquist.")

    def load_audio_debajo_nyquist(self):
        try:
            self.audio_debajo_nyquist = self.mixer.Sound(self.audio_file_debajo_nyquist)
            self.titulo_label.config(text=f"Archivo de audio debajo de Nyquist: {self.audio_file_debajo_nyquist}")
        except pygame.error:
            print("Error: No se pudo cargar el archivo de audio debajo de Nyquist.")

    def comparar_graficas(self):
        if self.audio_sin_filtro is not None and self.audio_filtrado is not None:
            _, audio_sin_filtro = wavfile.read(self.audio_file_sin_filtro)
            _, audio_filtrado = wavfile.read(self.audio_file_filtrado)

            # Crear una figura con dos subtramas
            plt.figure(figsize=(10, 5))
            
            # Subtrama 1: Audio sin filtro
            plt.subplot(2, 1, 1)
            plt.title("Audio sin filtro")
            plt.plot(audio_sin_filtro, color='b')
            
            # Subtrama 2: Audio filtrado
            plt.subplot(2, 1, 2)
            plt.title("Audio filtrado")
            plt.plot(audio_filtrado, color='r')

            plt.tight_layout()

            # Mostrar la figura con ambas subtramas en una ventana emergente
            plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioPlayer(root)
    root.mainloop()
