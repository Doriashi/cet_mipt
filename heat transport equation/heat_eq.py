import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from celluloid import Camera

lam = 46   # Коэффициент теплопроводности
ro = 7800   # Плотность
c = 460   # Теплоемкость
coef = lam / (ro * c)   # Коэффициент температуропроводности

L, H = 0.4, 0.6  # Размер пластины по осям Ox и Oy
Nx, Ny = 120, 180  # Число разбиений

# Граничные условия 1 рода
T_x0 = 100
T_yH = 70
'''
T_xL = 
T_y0 = 
'''

# Граничные условия 2 рода
q_xL = -5000  # тепловой поток нагревает материал
q_y0 = 0  # адиабатическая граница
'''
q_xL = 
q_y0 = 
'''

# Начальные условия
# Температура пластины в момент t = 0
T_t0 = 10

t_full = 50  # Время расчета
ht = 1  # Шаг расчета по времени

hx, hy = L / Nx, H / Ny  # Шаги расчета по осям Ox и Oy

u = np.zeros([Nx, Ny])  # Инициализация массива для температур
u[:, :] = T_t0  # Начальные условия

theta = 1/2  # Параметр в разностной схеме, при 0.5 безусловно устойчивая

t = 0
fig, (ax, cbar_ax) = plt.subplots(ncols=2, figsize=(14, 8), gridspec_kw={'width_ratios': [12, 1]})
camera = Camera(fig)

while t < t_full:
    t += ht
    Ku = coef * ht / hx ** 2
    P, Q = np.zeros(Nx - 1), np.zeros(Nx - 1)
    for j in range(Ny):  # Решение СЛАУ на промежуточном слое по времени в направлении Ох
        # Использование ГУ 1го рода
        P[0] = 0  # Прогоночные коэффициенты в 1ом узле по Ох
        Q[0] = T_x0
        # Использование ГУ 2го рода
        '''
        P[0] = 2 * coef * ht / (2 * coef * ht + hx ** 2)
        Q[0] = hx ** 2 * u[0, j] / (2 * coef * ht + hx ** 2) +\
               2 * coef * ht * hx * q_x0 / (lam * (hx ** 2 + 2 * coef * ht))
        '''
        for i in range(1, Nx - 1):  # Расчет остальных прогоночных коэффициентов
            a = theta * Ku
            b = 2 * theta * Ku + 1
            c = theta * Ku
            d = - u[i, j] - (1 - theta) * (u[i - 1, j] - 2 * u[i, j] + u[i, j])
            P[i] = c / (b - a * P[i - 1])
            Q[i] = (c * Q[i - 1] - d) / (b - a * P[i - 1])
        # Использование ГУ 1го рода
        '''
        u[Nx - 1, j] = T_xL
        '''
        # Использование ГУ 2го рода
        u[Nx - 1, j] = (2 * coef * ht * Q[Nx-2] - 2 * coef * ht * hx * q_xL + hx ** 2 * u[Nx - 1, j]) /\
                       (2 * coef * ht * (1 - P[Nx - 2]) + hx ** 2)
        for i in range(Nx - 2, -1, -1):
            u[i, j] = P[i] * u[i + 1, j] + Q[i]   # Расчет температуры в промежуточном слое по времени в направлении Ох

    Ku = coef * ht / hy ** 2
    P, Q = np.zeros(Ny - 1), np.zeros(Ny - 1)
    for i in range(1, Nx - 1):  # Решение СЛАУ на целом слое по времени в направлении Оу
        # Использование ГУ 1го рода
        '''
        P[0] = 0
        Q[0] = T_y0
        '''
        # Использование ГУ 2го рода
        P[0] = 2 * coef * ht / (2 * coef * ht + hy ** 2)
        Q[0] = hy ** 2 * u[i, 0] / (2 * coef * ht + hy ** 2) +\
               2 * coef * ht * hy * q_y0 / (lam * (hy ** 2 + 2 * coef * ht))
        for j in range(1, Ny - 1):  # Расчет остальных прогоночных коэффициентов
            a = theta * Ku
            b = 2 * theta * Ku + 1
            c = theta * Ku
            d = - u[i, j] - (1 - theta) * Ku * (u[i, j - 1] - 2 * u[i, j] + u[i + 1, j + 1])
            P[j] = c / (b - a * P[j - 1])
            Q[j] = (c * Q[j - 1] - d) / (b - a * P[j - 1])
        # Использование ГУ 1го рода
        u[i, Ny - 1] = T_yH
        # Использование ГУ 2го рода
        '''
        u[i, Ny - 1] = (2 * coef * ht * Q[Ny - 2] - 2 * coef * ht * hy * q_yH + hy ** 2 * u[i, Ny - 1]) /
                       (2 * coef * ht * (1 - P[Ny - 2]) + hy ** 2)
        '''
        for j in range(Ny - 2, -1, -1):
            u[i, j] = P[j] * u[i, j + 1] + Q[j]   # Расчет температуры в промежуточном слое по времени в направлении Оу

    sns.heatmap(u[::-1, ], cmap='coolwarm')
    camera.snap()

plt.show()
animation = camera.animate(interval=150)
animation.save('Heat_new.gif')
