import numpy as np
import pickle
from colorama import Fore, Back, Style
from os.path import exists


def print_sign(sign, val):
    if val == 0:
        print(sign, end='')
    elif val == 1:
        print(Back.YELLOW + sign + Style.RESET_ALL, end='')
    elif val == 2:
        print(Fore.BLUE + sign + Style.RESET_ALL, end='')
    elif val == 3:
        print(Fore.BLUE + Back.YELLOW + sign + Style.RESET_ALL, end='')
    elif val == 4:
        print(Fore.RED + sign + Style.RESET_ALL, end='')
    elif val == 5:
        print(Fore.RED + Back.YELLOW + sign + Style.RESET_ALL, end='')
    elif val == 6:
        print(Fore.MAGENTA + sign + Style.RESET_ALL, end='')
    else:
        print(Fore.MAGENTA + Back.YELLOW + sign + Style.RESET_ALL, end='')


# wypisuje symbol zamiast wart. liczbowej
def print_first_row(row):
    print("|", end='')
    print_sign("R", row[0])
    print(":", end='')
    print_sign(" ", row[1])
    print("|", end='')
    print_sign(" ", row[2])
    print(":", end='')
    print_sign(" ", row[3])
    print(":", end='')
    print_sign("G", row[4])
    print("|")


def print_second_and_third_row(row):
    print("|", end='')
    print_sign(" ", row[0])
    print(":", end='')
    print_sign(" ", row[1])
    print(":", end='')
    print_sign(" ", row[2])
    print(":", end='')
    print_sign(" ", row[3])
    print(":", end='')
    print_sign(" ", row[4])
    print("|")


def print_forth_row(row):
    print("|", end='')
    print_sign(" ", row[0])
    print("|", end='')
    print_sign(" ", row[1])
    print(":", end='')
    print_sign(" ", row[2])
    print("|", end='')
    print_sign(" ", row[3])
    print(":", end='')
    print_sign(" ", row[4])
    print("|")


def print_fifth_row(row):
    print("|", end='')
    print_sign("Y", row[0])
    print("|", end='')
    print_sign(" ", row[1])
    print(":", end='')
    print_sign(" ", row[2])
    print("|", end='')
    print_sign("B", row[3])
    print(":", end='')
    print_sign(" ", row[4])
    print("|")


# wypisuje searator wierszy
def print_border():
    print("+---------+")


# wypisuje cala plansze
def print_board(board):
    print_border()
    print_first_row(board[0])
    print_second_and_third_row(board[1])
    print_second_and_third_row(board[2])
    print_forth_row(board[3])
    print_fifth_row(board[4])
    print_border()


def get_pos_cor(pos_num):
    if pos_num == 0:
        return 0, 0
    elif pos_num == 1:
        return 0, 4
    elif pos_num == 2:
        return 4, 0
    elif pos_num == 3:
        return 4, 3
    else:
        return -1, -1


def generate_board(start, end, curr_pos_row, curr_pos_col):
    board = np.zeros(shape=(5, 5))
    start_row, start_col = get_pos_cor(start)
    end_row, end_col = get_pos_cor(end)
    if start < 4:
        board[start_row][start_col] += 4
    board[end_row][end_col] += 2
    board[curr_pos_row][curr_pos_col] += 1
    return board


# generuje liste list wszystkich mozliwych do uzyskania plansz
def generate_boards():
    boards = [[[[np.zeros(shape=(5, 5)) for i in range(4)] for j in range(5)] for k in range(5)] for l in range(5)]
    for row in range(5):
        for col in range(5):
            for start in range(5):
                for end in range(4):
                    boards[row][col][start][end] = generate_board(start, end, row, col)
    return boards

# lista wszystkich mozliwych ukladow w grze
file_name = "boards_save"

if not exists(file_name):
    BOARDS = generate_boards()
    with open(file_name, 'wb') as f:
        pickle.dump(BOARDS, f)
