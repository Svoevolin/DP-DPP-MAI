def optimal_replacement(r: list, u: list, s: list, p: int, t_0: int, period: int) -> (list, list):
    n = len(r)
    r = list(x - y for x, y in zip(r, u)) # вычтем из доходов от оборудования издержки на него для каждого года

    # Создаем матрицу для максимальных прибылей и выборы замены/сохранения в кортеже: (прибыль, выбор стратегии)
    profit_matrix = [[tuple()] * (n) for _ in range(period)]

    # Этап условная оптимизация
    profit_matrix = _conditional_optimization(matrix=profit_matrix, r=r, s=s, p=p, n=n, period=period)

    # Этап безусловной оптимизации
    optimal_strategy = _unconditional_optimization(matrix=profit_matrix, t_0=t_0, period=period)

    return profit_matrix, optimal_strategy

def _conditional_optimization(matrix: list, r: list, s: list, p: int, n: int, period: int) -> list:
    print('Условная оптпимизация:')

    for k in range(period - 1, -1, -1): # итерируемся по k с последнего года эксплуатации к первому
        for t in range(n): # вычисляем прибыль для каждого возможного возраста оборудования

            if k == period - 1: # последний год эксплуатации

                save = r[t] # высчитываем прибыль при сохранении
                replace = r[0] + s[t] - p # высчитываем прибыль при замене

                print(f'F_{k + 1}({t}) = max({r[t]}, {r[0]} + {s[t]} - {p})')

            else: # все года эксплуатации кроме последнего

                save = r[t] + (matrix[k + 1][t + 1][0]) if t < n - 1 else 0 # высчитываем прибыль при сохранении
                replace = r[0] + s[t] - p + matrix[k + 1][0][0] # высчитываем прибыль при замене

                print(f'F_{k + 1}({t + 1}) = max({r[t]} + {matrix[k + 1][t + 1][0] if t < n - 1 else 0}, {r[0]} + {s[t]} - {p} + {matrix[k + 1][0][0]})')

            matrix[k][t] = (save, 'С') if save >= replace else (replace, 'З') # сохраняем большую прибыль и стратегию

    return matrix


def _unconditional_optimization(matrix: list, t_0: int, period: int) -> list:

    optimal_strategy = [] # будем сохранять здесь выбор для каждого года
    t_current = t_0  # возраст оборудования на текущий год эксплуатации

    for k in range(period): # годы эксплуатации растут до планового периода
        print(f'{k + 1}-й год эксплуатации')
        print(f'Возраст оборудования: {t_current}')

        if matrix[k][t_current][1] == 'З':
            print('Выгоднее заменить это оборудование')
            optimal_strategy.append(matrix[k][t_current])
            t_current = 0 # оборудование заменится на новое с возрастом 0 лет

        else:
            optimal_strategy.append(matrix[k][t_current])
            print('Выгоднее оставить это оборудование')
            t_current += 1 # оборудование постареет на 1 год

    return optimal_strategy


# Пример использования функции 1
r = [8, 7, 7, 6, 6, 5, 5] # стоимость продукции, произведенной в течение каждого года с помощью этого оборудования
u = [1, 2, 1, 2, 1, 2, 1] # ежегодные затраты, связанные с эксплуатацией оборудования
s = [12, 10, 8, 8, 7, 6, 4] # остаточная стоимость оборудования
p = 14 # стоимость нового оборудования
t_0 = 0 # возраст оборудования на момент анализа
planned_period = 6 # продолжительность работы оборудования

profit_matrix, optimal_strategy = optimal_replacement(r=r, u=u, s=s, p=p, t_0=t_0, period=planned_period)

print("\n Матрица максимальных прибылей:")
for row in profit_matrix:
    print(row)

print("\n Оптимальная стратегия:")
print(*list(f'|{i + 1} год: {"Сохранить" if x[1] == "С" else "Заменить"}|' for i, x in enumerate(optimal_strategy)),
      sep=' -> ')
