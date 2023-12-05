from prettytable import PrettyTable

def resource_allocation(costs, profits, total_resources):
    # Получаем количество предприятий
    num_enterprises = len(costs)
    # Инициализируем двумерный массив для хранения результатов
    dp = [[0 for _ in range(total_resources + 1)] for _ in range(num_enterprises + 1)]

    # Заполняем таблицу значениями
    for i in range(1, num_enterprises + 1):
        for r in range(1, total_resources + 1):
            # Выбираем максимальное значение для текущей ячейки в таблице
            # Если текущий ресурс больше или равен стоимости текущего предприятия
            if costs[i - 1] <= r:
                # Максимизируем доход: выбираем между включением текущего предприятия
                # и максимальным доходом на предыдущем уровне без текущего предприятия
                dp[i][r] = max(profits[i - 1] + dp[i - 1][r - costs[i - 1]], dp[i - 1][r])
            else:
                # Если стоимость текущего предприятия превышает доступные ресурсы,
                # просто копируем значение из предыдущей ячейки
                dp[i][r] = dp[i - 1][r]

    # оптимальное решение (выбранные предприятия)
    selected_enterprises = []
    i, r = num_enterprises, total_resources
    while i > 0 and r > 0:
        if dp[i][r] != dp[i - 1][r]:
            # Если значение отличается, добавляем текущее предприятие к выбранным
            selected_enterprises.append(i - 1)
            # Уменьшаем доступные ресурсы на стоимость текущего предприятия
            r -= costs[i - 1]
        i -= 1

    # Возвращаем максимальный доход и выбранные предприятия
    return dp[num_enterprises][total_resources], selected_enterprises[::-1]

costs = [1,2,3,4,5,6,7,8]
profits = [2, 3, 4, 7, 6, 5, 4, 8]
total_resources = 12

x = PrettyTable()
fields = ["Предприятие", "Объем вложений", "Прибыль"]
x.field_names = fields
for i in range(len(costs)):
    x.add_row(
        [i+1, costs[i], profits[i]]
    )


print(x)
max_profit, selected_enterprises = resource_allocation(costs, profits, total_resources)
selected_enterprises = list(map(lambda x: x+1 , selected_enterprises))
print(f"Всего ресурсов: {total_resources}")
print(f"Максимальный доход: {max_profit}")
print(f"Выбранные предприятия: {selected_enterprises}")
