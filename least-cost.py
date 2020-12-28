#%%

import numpy as np
import pandas as pd


def print_table(table, supply, demand):
    # print(demand)
    table = np.r_[table, [demand]]
    # print(table)
    table = np.c_[table, supply + [0]]
    df = pd.DataFrame(table)
    print(df)


def least_cost(table, supply, demand):
    table_copy = np.array(table.copy())

    if sum(supply) > sum(demand):
        # add demand col
        demand.append(sum(supply) - sum(demand))
        table_copy = np.c_[table_copy, np.zeros((len(supply), 1))]
    else:
        # add supply row
        if sum(supply) < sum(demand):
            supply.append(sum(demand) - sum(supply))
            table_copy = np.r_[table_copy, np.zeros((1, len(demand)))]

    supply_table = np.zeros(np.array(table_copy).shape)
    max_num = np.max(table_copy) + 1

    multiply_table = table_copy.copy()

    # print(table_copy)
    # print(supply)
    # print(demand)

    i = 0
    while sum(demand) != 0:
        i = i + 1
        print("Iteration", i)
        min_index = np.unravel_index(table_copy.argmin(), table_copy.shape)

        # min_idx_sup_dem = supply[min_index[0]], demand[min_index[1]]

        if supply[min_index[0]] >= demand[min_index[1]]:
            # add cost to supply table
            supply_table[min_index] = demand[min_index[1]]
            # subtract cost from supply
            supply[min_index[0]] = supply[min_index[0]] - demand[min_index[1]]
            # subtract cost from demand
            demand[min_index[1]] = 0
        else:
            # add cost to supply table
            supply_table[min_index] = supply[min_index[0]]
            # subtract cost from demand
            demand[min_index[1]] = demand[min_index[1]] - supply[min_index[0]]
            # subtract cost from supply
            supply[min_index[0]] = 0

        table_copy[min_index] = max_num

        print_table(supply_table, supply, demand)

    answer = np.sum(np.multiply(supply_table, multiply_table))
    print("Answer:", answer)


#%%

table = [[6, 7, 8, 10], [4, 7, 13, 5], [7, 8, 7, 8]]
supply = [100, 200, 300]
demand = [150, 100, 275, 75]

least_cost(table, supply, demand)
# %% Бодлого 3
table = [[1, 2, 1], [5, 7, 4], [3, 8, 2]]
supply = [30, 20, 50]
demand = [50, 60, 60]

least_cost(table, supply, demand)


# %% Бодлого 13
table = [[4, 5, 2, 4, 3, 1], [3, 1, 3, 5, 2, 6], [2, 7, 6, 1, 6, 3]]
supply = [60, 80, 60]
demand = [20, 20, 35, 25, 40, 60]
least_cost(table, supply, demand)

# %% Бодлого 23
table = [
    [25, 28, 20, 25, 7],
    [27, 5, 11, 23, 10],
    [1, 25, 14, 16, 16],
    [8, 6, 4, 16, 18],
]
supply = [100, 120, 140, 180]
demand = [70, 80, 40, 110, 30]
least_cost(table, supply, demand)
# %% Бодлого 33
table = [[3, 1, 5, 4], [2, 4, 6, 7], [4, 3, 5, 8], [9, 3, 8, 1]]
supply = [80, 110, 50, 60]
demand = [100, 40, 90, 70]
least_cost(table, supply, demand)

# %% Бодлого 43
table = [[3, 5, 7, 11], [1, 4, 6, 3], [8, 8, 12, 7]]
supply = [100, 130, 70]
demand = [150, 120, 80, 50]
least_cost(table, supply, demand)
# %%
