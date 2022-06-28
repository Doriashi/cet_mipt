import numpy as np
from numpy import exp
import matplotlib.pyplot as plt

def MKE(f, N, T0, T1):

    # N - число элементов
    M = 2 * N + 1  # М - число узлов

    L = np.zeros([3, N])  # L - матрица индексов
    for k in range(N):
        for i in range(3):
            L[i][k] = 2 * (k + 1) - 2 + i

    h = 1 / N

    # сборка полной матрицы жесткости
    A = np.zeros([M, M])
    for k in range(N):
        Ak = np.array([[7, -8, 1], [-8, 16, -8], [1, -8, 7]]) / (3 * h)
        for i in range(3):
            for j in range(3):
                A[2 * k + j][2 * k + i] += Ak[j][i]

    # сборка полного вектора нагрузки
    F = np.zeros(M)
    for k in range(N):
        Fk = h / 30 * np.matmul(np.array([[4, 2, -1], [2, 16, 2], [-1, 2, 4]]),\
             np.array([f(L[0][k] * h / 2), f(L[1][k] * h / 2), f(L[2][k] * h / 2)]))
        for i in range(3):
            F[2 * k + i] += Fk[i]

    A[0][:3] = [1, 0, 0]  # Граничные условия
    A[-1][-3:] = [0, 0, 1]
    F[0] = T0
    F[-1] = T1

    U = np.linalg.solve(A, F)  # Решаем СЛАУ
    return U


def u(x):  # точное решение
    return exp(-(32 * x - 16) ** 2)


def f(x):  # мощность тепловых источников f(x)=-u''
    return -(1024 - 2048 * x) ** 2 * exp(-(32 * x - 16) ** 2) + 2048 * exp(-(32 * x - 16) ** 2)


# Граничные условия
T0 = T1 = 0

# График для точного и посчитанного решения
N = 64  # Число узлов сетки
plt.plot(np.linspace(0, 1, 100), [u(x) for x in np.linspace(0, 1, 100)], label='Точное решение', c='k')
plt.scatter(np.linspace(0, 1, 2 * N + 1), MKE(f, N, T0, T1), label='МКЭ', c='r')
plt.title("Распределение температуры по длине стержня,\nчисло элементов = 64")
plt.legend(loc='upper right')
plt.show()

# Рассчитать скорость сходимости
N1 = 50
N2 = 100
error1 = abs(MKE(f, N1, T0, T1) - [u(x) for x in np.linspace(0, 1, 2 * N1 + 1)]).max()
error2 = abs(MKE(f, N2, T0, T1) - [u(x) for x in np.linspace(0, 1, 2 * N2 + 1)]).max()
print('Скорость сходимости u: %r' % (np.log2(error1/error2)))