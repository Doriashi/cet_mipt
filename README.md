# cet_mipt
## Задачи по вычислительной математике
#### 1. Линейное уравнение переноса
- **transport_equation.py**

Решение уравнения адвекции с использованием разностных схем
   - Реализация схемы явный левый уголок
   - Реализация схемы Лакса-Вендроффа
   - Реализация TVD-схемы с лимиттером

![TE](https://github.com/Doriashi/cet_mipt/blob/main/plots/TE.png)

Рассчитаны погрешности расчета через 80 с после начала отсчета

|               Схема   |  Максимальная   |  Среднеквадратическая|
| ------------- |:-------------:| -----:|
|  Явный левый уголок | 0.455369 | 0.113105|
|                 TVD  |0.641473 | 0.105917|
 |      Лакс-Вендрофф  |0.566645 | 0.094985|

#### 2. Движение волны сжатия
**compression_wave.py**

   - Реализация схемы Лакса
   - Реализация схемы Мак-Кормака
![Laks](https://github.com/Doriashi/cet_mipt/blob/main/plots/wave_Laks.png)
![MC](https://github.com/Doriashi/cet_mipt/blob/main/plots/wave_MC.png)
#### 3. МКЭ для стационарной теплопроводности в однородном стержне
- **finite_element_method.py**

Задача о стационарной теплопроводности в однородном стержне, на концах которого поддерживается нулевая температура:

В задаче используются квадратичные элементы
![MKE](https://github.com/Doriashi/cet_mipt/blob/main/plots/MKE.png)
Скорость сходимости численного алгоритма: 4.06


## Задача с использованием C++
- **tamagotchi.cpp** - консольная игра-тамагочи, написанная с применением ООП. Игра моделирует поведение животного в реальном времени.<br>
*Цель игры* - не допустить смерти животного, которая наступает при достижении максимального параметра в 
индикаторах голода, скуки и усталости.

## Задачи комбинаторной оптимизации для решения задачи множественного рюкзака
- **Or-tools.py** написана для решения линейных целочисленных задач оптимизации, использует пакет Google or-tools,
SCIP Solver

- **Gurobi_lp.py** написана для решения линейных целочисленных задач, использует коммерческий пакет Gurobi, Gurobi Solver

- **Gurobi_qp.py** написана для решения линейных целочисленных задач с квадратичными условиями, также использует коммерческий 
пакет Gurobi, Gurobi Solver

Входные данные берутся из excel файла: 

| Имя ОТВС        | Дата выгрузки ОТВС из активной зоны           | Значение тепловыделения ОТВС  |
| ------------- |:-------------:| -----:|
| 30240125.78      | 12.10.1981| 0,132969465 |
| 20000021.78     | 21.09.1983      |   0,201461816 |
| ... | ...      |   ... |

Программы распределяют ОТВС по партиям в так, чтобы их тепловыделение было примерно одинаково.
