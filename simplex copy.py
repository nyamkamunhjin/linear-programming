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
    # table = np.r_[np.array(constraints), np.array([profit])]
    table = np.array(constraints)

    # big m slacks
    a_slacks = np.zeros((len(slacks), 1))

    # cb column items
    cb = []

    for i in range(len(slacks)):
        col = np.zeros((len(slacks), 1))
        col[i, 0] = slacks[i]

        table = np.c_[table, col]

        if slacks[i] == -1:
            if goal == "maximize":
                cb.append(-10)
            else:
                cb.append(10)

            if a_slacks.all() == 0:
                a_slacks = -col
            else:
                a_slacks = np.c_[a_slacks, -col]
        else:
            cb.append(0)
            # print(a_slacks)
        # print(col)

    for i in range(len(slacks)):
        profit.append(0)

    for i in range(a_slacks.shape[1]):
        if goal == "maximize":
            profit.append(-10)
        else:
            profit.append(10)

    table = np.c_[table, a_slacks]
    table = np.c_[table, answers]
    table = np.c_[cb, table]
    print(profit)
    print(table)

    # Objective function value
    ofv = (
        table[:, table.shape[1] - 1][0] * cb[0]
        + table[:, table.shape[1] - 1][1] * cb[1]
    )

    print(ofv)

    # arr = np.eye(table.shape[0])
    # np.fill_diagonal(arr, slacks + [1])

    # add columns
    # table = np.c_[table, arr, answers + [0]]
    # table = np.c_[table, answers + [0]]
    # print(table)

    # if goal == "minimize":
    #     table = np.transpose(table)

    #     arr = np.eye(table.shape[0])
    #     np.fill_diagonal(arr, slacks + [1])

    #     arr[: arr.shape[0] - 1, : arr.shape[1] - 1] = np.negative(
    #         arr[: arr.shape[0] - 1, : arr.shape[1] - 1]
    #     )

    # table[table.shape[0] - 1, : table.shape[1] - 1] = np.negative(
    #     table[table.shape[0] - 1, : table.shape[1] - 1]
    # )

    # print_table(table)

    # create headers
    # rowNames = []
    # colNames = []

    # for i in range(1, table.shape[1]):
    #     colNames = colNames + ["x" + str(i)]

    # for i in range(1, table.shape[0]):
    #     rowNames = rowNames + ["s" + str(i)]

    # rowNames = rowNames + ["p"]
    # colNames = colNames + rowNames + ["_"]

    # table = np.c_[table[:, : table.shape[1] - 1], arr, table[:, table.shape[1] - 1]]

    # # print((colNames, rowNames))
    # return table, (colNames, rowNames)


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
                        + str(round(table[index, table.shape[1] - 1]))
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
                    + str(round(table[table.shape[0] - 1, i]))
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
    return table


# %%

"""
minimize: p = 7x + 15y + 20z
Subject to: 2x + 4y + 6z >= 24
            3x + 9y + 6z >= 30
            x, y, z => 0

"""
testConstraints = [[2, 4, 6], [3, 9, 6]]
testAnswer = [24, 30]
slacks = [-1, -1]
profit = [7, 15, 30]
# table = simplex(testConstraints, testAnswer, slacks, profit, "maximize")
table, headers = create_table(testConstraints, testAnswer, slacks, profit, "minimize")
print_table(table, headers)
# %%

"""
maximize: p = 2x + y
Subject to: x - y <= 11
            x + 3y >= 15
            x, y >= 0

"""
testConstraints = [[1, -1], [1, 3]]
testAnswer = [11, 15]
slacks = [1, -1]
profit = [2, 1]
# table = simplex(testConstraints, testAnswer, slacks, profit, "maximize")
table, headers = create_table(testConstraints, testAnswer, slacks, profit, "maximize")
print_table(table, headers)
# %%
