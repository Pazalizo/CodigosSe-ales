import numpy as np
def filtro_media_movil(x, M):
    N = len(x)
    y = np.zeros(N)
    for n in range(N+1):
        if n <= M:
            # No hay suficientes datos previos, conservar el valor original
            y[n-1] = x[n-1]
        else:
            # Calcular el promedio de M puntos
            print(n)
            print(x[n - M -1: n-1])
            print(np.mean(x[n - M -1: n-1]))
            y[n-1] = np.mean(x[n - M -1: n-1])
    return y

# Secuencia x(n)
x = [1, 2, 0, -1, 2]
M = 2  # Tamaño de la ventana

# Aplicar el filtro de media móvil
y = filtro_media_movil(x, M)

print(y)

