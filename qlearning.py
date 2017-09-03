import numpy as np
import pickle
import common_functions as cf
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


QTABLE = cf.generate_qtable()


def update_qtable(qtable, pos_row, pos_col, start, end, reward, act_num, pos_row_new, pos_col_new, start_new, end_new):
    # stara warosc w tabeli
    q_act_val = qtable[pos_row][pos_col][start][end][act_num]
    # wartosc optymalnego ruchu w nowym stanie
    q_opt_val = cf.qtab_maxi(qtable, pos_row_new, pos_col_new, start_new, end_new)
    # wartosc uaktualnienia w tabeli zgodna z Q-learningiem
    q_change = reward + GAMMA * q_opt_val
    # uaktualnienie tabel kolka i krzyzyka
    qtable[pos_row][pos_col][start][end][act_num] += ALPHA * (q_change - q_act_val)


def exec_episode(qtable, pos_row, pos_col, start, end):
    act_num = cf.choose_action(pos_row, pos_col, start, end, EPSILON, qtable)
    pos_row_new, pos_col_new, start_new, end_new, reward = cf.make_action(act_num, pos_row, pos_col, start, end)
    update_qtable(qtable, pos_row, pos_col, start, end, reward, act_num, pos_row_new, pos_col_new, start_new, end_new)
    return pos_row_new, pos_col_new, start_new, end_new


for episode in range(MAX_EPISODES):
    pos_row, pos_col, start, end = cf.generate_start()
    if episode > 500:
        print("Episode:", episode + 1)
        print(pos_row, pos_col, start, end)
        time.sleep(1)
        os.system('clear')
    while end != 4:
        if episode > 500:
            boards.print_board(BOARDS[pos_row][pos_col][start][end])
            time.sleep(1)
            os.system('clear')
        pos_row, pos_col, start, end = exec_episode(QTABLE, pos_row, pos_col, start, end)

