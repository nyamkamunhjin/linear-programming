# %%

"""
2x + y <= 5
x + 2y <= 4
x => 0, y => 0

Maximize: p = 2x + 5y

2x + y <= 5  --->  [2, 1, '<=', 5]
x + 2y <= 4  --->  [1, 2, '<=', 4]
p = 2x + 5y  --->  [2, 5]                

"""
import numpy as np
import pandas as pd

# constraints = [[2, 1, "<=", 5], [1, 2, "<=", 4]]


def print_table(table, headers):
    df = pd.DataFrame(table, columns=headers[0], index=headers[1])
    print(df)


def create_table(constraints, answers, slacks, profit):
    print("creating table")
    # add profit (x1, x2, ...) to table row
    table = np.r_[np.array(constraints), np.array([profit]) * -1]

    # slack identity matrix
    arr = np.eye(table.shape[0])
    np.fill_diagonal(arr, slacks + [1])

    # add columns
    table = np.c_[table, arr, testAnswer + [0]]

    return table


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
    # print(divided_matrix)

    min = max(divided_matrix)
    index = -1
    for i in range(len(divided_matrix)):
        if divided_matrix[i] > 0 and divided_matrix[i] < min:
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

    subtractRow = np.dot(np.diag(subtract), np.tile(
        table[pivot_idx[0]], (table.shape[0], 1)))
    table = table - subtractRow

    return table


def simplex(constraints, answers, slacks, profit, headers, goal):
    table = create_table(constraints, answers, slacks, profit)
    print_table(table, headers)

    while np.min(table[table.shape[0] - 1]) < 0:
        pivot_idx = find_pivot(table, headers)
        table = row_operation(table, pivot_idx)
        print_table(table, headers)

    colNames, rowNames = headers

    answer = "Answer: "
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

    return table


# %%
testConstraints = [[2, 1], [1, 2]]
testAnswer = [5, 4]
slacks = [1, 1]
profit = [2, 5]
goal = "maximize"
headers = ["x1", "x2", "s1", "s2", "p", "_"], ["s1", "s2", "p"]
table = simplex(testConstraints, testAnswer,
                slacks, profit, headers, "maximize")
# %%
testConstraints = [[2, 4], [3, 2]]
testAnswer = [220, 150]
slacks = [1, 1]
profit = [4, 3]
goal = "maximize"
headers = ["x1", "x2", "s1", "s2", "p", "_"], ["s1", "s2", "p"]
table = simplex(testConstraints, testAnswer,
                slacks, profit, headers, "maximize")
# %%
testConstraints = [[5, 3, 2], [4, 4, 4], [4, 2, 5]]
testAnswer = [60, 72, 100]
slacks = [1, 1, 1]
profit = [10, 5, 8]
# goal = "maximize"
headers = ["x1", "x2", "x3", "s1", "s2",
           "s3", "p", "_"], ["s1", "s2", "s3", "p"]
table = simplex(testConstraints, testAnswer,
                slacks, profit, headers, "maximize")
# %%
