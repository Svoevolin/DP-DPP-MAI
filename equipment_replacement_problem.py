def optimal_replacement(r: list, u: list, s: list, p: int, age: int, period: int):
    n = len(r)
    r = list(x - y for x, y in zip(r, u))
    print(r)
    # Создаем матрицу для хранения максимальных прибылей
    profit_matrix = [[tuple()] * (n - age) for _ in range(n - age)]
    # Заполняем матрицу прибылей и сохраняем выборы замены/сохранения в кортеже: (прибыль, выбор стратегии)
    # Условная оптимизация
    for k in range(period, 0, -1):
        for t in range(1, period + 1):
            if k == period:
                save = r[t]
                replace = r[0] + s[t] - p
            else:
                save = r[t] + (profit_matrix[k][t][0]) if t <= period - 1 else 0
                replace = r[0] + s[t] - p + profit_matrix[k][0][0]
            if save >= replace:
                profit_matrix[k - 1][t - 1] = save, 'Save   '
            else:
                profit_matrix[k - 1][t - 1] = replace, 'Replace'

    # Находим оптимальную стратегию
    # Безусловная оптимизация
    optimal_strategy = []
    profit = 0
    t = age
    for k in range(1, period + 1):
        optimal_strategy.append(profit_matrix[k - 1][t - 1])
        profit += profit_matrix[k - 1][t - 1][0]
        if profit_matrix[k - 1][t - 1][1] == 'Replace':
            t = age
        else:
            t += 1
    return profit_matrix, optimal_strategy, profit

# Пример использования функции 1
r = [8, 7, 7, 6, 6, 5, 5]
u = [0, 0, 0, 0, 0, 0, 0]
s = [12, 10, 8, 8, 7, 6, 4]
p = 13
age_of_equipment = 1
planned_period = 6

profit_matrix, optimal_strategy, profit = optimal_replacement(r, u, s, p, age_of_equipment, planned_period)

print("Матрица оптимальных прибылей:")
for row in profit_matrix:
    print(row)

print("\nОптимальная стратегия:")
print(*list(f'{i + 1} год: {x[1]}' for i, x in enumerate(optimal_strategy)), sep='\n')

print("\nПрибыль:")
print(profit)

# Пример использования функции 2
r = [10, 9, 9, 6, 6, 5, 5]
u = [2, 2, 4, 2, 2, 4, 2]
s = [10, 10, 10, 8, 7, 6, 4]
p = 16
age_of_equipment = 1
planned_period = 6

profit_matrix, optimal_strategy, profit = optimal_replacement(r, u, s, p, age_of_equipment, planned_period)

print("Матрица оптимальных прибылей:")
for row in profit_matrix:
    print(row)

print("\nОптимальная стратегия:")
print(*list(f'{i + 1} год: {x[1]}' for i, x in enumerate(optimal_strategy)), sep='\n')

print("\nПрибыль:")
print(profit)

