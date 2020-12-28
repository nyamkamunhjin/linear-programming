#%%
"""
Minimize z = 600x1 + 500x2 [600, 500]
Subject to  2x1 + x2 >= 80 [2, 1]
            x1 + 2x2 >= 60 [1, 2]
            x1, x2 >= 0
maximize => -M
minimize => +M

z = [600, 500]
constraints = [[2, 1], [1, 2]]
s = [-1, -1]
a = [1, 1]

"""

#%%
import numpy as np
import pandas


def print_table(table, headers):
    # print(table)
    df = pd.DataFrame(table, columns=headers[0], index=headers[1])
    print(df)


def create_table(z, constraints, s, a, solution, goal):
    cj = z.copy()

    # add slacks to profit
    for _ in range(len(s)):
        cj.append(0)

    # add bigM (a's) to profit
    for _ in range(len(a)):
        cj.append("M")

    # print(cj)

    table = np.array(constraints)

    table = np.c_[table, -np.eye(len(s))]
    table = np.c_[table, np.eye(len(a))]
    table = np.c_[table, solution]
    table = np.r_[[cj + [0]], table]

    # append cb
    cb = [0] + a
    print(cb)
    table = np.c_[cb, table]
    print(table)

    rowNames = []
    colNames = []

    for i in range(len(constraints[0])):
        rowNames.append("x" + i)

    for i in range(len(s)):
        rowNames.append("s" + i)

    for i in range(len(a)):
        rowNames.append("a" + i)

    for i in range(constraints)
    # print_table(table,)
    # for i in range(len(constraints)):


#%%
z = [600, 500]
constraints = [[2, 1], [1, 2]]
s = [-1, -1]
a = [1, 1]
solution = [80, 60]

create_table(z, constraints, s, a, solution, "minimize")
# %%
