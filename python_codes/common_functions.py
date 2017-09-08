# Wspolne funkcje dla Q-learningu i SARSA

import numpy as np
import random

# lista akcji N - north, S - south, E - east, W - west, P - pick up, D- drop off
ACTIONS = ['N', 'S', 'E', 'W', 'P', 'D']

REWARDS = [-11, -1, 19]  # nagrody

ACCEPTING_VALUE = 9.7


# generuje wyzerowana tabele Q
def generate_qtable():
    qtable = [[[[np.zeros(shape=len(ACTIONS)) for i in range(5)] for j in range(5)] for k in range(5)]
              for l in range(5)]
    return qtable


# generuje wspolrzedne ukladu poczatkowego tj.lokazliacja taksowki, poczatek i koniec
def generate_start():
    row = random.randint(0, 4)
    col = random.randint(0, 4)
    start = random.randint(0, 3)
    end = random.randint(0, 3)
    return row, col, start, end


# wybiera najlepsza w mysl strategii zachlannej akcje i ja zwraca, jesli kilka jest
# rownie dobrych losuje jedna
def best_action(qtable, pos_row, pos_col, start, end):
    maxi = -100000  # duza arbitralna wartosc rownowazna -nieskonczonosc
    eq_best_actions = list()
    for i in range(len(ACTIONS)):  # sprawdzenie wszystkich akcji
        if qtable[pos_row][pos_col][start][end][i] > maxi:  # jesli lepsza niz do tej pory zerowanie i zmiany
            eq_best_actions.clear()
            eq_best_actions.append(i)
            maxi = qtable[pos_row][pos_col][start][end][i]
        elif qtable[pos_row][pos_col][start][end][i] == maxi:
            eq_best_actions.append(i)
    return np.random.choice(eq_best_actions)  # losowanie najlepszej akcji


# wybiera akcje epsilon-zachlannie, tzn. jesli wylosuje wartosc <= epslion to
# zwraca najlepsza akcje wybrana best_action, wpp. losuje jakas akcje
def choose_action(pos_row, pos_col, start, end, epsilon, qtable):
    if np.random.uniform() > epsilon:
        act_num = np.random.choice(len(ACTIONS))
    else:
        act_num = best_action(qtable, pos_row, pos_col, start, end)
    return act_num


# wykonuje wskazana akcje dla danej sytuacji dla planszy; zwraca nowa pozycje planszy
# oraz nagrode za ruch
def make_action(act_num, pos_row, pos_col, start, end):
    if act_num == ACTIONS.index("N"):
        if pos_row == 0:  # wejscie w gorna krawedz - pozycja bez zmian
            return pos_row, pos_col, start, end, REWARDS[1]
        else:  # poprawny ruch
            return pos_row - 1, pos_col, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("S"):
        if pos_row == 4:  # wejscie w dolna krawedz - pozycja bez zmian
            return pos_row, pos_col, start, end, REWARDS[1]
        else:  # poprawny ruch
            return pos_row + 1, pos_col, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("E"):
        if pos_col == 4:  # wejscie w prawa krawedz - pozycja bez zmian
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 0 and pos_col == 1:  # proby przejscia przez zablokawane krawedzie
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 3 and (pos_col == 0 or pos_col == 2):
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 4 and (pos_col == 0 or pos_col == 2):
            return pos_row, pos_col, start, end, REWARDS[1]
        else:  # poprawny ruch
            return pos_row, pos_col + 1, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("W"):
        if pos_col == 0:  # wejscie w lewa krawedz - pozycja bez zmian
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 0 and pos_col == 2:  # proby przejscia przez zablokawane krawedzie
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 3 and (pos_col == 1 or pos_col == 3):
            return pos_row, pos_col, start, end, REWARDS[1]
        elif pos_row == 4 and (pos_col == 1 or pos_col == 3):
            return pos_row, pos_col, start, end, REWARDS[1]
        else:  # poprawny ruch
            return pos_row, pos_col - 1, start, end, REWARDS[1]
    elif act_num == ACTIONS.index("P"):
        if start == 0 and pos_row == 0 and pos_col == 0:  # poprawne zabranie pasazera
            return pos_row, pos_col, 4, end, REWARDS[1]
        elif start == 1 and pos_row == 0 and pos_col == 4:
            return pos_row, pos_col, 4, end, REWARDS[1]
        elif start == 2 and pos_row == 4 and pos_col == 0:
            return pos_row, pos_col, 4, end, REWARDS[1]
        elif start == 3 and pos_row == 4 and pos_col == 3:
            return pos_row, pos_col, 4, end, REWARDS[1]
        else:  # bledne zabranie pasazera
            return pos_row, pos_col, start, end, REWARDS[0]
    else:  # act_num == ACTIONS.index("D")
        if start != 4:  # pasazer niezabrany - blad
            return pos_row, pos_col, start, end, REWARDS[0]
        else:
            if end == 0 and pos_row == 0 and pos_col == 0:  # wysadzanie pasazera w dobrym miejscu
                return pos_row, pos_col, start, 4, REWARDS[2]
            elif end == 1 and pos_row == 0 and pos_col == 4:
                return pos_row, pos_col, start, 4, REWARDS[2]
            elif end == 2 and pos_row == 4 and pos_col == 0:
                return pos_row, pos_col, start, 4, REWARDS[2]
            elif end == 3 and pos_row == 4 and pos_col == 3:
                return pos_row, pos_col, start, 4, REWARDS[2]
            else:  # wysadzanie pasazera w zlym miejscu
                return pos_row, pos_col, start, end, REWARDS[0]


# zwraca maksymalna wartosc Q w danym stanie
def qtab_maxi(qtable, pos_row, pos_col, start, end):
    maxi = -100000  # arbitralna bardzo mala wartosc rownowazna -nieskonczonosc
    for i in range(len(ACTIONS)):
        if qtable[pos_row][pos_col][start][end][i] > maxi:
            maxi = qtable[pos_row][pos_col][start][end][i]
    return maxi


last_100_episodes = list()  # lista 100 poprzenich prob


# sprawdza czy w 100 ostatnich probach srednia gry jest powyzej ACCEPTING_VALUE
def check_avg_val(rew_sum):
    if len(last_100_episodes) < 100:  # jesli mniej niz 100 epizodow to tylko dodajemy ten
        last_100_episodes.append(rew_sum)
        return False
    else:
        last_100_episodes.remove(last_100_episodes[0])  # usuniecie najwczesniejszego epizodu
        last_100_episodes.append(rew_sum)  # dodanie najnowszego epizodu
        if sum(last_100_episodes) / len(last_100_episodes) >= ACCEPTING_VALUE:  # sprawdzenie warunku
            return True
        else:
            return False
