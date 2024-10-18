import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk

señal_salida = []
señal_H = []
señal_entrada = []

def señalEntrada(a, b, n):
    señal_entrada.clear()
    for i in range(0, n):
        señal_entrada.append(a * np.exp(b * i))
        print(f"X({i}): {señal_entrada[i]} ")

def SeñalH(punto_final):
    señal_H.clear()
    for i in range(0, punto_final):
        if i - 1 >= 0:
            señal_H.append((c / (2 * a)) * (np.exp((d + k) * i) - np.exp(b) * np.exp((d + k) * (i - 1)) + np.exp((d - k) * i) - np.exp(b) * np.exp((d - k) * (i - 1))))
        else:
            señal_H.append((c / (2 * a)) * (np.exp((d + k) * i) + np.exp((d - k) * i)))
        print(f"h({i}):{señal_H[i]}")

def convolucion(n):
    señal_salida.clear()
    for i in range(0, n):
        sumatoria = 0
        for k in range(0, len(señal_H)):
            if i - k >= 0:
                sumatoria += señal_H[k] * señal_entrada[i - k]
            else:
                break
        señal_salida.append(sumatoria)
        print(f"y({i}): {señal_salida[i]}")

def graficar_señal(señal_xn, señal_yn):
    plt.figure()

    plt.subplot(2, 1, 1)
    plt.stem(señal_xn, linefmt='b-', markerfmt='bo', basefmt=" ")
    plt.title('X[n]')
    plt.xlabel('n')
    plt.ylabel('X[n]')

    plt.subplot(2, 1, 2)
    plt.stem(señal_yn, linefmt='b-', markerfmt='bo', basefmt=" ")
    plt.title('Y[n]')
    plt.xlabel('n')
    plt.ylabel('Y[n]')

    plt.tight_layout()
    plt.show()

# Valores predeterminados
a = 0.3
b = 0.4
c = 1
d = 0.14
k = 0.14
n = 100

# Interfaz gráfica para ingresar valores
root = tk.Tk()
root.configure(bg='#ffffea')  
root.title("Entrada de Valores")
root.geometry("300x300")

# Crear etiquetas y campos de entrada para cada valor
labels = ["a", "b", "c", "d", "k", "Cantidad de puntos (n)"]
initial_values = [a, b, c, d, k, n]
entries = []

for i, label in enumerate(labels):
    tk.Label(root, text=label, bg='#a795a5', fg='white').grid(row=i, column=0, pady=5, padx=10, sticky="w")
    entry = ttk.Entry(root)
    entry.insert(0, str(initial_values[i]))
    entry.grid(row=i, column=1, pady=5, padx=10)
    entries.append(entry)

def obtener_valores():
    global a, b, c, d, k, n  
    a = float(entries[0].get())
    b = float(entries[1].get())
    c = float(entries[2].get())
    d = float(entries[3].get())
    k = float(entries[4].get())
    n = int(entries[5].get())
    root.destroy()

# Botón para confirmar los valores ingresados
ttk.Button(root, text="Aceptar", command=obtener_valores).grid(row=len(labels), columnspan=2, pady=20)

root.mainloop()

# Llamar a las funciones correspondientes
señalEntrada(a, b, n)
SeñalH(n)
convolucion(n)
graficar_señal(señal_entrada, señal_salida)
