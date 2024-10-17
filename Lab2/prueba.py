import numpy as np
import matplotlib.pyplot as plt

señal_salida = []
señal_H = []
señal_entrada = []
a = 0.3  # Puedes ajustar según tus necesidades
b = 0.4  # Puedes ajustar según tus necesidades
c = 1  # Puedes ajustar según tus necesidades
d = 0.14  # Puedes ajustar según tus necesidades
f = 0.14  # Puedes ajustar según tus necesidades

def señalEntrada(a, b, n):
    for i in range(0, n):
        señal_entrada.append(a * np.exp(b * i))
        print(f"X({i}): {señal_entrada[i]} ")

def SeñalH(punto_inicial, punto_final, prueba):
    for i in range(0, punto_final):
        if i - 1 >= 0:
            señal_H.append((c / (2 * a)) * (np.exp((d + f) * i) - np.exp(b) * np.exp((d + f) * (i - 1)) + np.exp((d - f) * i) - np.exp(b) * np.exp((d - f) * (i - 1))))
        else:
            señal_H.append((c / (2 * a)) * (np.exp((d + f) * i) + np.exp((d - f) * i)))
        print(f"h({i}):{señal_H[i]}")

def convolucion(n):
    for i in range(0, n):
        sumatoria = 0
        for k in range(0, n):
            if i - k >= 0:
                sumatoria += señal_H[k] * señal_entrada[i - k]
            else:
                break
        señal_salida.append(sumatoria)
        print(f"y({i}): {señal_salida[i]}")

def graficar_señal(señal_xn, señal_yn):
    plt.figure()

    plt.subplot(2, 1, 1)
    plt.stem(señal_xn)
    plt.title('X[n]')
    plt.xlabel('xn')
    plt.ylabel('X[n]')

    plt.subplot(2, 1, 2)
    plt.stem(señal_yn)
    plt.title('Y[n]')
    plt.xlabel('n')
    plt.ylabel('Y[n]')

    plt.tight_layout()
    plt.show()

señalsalida = []
señalentrada = []
prueba = 0
Inicio = 0
Final= int(input("Cantidad De puntos: "))

señalEntrada(a, b, Final)
SeñalH(Inicio, Final, prueba)
convolucion(Final)
graficar_señal(señal_entrada, señal_salida)