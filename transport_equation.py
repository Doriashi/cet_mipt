import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt

def foo(x): # начальная функция
    d = 0.4
    if x > 0:
        return 1
    else:
        return math.exp(-x ** 2/d ** 2)

def start_bound(x1, x2, d_x, t, d_t):
    X = np.arange(x1, x2 + d_x, d_x) # сделали сетку по x
    T = np.arange(0, t + d_t, d_t) # сделали сетку по t
    U = np.zeros((len(T), len(X))) # сделали массив, куда будем складывать решение

    for i in range(len(X)): # сделали НУ
        U[0][i] = foo(X[i])

    for j in range(len(T)): # сделали ГУ
        U[j][0] = foo(x1)
    return X, T, U

def exact(X, t, c): #считаем точное решение
    U = []
    for x_i in X:
        U.append(foo(x_i - c * t))
    return U


def corner(X, U, T, c, d_x, d_t):  # левый явный уголок
    kur = c * d_t / d_x
    for t_j in range(len(T) - 1):
        for x_i in range(1, len(X)):
            U[t_j + 1][x_i] = U[t_j][x_i] - kur * (U[t_j][x_i] - U[t_j][x_i - 1])
    return U


def TVD(X, U, T, c, d_x, d_t):  # TVD с лимитером
    kur = c * d_t / d_x
    for t_j in range(len(T) - 1):
        for x_i in range(1, len(X)):
            if x_i != (len(X)-1):
                q = (U[t_j][x_i] - U[t_j][x_i - 1] + 1.e-5) / (U[t_j][x_i + 1] - U[t_j][x_i] + 1.e-5)
                fi = max(0, min(1, q))  # лимитер
                U_plus = 0.5 * fi * kur * (1 - kur) * (U[t_j][x_i + 1] - U[t_j][x_i])
                U_minus = 0.5 * fi * kur * (1 - kur) * (U[t_j][x_i] - U[t_j][x_i - 1])
                U[t_j + 1][x_i] = U[t_j][x_i] - kur * (U[t_j][x_i] - U[t_j][x_i - 1]) - (U_plus - U_minus)
            else:
                U[t_j + 1][x_i] = (1 - kur) / (1 + kur) * (U[t_j][x_i] - U[t_j + 1][x_i - 1]) + U[t_j][x_i -1]
    return U


def Laks_Vend(X, U, T, c, d_x, d_t): # Лакс-Вендрофф
    kur = c * d_t / d_x
    for t_j in range(len(T) - 1):
        for x_i in range(1, len(X) - 1):
            U_plus = 0.5 * kur * (1 - kur) * (U[t_j][x_i + 1] - U[t_j][x_i])
            U_minus = 0.5 * kur * (1 - kur) * (U[t_j][x_i] - U[t_j][x_i - 1])
            U[t_j + 1][x_i] = U[t_j][x_i] - kur * (U[t_j][x_i] - U[t_j][x_i - 1]) - (U_plus - U_minus)
    return U

def e_max(X, U, F, t): # максимальная ошибка
    A = []
    for i in range(len(X)):
        A.append(abs(U[i] - F[t][i]))
    return max(A)


def e_rms(X, U, F, t): # среднеквадратичная ошибка
    return (sum(((U[i] - F[t][i]) ** 2) for i in range(len(X))) / len(X)) ** (1/2)

# условия
x1 = -10
x2 = 70
d_x = 1
d_t = 1
c = 0.5
T = 100 # максимальное время

# моменты времени, в которые смотрим решения
t1 = 0
t2 = 50
t3 = 100

X, T, U = start_bound(x1, x2, d_x, T, d_t)

'''
fig1 = plt.figure(figsize=(12, 6))
plt.title("Точное решение", fontsize=15)
plt.xlabel("x")
plt.ylabel("Решение")
plt.plot(X, exact(X, t1, c), "-", color='red', label = t1)
plt.plot(X, exact(X, t2, c), "-", color='orange', label = t2)
plt.plot(X, exact(X, t3, c), "-", color='blue', label = t3)
plt.legend()
plt.show()

U2 = corner(X, U, T, c, d_x, d_t)
fig2 = plt.figure(figsize=(12, 6))
plt.title("Явный левый уголок", fontsize=15)
plt.xlabel("x")
plt.ylabel("Решение")
plt.plot(X, U2[t1], "-", color='red', label = t1)
plt.plot(X, U2[t2], "-", color='orange', label = t2)
plt.plot(X, U2[t3], "-", color='blue', label = t3)
plt.legend()
plt.show()

U3 = TVD(X, U, T, c, d_x, d_t)
fig3 = plt.figure(figsize=(12, 6))
plt.title("TVD с лимитером (12)", fontsize=15)
plt.xlabel("x")
plt.ylabel("Решение")
plt.plot(X, U3[t1], "-", color='red', label = t1)
plt.plot(X, U3[t2], "-", color='orange', label = t2)
plt.plot(X, U3[t3], "-", color='blue', label = t3)
plt.legend()
plt.show()

U4 = Laks_Vend(X, U, T, c, d_x, d_t)
fig4 = plt.figure(figsize=(12, 6))
plt.title("Лакс-Вендрофф", fontsize=15)
plt.xlabel("x")
plt.ylabel("Решение")
plt.plot(X, U4[t1], "-", color='red', label = t1)
plt.plot(X, U4[t2], "-", color='orange', label = t2)
plt.plot(X, U4[t3], "-", color='blue', label = t3)
plt.legend()
plt.show()
'''

t_all = 80
fig5 = plt.figure(figsize=(12, 6))
plt.title("Сравнение численных и точного решения\nчерез t = 80", fontsize=15)
plt.xlabel("Значение координаты, вдоль которой осуществляется перенос")
plt.ylabel("Решение")
U1 = exact(X, t_all, c)
plt.plot(X, exact(X, t_all, c), "-", color='black', label = 'Точное')

U2 = corner(X, U, T, c, d_x, d_t)
em2 = e_max(X, U1, U2, t_all)
er2 = e_rms(X, U1, U2, t_all)
plt.plot(X, U2[t_all], "-", color='red', label = 'Явный левый уголок')

U3 = TVD(X, U, T, c, d_x, d_t)
em3 = e_max(X, U1, U3, t_all)
er3 = e_rms(X, U1, U3, t_all)
plt.plot(X, U3[t_all], "-", color='orange', label = 'TVD')

U4 = Laks_Vend(X, U, T, c, d_x, d_t)
em4 = e_max(X, U1, U4, t_all)
er4 = e_rms(X, U1, U4, t_all)
plt.plot(X, U4[t_all], "-", color='blue', label = 'Лакс-Вендрофф')
plt.legend()
plt.show()

Names = ["Явный левый уголок", "TVD", "Лакс-Вендрофф"]
E_max = [em2, em3, em4]
E_rms = [er2, er3, er4]
dict = {
            'Names': Names,
            'E_max': E_max,
            'E_rms': E_rms
        }
df = pd.DataFrame(dict)
print(df)