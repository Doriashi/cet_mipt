# cet_mipt
### Задачи по вычислительной математики
#### 1. Линейное уравнение переноса
   - Реализация схемы явный левый уголок
   - Реализация схемы Лакса-Вендроффа
   - Реализация схемы с лимиттером
#### 2. Движение волны сжатия
   - Реализация схемы Лакса
   - Реализация схемы Мак-Кормака
#### 3. МКЭ для стационарной теплопроводности в однородном стержне

#### 4. Метод сопряженных градиентов для больших СЛАУ

### Задача с использованием C++
**tamagotchi.cpp** - консольная игра-тамагочи, написанная с применением ООП. Игра моделирует поведение животного в реальном времени.<br>
*Цель игры* - не допустить смерти животного, которая наступает при достижении максимального параметра в 
индикаторах голода, скуки и усталости.

### Задачи комбинаторной оптимизации
- **Multiple Knapsack.py** написана для решения линейных целочисленных задач оптимизации, использует пакет Google or-tools,
SCIP Solver

- **Gurobi lp.py** написана для решения линейных целочисленных задач, использует коммерческий пакет Gurobi, Gurobi Solver

- **Gurobi_qp.py** написана для решения линейных целочисленных задач с квадратичными условиями, также использует коммерческий 
пакет Gurobi, Gurobi Solver

Входные данные берутся из excel файла: 

| Имя ОТВС        | Дата выгрузки ОТВС из активной зоны           | Значение тепловыделения ОТВС  |
| ------------- |:-------------:| -----:|
| 30240125.78      | 12.10.1981| 0,132969465 |
| 20000021.78     | 21.09.1983      |   0,201461816 |
| ... | ...      |   ... |

Программы распределяют ОТВС по партиям в так, чтобы их тепловыделение было примерно одинаково.
