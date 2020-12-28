#%%


import numpy as np
import pandas as pd


def print_table(table, headers):
    # print(table)
    df = pd.DataFrame(table, columns=headers[0], index=headers[1])
    print(df)


def create_table(constraints, answers, slacks, profit, goal):
    print("creating table")
    # add profit (x1, x2, ...) to table row
    table = np.r_[np.array(constraints), np.array([profit])]

    # slack identity matrix
    arr = np.eye(table.shape[0])
    np.fill_diagonal(arr, slacks + [1])

    # add columns
    # table = np.c_[table, arr, answers + [0]]
    table = np.c_[table, answers + [0]]
    print(table)

    if goal == "minimize":
        table = np.transpose(table)

        arr = np.eye(table.shape[0])
        np.fill_diagonal(arr, slacks + [1])

        arr[: arr.shape[0] - 1, : arr.shape[1] - 1] = np.negative(
            arr[: arr.shape[0] - 1, : arr.shape[1] - 1]
        )

    table[table.shape[0] - 1, : table.shape[1] - 1] = np.negative(
        table[table.shape[0] - 1, : table.shape[1] - 1]
    )

    print(table)

    # create headers
    rowNames = []
    colNames = []

    for i in range(1, table.shape[1]):
        colNames = colNames + ["x" + str(i)]

    for i in range(1, table.shape[0]):
        rowNames = rowNames + ["s" + str(i)]

    rowNames = rowNames + ["p"]
    colNames = colNames + rowNames + ["_"]

    table = np.c_[table[:, : table.shape[1] - 1], arr, table[:, table.shape[1] - 1]]

    # print((colNames, rowNames))
    return table, (colNames, rowNames)


def find_pivot(table, headers):
    print("finding pivot")
    # find most negative number index from bottom row
    min_idx = np.argmin(table[table.shape[0] - 1])
    # min_idx = np.where(table[table.shape[0] - 1] > 0)
    # print(table[table.shape[0] - 1, min_idx])
    a = table[: table.shape[0] - 1, min_idx]
    if np.max(a) < 0:
        print("Unbounded")
        raise Exception("Unbounded")

    b = table[: table.shape[0] - 1, table.shape[1] - 1]
    divided_matrix = b / a
    print(a, b, divided_matrix)
    # print(divided_matrix)

    min = max(divided_matrix)
    index = -1
    for i in range(len(divided_matrix)):
        print(divided_matrix[i])
        if divided_matrix[i] > 0 and divided_matrix[i] <= min:
            min = divided_matrix[i]
            index = i

    if index < 0:
        raise Exception("Unbounded")
    # print()
    # get 2d pivot index

    pivot_idx = index, min_idx

    # swap columns, index
    colNames, rowNames = headers

    rowNames[index] = colNames[min_idx]

    print(pivot_idx)
    return pivot_idx


def row_operation(table, pivot_idx):
    # make pivot entry 1
    table[pivot_idx[0]] = table[pivot_idx[0]] / table[pivot_idx]

    # make other rows pivot col 0
    print("make other rows pivot col 0")

    subtract = np.array(table[:, pivot_idx[1]])
    subtract[pivot_idx[0]] = 0

    subtractRow = np.dot(
        np.diag(subtract), np.tile(table[pivot_idx[0]], (table.shape[0], 1))
    )
    table = table - subtractRow

    return table


def print_answer(headers, table, goal):
    colNames, rowNames = headers
    answer = "Answer: "

    if goal == "maximize":
        for i in range(len(colNames)):
            if colNames[i][0] == "x":
                if colNames[i] in rowNames:

                    index = rowNames.index(colNames[i])
                    answer = (
                        answer
                        + colNames[i]
                        + " = "
                        + str(table[index, table.shape[1] - 1])
                        + ", "
                    )

                else:
                    answer = answer + colNames[i] + " = 0, "

        print(answer)
        # print minimize
    else:
        for i in range(len(colNames)):
            if colNames[i][0] == "s":
                answer = (
                    answer
                    + colNames[i]
                    + " = "
                    + str(table[table.shape[0] - 1, i])
                    + ", "
                )

        print(answer)


def simplex(constraints, answers, slacks, profit, goal="maximize"):
    table, headers = create_table(constraints, answers, slacks, profit, goal)
    print_table(table, headers)

    while np.min(table[table.shape[0] - 1]) < 0:
        pivot_idx = find_pivot(table, headers)
        table = row_operation(table, pivot_idx)
        print_table(table, headers)

    print_answer(headers, table, goal)
    # answer = "Answer: "
    # for i in range(len(colNames)):
    #     if colNames[i][0] == "x":
    #         if colNames[i] in rowNames:

    #             index = rowNames.index(colNames[i])
    #             answer = (
    #                 answer
    #                 + colNames[i]
    #                 + " = "
    #                 + str(round(table[index, table.shape[1] - 1]))
    #                 + ", "
    #             )

    #         else:
    #             answer = answer + colNames[i] + " = 0, "

    # print(answer)

    return table


# %%
"""
2x + y <= 5
x + 2y <= 4
x => 0, y => 0

Maximize: p = 2x + 5y

2x + y <= 5  --->  [2, 1]
x + 2y <= 4  --->  [1, 2]
p = 2x + 5y  --->  [2, 5]                

"""

testConstraints = [[2, 1], [1, 2]]
testAnswer = [5, 4]
slacks = [1, 1]
profit = [2, 5]

table = simplex(testConstraints, testAnswer, slacks, profit)
# %%
testConstraints = [[2, 4], [3, 2]]
testAnswer = [220, 150]
slacks = [1, 1]
profit = [4, 3]

table = simplex(testConstraints, testAnswer, slacks, profit)
# %%
testConstraints = [[5, 3, 2], [4, 4, 4], [4, 2, 5]]
testAnswer = [60, 72, 100]
slacks = [1, 1, 1]
profit = [10, 5, 8]
table = simplex(testConstraints, testAnswer, slacks, profit)
# %%
testConstraints = [[2, 1], [0, 0], [5, 4], [0, 2], [0, 0]]
testAnswer = [600, 225, 1000, 150, 0]
slacks = [1, 1, 1, -1, -1]
profit = [3, 4]
table = simplex(testConstraints, testAnswer, slacks, profit)

# %%
# minimize
testConstraints = [[1, 2], [7, 6]]
testAnswer = [4, 20]
slacks = [-1, -1]
profit = [14, 20]
table = simplex(testConstraints, testAnswer, slacks, profit, "minimize")
# %%
# minimize
testConstraints = [[2, 1], [1, 2]]
testAnswer = [8, 8]
slacks = [-1, -1]
profit = [3, 9]
table = simplex(testConstraints, testAnswer, slacks, profit, "minimize")
# %%
testConstraints = [[0.2, 0.32], [1, 1], [1, 1]]
testAnswer = [0.25, 1, 1]
slacks = [-1, -1, 1]
profit = [80, 60]
table = simplex(testConstraints, testAnswer, slacks, profit, "minimize")
# %%
testConstraints = [[-1, 2, 1, 0, 0], [2, 1, 1, 1, 2], [1, -1, 0, 0, 1]]
testAnswer = [2, 6, 1]
slacks = [-1, 1, -1]
profit = [1, 2, 1, -1, 1]
table = simplex(testConstraints, testAnswer, slacks, profit)
#%%
testConstraints = [[1, -1, 2, 1, 5], [2, -1, 1, -1, 5], [1, 0, 1, 2, 6]]
testAnswer = [5, 5, 6]
slacks = [-1, -1, -1]
profit = [1, 3, -1, -1, -1]
table = simplex(testConstraints, testAnswer, slacks, profit, "minimize")
# %%
