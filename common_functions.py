import numpy as np
import random

# lista akcji N - north, S - south, E - east, W - west, P - pick up, L - drop off
ACTIONS = ['N', 'S', 'E', 'W', 'P', 'D']

REWARDS = [-11, -1, 20]  # nagrody


def generate_qtable():
    qtable = [[[[np.zeros(shape=len(ACTIONS)) for i in range(5)] for j in range(5)] for k in range(5)] for l in range(5)]
    return qtable


def generate_start():
    row = random.randint(1, 2)
    col = random.randint(1, 3)
    start = random.randint(0, 3)
    end = random.randint(0, 3)
    return row, col, start, end


def best_action(qtable, pos_row, pos_col, start, end):
    maxi = -100000  # duza arbitralna wartosc rownowazna -nieskonczonosc
    eq_best_actions = list()
    for i in range(len(ACTIONS)):
        if qtable[pos_row][pos_col][start][end][i] > maxi:
            eq_best_actions.clear()
            eq_best_actions.append(i)
            maxi = qtable[pos_row][pos_col][start][end][i]
        elif qtable[pos_row][pos_col][start][end][i] == maxi:
            eq_best_actions.append(i)
    return np.random.choice(eq_best_actions)


def choose_action(pos_row, pos_col, start, end, epsilon, qtable):
    if np.random.uniform() > epsilon:
        # print("random")
        act_num = np.random.choice(len(ACTIONS))
    else:
        act_num = best_action(qtable, pos_row, pos_col, start, end)
    return act_num


def make_action(act_num, pos_row, pos_col, start, end):
    if act_num == ACTIONS.index("N"):
        if pos_row == 0:
            return pos_row, pos_col, start, end, REWARDS[1]
        else:
            return pos_row - 1, pos_col, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("S"):
        if pos_row == 4:
            return pos_row, pos_col, start, end, REWARDS[1]
        else:
            return pos_row + 1, pos_col, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("E"):
        if pos_col == 4:
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 0 and pos_col == 1:
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 3 and (pos_col == 0 or pos_col == 2):
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 4 and (pos_col == 0 or pos_col == 2):
            return pos_row, pos_col, start, end, REWARDS[1]
        else:
            return pos_row, pos_col + 1, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("W"):
        if pos_col == 0:
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 0 and pos_col == 2:
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 3 and (pos_col == 1 or pos_col == 3):
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 4 and (pos_col == 1 or pos_col == 3):
            return pos_row, pos_col, start, end, REWARDS[1]
        else:
            return pos_row, pos_col - 1, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("P"):
        if start == 0 and pos_row == 0 and pos_col == 0:
            return pos_row, pos_col, 4, end, REWARDS[1]
        elif start == 1 and pos_row == 0 and pos_col == 4:
            return pos_row, pos_col, 4, end, REWARDS[1]
        elif start == 2 and pos_row == 4 and pos_col == 0:
            return pos_row, pos_col, 4, end, REWARDS[1]
        elif start == 3 and pos_row == 4 and pos_col == 3:
            return pos_row, pos_col, 4, end, REWARDS[1]
        else:
            return pos_row, pos_col, start, end, REWARDS[0]
    else:  # act_num == ACTIONS.index("D")
        if start != 4:
            return pos_row, pos_col, start, end, REWARDS[0]
        else:
            if end == 0 and pos_row == 0 and pos_col == 0:
                return pos_row, pos_col, start, 4, REWARDS[2]
            elif end == 1 and pos_row == 0 and pos_col == 4:
                return pos_row, pos_col, start, 4, REWARDS[2]
            elif end == 2 and pos_row == 4 and pos_col == 0:
                return pos_row, pos_col, start, 4, REWARDS[2]
            elif end == 3 and pos_row == 4 and pos_col == 3:
                return pos_row, pos_col, start, 4, REWARDS[2]
            else:
                return pos_row, pos_col, start, end, REWARDS[0]


def qtab_maxi(qtable, pos_row, pos_col, start, end):
    maxi = -100000
    for i in range(len(ACTIONS)):
        if qtable[pos_row][pos_col][start][end][i] > maxi:
            maxi = qtable[pos_row][pos_col][start][end][i]
    return maxi
