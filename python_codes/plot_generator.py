import os

import matplotlib.pyplot as plt
import numpy as np

from python_codes import qlearning as ql
from python_codes import sarsa as sa

# parametry programu: wartosc startowa, koncowa i krok dla kazdego parametru
START_EPSILON = 0.9999
STOP_EPSILON = 0.99995
STEP_EPSILON = 0.00001
START_ALPHA = 0.4
STOP_ALPHA = 0.61
STEP_ALPHA = 0.04
START_GAMMA = 0.7
STOP_GAMMA = 0.91
STEP_GAMMA = 0.05

# wbor i stworzenie folderow na wykresy
ql_dir = "qlearning_plots2"
sa_dir = "sarsa_plots2"
os.makedirs(ql_dir)
os.makedirs(sa_dir)


# robi wykres dla danych osi x i y
def make_plot(plot_name, x_axis, y_axis):
    plt.plot(x_axis, y_axis)
    plt.xlabel('episode')
    plt.ylabel('rewards sum')
    plt.savefig(plot_name)
    plt.close()


# przejscie po wszystkich kombinacjach parametrow
for epsilon in np.arange(START_EPSILON, STOP_EPSILON, STEP_EPSILON):
    for alpha in np.arange(START_ALPHA, STOP_ALPHA, STEP_ALPHA):
        for gamma in np.arange(START_GAMMA, STOP_GAMMA, STEP_GAMMA):
            # uzyskanie pojedynczych danych dla Q-learningu i SARSA
            ql_episodes, ql_rewards = ql.run_qlearning(epsilon, alpha, gamma)
            sa_episodes, sa_rewards = sa.run_sarsa(epsilon, alpha, gamma)
            # nazwy wykresow
            ql_plot_name = ql_dir + "/EPS:" + "{0:.3f}".format(epsilon) + " ALP:" + "{0:.3f}".format(alpha)\
                           + " GAM:" + "{0:.3f}".format(gamma) + ".png"
            sa_plot_name = sa_dir + "/EPS:" + "{0:.3f}".format(epsilon) + " ALP:" + "{0:.3f}".format(alpha)\
                            + " GAM:" + "{0:.3f}".format(gamma) + ".png"
            # rysowanie wykresow
            make_plot(ql_plot_name, ql_episodes, ql_rewards)
            make_plot(sa_plot_name, sa_episodes, sa_rewards)

