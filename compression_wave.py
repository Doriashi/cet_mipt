import numpy as np
import matplotlib.pyplot as plt
from celluloid import Camera

def f(x, x1, x2):  # начальная функция
    u1 = 1
    u2 = 0
    if x < x1:
        return u1
    elif x > x2:
        return u2
    else:
        return u1 + (u2 - u1) * (x - x1) / (x2 - x1)


def start_bound_f(a, b, x1, x2, d_x, t, d_t):
    X = np.arange(a, b + d_x, d_x)  # сетка по x
    T = np.arange(0, t + d_t, d_t)  # сетка по t
    U = np.zeros((len(T), len(X)))  # массив, куда складываются решение

    for i in range(len(X)):  # НУ
        U[0][i] = f(X[i], x1, x2)

    for j in range(len(T)):  # ГУ
        U[j][0] = f(a, x1, x2)
        U[j][len(X) - 1] = f(b, x1, x2)
    return X, T, U


def F(u):
    return u ** 2 / 2


def Laks(X, U, T, d_x, d_t):
    kur = d_t / d_x
    for t_j in range(len(T) - 1):
        for x_i in range(1, len(X) - 1):
            U[t_j + 1][x_i] = 0.5 * (U[t_j][x_i + 1] + U[t_j][x_i - 1]) - kur / 2 * (F(U[t_j][x_i + 1]) - F(U[t_j][x_i - 1]))
    return U


def MacCormack(X, U, T, d_x, d_t):
    kur = d_t / d_x
    for t_j in range(len(T) - 1):
        x_i = 0
        U_pr_prev = U[t_j][x_i] - kur / 2 * ((U[t_j][x_i + 1]) ** 2 - (U[t_j][x_i]) ** 2)
        for x_i in range(1, len(X) - 1):
            U_pr = U[t_j][x_i] - kur / 2 * (U[t_j][x_i + 1] ** 2 - U[t_j][x_i] ** 2)
            U[t_j + 1][x_i] = 0.5 * (U[t_j][x_i] + U_pr) - kur / 4 * (U_pr ** 2 - U_pr_prev ** 2)
            U_pr_prev = U_pr
    return U


def printer(U, title, file_name):
    fig = plt.figure(figsize=(10, 6))
    plt.title(title, fontsize=15)
    plt.xlabel("Значение координаты, вдоль которой осуществляется движение")
    plt.ylabel("Решение")
    ax = fig.gca()
    ax.set_xticks(np.arange(0, 1, 0.1))
    ax.set_yticks(np.arange(0, 1.2, 0.2))
    plt.grid()
    t_i = 0
    t_max = 0.7  # время, до которого рисуем решения
    camera = Camera(fig)
    while t_i <= t_max:
        plt.plot(X, U[int(t_i / d_t)], "-", color='blue')
        t_i += 0.01
        camera.snap()
    animation = camera.animate()
    animation.save(file_name, writer = 'imagemagick')
    return 0


a = 0  # условия
b = 1
x1 = 0.2
x2 = 0.5
d_x = 0.001
d_t = 0.0005
t = 0.8  # максимальное время
U1, U2 =[], []

X, T, U = start_bound_f(a, b, x1, x2, d_x, t, d_t)

U1 = Laks(X, U, T, d_x, d_t)
printer(U1, 'Схема Лакса', 'Laks.gif')

U2 = MacCormack(X, U, T, d_x, d_t)
printer(U2, 'Схема Мак-Кормака', 'MC.gif')