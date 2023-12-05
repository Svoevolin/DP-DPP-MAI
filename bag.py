import matplotlib.pyplot as plt
import numpy as np

def knapsack_dynamic(weights, values, capacity):
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]

    return dp[n][capacity]

def plot_knapsack_solution(weights, values, capacities):
    for capacity in capacities:
        x = list(range(capacity + 1))
        y = [knapsack_dynamic(weights, values, w) for w in x]

        plt.plot(x, y, marker='o', label=f'Capacity = {capacity}')

    plt.title('Knapsack Problem Dynamic Programming Solution')
    plt.xlabel('Knapsack Capacity')
    plt.ylabel('Maximum Value')
    plt.legend()
    plt.grid(True)
    plt.show()

# Генерация случайных весов и значений
np.random.seed(42)  # Для воспроизводимости результатов
num_items = 5
weights = np.random.randint(1, 10, num_items)
values = np.random.randint(1, 20, num_items)
print(weights,values)
capacities = [20]

# Пример использования с сгенерированными данными
plot_knapsack_solution(weights, values, capacities)
