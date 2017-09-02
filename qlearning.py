import numpy as np
import pickle
import random
import os
import boards
import time
from os.path import exists

# lista akcji N - north, S - south, E - east, W - west, P - pick up, L - drop off
ACTIONS = ['N', 'S', 'E', 'W', 'P', 'D']


# parametry programu
EPSILON = 0.9  # strategia zachlanna
ALPHA = 0.5  # wspolczynnik wartosci kroku
GAMMA = 0.9  # wspolczynnik dyskontowania
MAX_EPISODES = 550  # ilosc gier
REWARDS = [-11, -1, 20]  # nagrody

# wczytujemy uklad wszystkich plansz
file_obj = open("boards_save", 'rb')
BOARDS = pickle.load(file_obj)


def clear():
    os.system('clear')


def generate_qtable():
    qtable = [[[[np.zeros(shape=len(ACTIONS)) for i in range(5)] for j in range(5)] for k in range(5)] for l in range(5)]
    return qtable


QTABLE = generate_qtable()


def generate_start():
    x = random.randint(1, 3)
    y = random.randint(1, 2)
    start = random.randint(0, 3)
    end = random.randint(0, 3)
    return x, y, start, end


def best_action(qtable, x_pos, y_pos, start, end):
    maxi = -100000  # duza arbitralna wartosc rownowazna -nieskonczonosc
    eq_best_actions = list()
    for i in range(len(ACTIONS)):
        if qtable[x_pos][y_pos][start][end][i] > maxi:
            eq_best_actions.clear()
            eq_best_actions.append(i)
            maxi = qtable[x_pos][y_pos][start][end][i]
        elif qtable[x_pos][y_pos][start][end][i] == maxi:
            eq_best_actions.append(i)
    return np.random.choice(eq_best_actions)


def choose_action(x_pos, y_pos, start, end, epsilon, qtable):
    if np.random.uniform() > epsilon:
        # print("random")
        act_num = np.random.choice(len(ACTIONS))
    else:
        act_num = best_action(qtable, x_pos, y_pos, start, end)
    return act_num


def make_action(act_num, x_pos, y_pos, start, end):
    if act_num == ACTIONS.index("N"):
        if y_pos == 0:
            return x_pos, y_pos, start, end, REWARDS[1]
        else:
            return x_pos, y_pos - 1, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("S"):
        if y_pos == 4:
            return x_pos, y_pos, start, end, REWARDS[1]
        else:
            return x_pos, y_pos + 1, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("E"):
        if x_pos == 0:
            return x_pos, y_pos, start, end, REWARDS[1]
        elif x_pos == 2 and y_pos == 0:
            return x_pos, y_pos, start, end, REWARDS[1]
        elif x_pos == 1 and (y_pos == 3 or y_pos == 4):
            return x_pos, y_pos, start, end, REWARDS[1]
        elif x_pos == 3 and (y_pos == 3 or y_pos == 4):
            return x_pos, y_pos, start, end, REWARDS[1]
        else:
            return x_pos - 1, y_pos, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("W"):
        if x_pos == 4:
            return x_pos, y_pos, start, end, REWARDS[1]
        elif x_pos == 1 and y_pos == 0:
            return x_pos, y_pos, start, end, REWARDS[1]
        elif x_pos == 0 and (y_pos == 3 or y_pos == 4):
            return x_pos, y_pos, start, end, REWARDS[1]
        elif x_pos == 2 and (y_pos == 3 or y_pos == 4):
            return x_pos, y_pos, start, end, REWARDS[1]
        else:
            return x_pos + 1, y_pos, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("P"):
        if start == 0 and x_pos == 0 and y_pos == 0:
            return x_pos, y_pos, 4, end, REWARDS[1]
        elif start == 1 and x_pos == 4 and y_pos == 0:
            return x_pos, y_pos, 4, end, REWARDS[1]
        elif start == 2 and x_pos == 0 and y_pos == 4:
            return x_pos, y_pos, 4, end, REWARDS[1]
        elif start == 3 and x_pos == 3 and y_pos == 4:
            return x_pos, y_pos, 4, end, REWARDS[1]
        else:
            return x_pos, y_pos, start, end, REWARDS[0]
    else:  # act_num == ACTIONS.index("D")
        if start != 4:
            return x_pos, y_pos, start, end, REWARDS[0]
        else:
            if end == 0 and x_pos == 0 and y_pos == 0:
                return x_pos, y_pos, start, 4, REWARDS[2]
            elif end == 1 and x_pos == 4 and y_pos == 0:
                return x_pos, y_pos, start, 4, REWARDS[2]
            elif end == 2 and x_pos == 0 and y_pos == 4:
                return x_pos, y_pos, start, 4, REWARDS[2]
            elif end == 3 and x_pos == 3 and y_pos == 4:
                return x_pos, y_pos, start, 4, REWARDS[2]
            else:
                return x_pos, y_pos, start, end, REWARDS[0]


def qtab_maxi(qtable, x_pos, y_pos, start, end):
    maxi = -100000
    for i in range(len(ACTIONS)):
        if qtable[x_pos][y_pos][start][end][i] > maxi:
            maxi = qtable[x_pos][y_pos][start][end][i]
    return maxi


def update_qtable(qtable, x_pos, y_pos, start, end, reward, act_num, x_pos_new, y_pos_new, start_new, end_new):
    # stara warosc w tabeli
    q_act_val = qtable[x_pos][y_pos][start][end][act_num]
    # wartosc optymalnego ruchu w nowym stanie
    q_opt_val = qtab_maxi(qtable, x_pos_new, y_pos_new, start_new, end_new)
    # wartosc uaktualnienia w tabeli zgodna z Q-learningiem
    q_change = reward + GAMMA * q_opt_val
    # uaktualnienie tabel kolka i krzyzyka
    qtable[x_pos][y_pos][start][end][act_num] += ALPHA * (q_change - q_act_val)


def exec_episode(qtable, x_pos, y_pos, start, end):
    act_num = choose_action(x_pos, y_pos, start, end, EPSILON, qtable)
    print("Action:", ACTIONS[act_num])
    x_pos_new, y_pos_new, start_new, end_new, reward = make_action(act_num, x_pos, y_pos, start, end)
    update_qtable(qtable, x_pos, y_pos, start, end, reward, act_num, x_pos_new, y_pos_new, start_new, end_new)
    return x_pos_new, y_pos_new, start_new, end_new


for episode in range(MAX_EPISODES):
    x_pos, y_pos, start, end = generate_start()
    if episode > 500:
        print("Episode:", episode + 1)
        print(x_pos, y_pos, start, end)
        time.sleep(1)
        clear()
    while end != 4:
        if episode > 500:
            boards.print_board(BOARDS[x_pos][y_pos][start][end])
            time.sleep(1)
            clear()
        x_pos, y_pos, start, end = exec_episode(QTABLE, x_pos, y_pos, start, end)

