import pickle

from python_codes import common_functions as cf

# lista akcji N - north, S - south, E - east, W - west, P - pick up, D - drop off
ACTIONS = ['N', 'S', 'E', 'W', 'P', 'D']


# parametry programu
EPSILON = 0.999  # strategia zachlanna
ALPHA = 0.5  # wspolczynnik wartosci kroku
GAMMA = 0.9  # wspolczynnik dyskontowania
MAX_EPISODES = 1000  # ilosc gier
FEEDBACK_VAL = 10  # ktore okresy sa zwracane
FIRST_EPISODE = 200  # pierwszy oceniany epizod
REWARDS = [-11, -1, 19]  # nagrody

# wczytujemy uklad wszystkich plansz
file_obj = open("boards_save", 'rb')
BOARDS = pickle.load(file_obj)


# uaktualnia tabele wartosci Q; ma wiedze w jakim stanie byl ruch, ktory ma ocenic,
# w jakim stanie jest po ruchu i jaka nagroda zostala przyznana, na tej podstawie
# wybiera kolejna akcje i po jej wybraniu aktualizuje tabele; zwraca numer wybranej akcji
def update_qtable(qtable, pos_row, pos_col, start, end, reward, act_num, pos_row_new,
                  pos_col_new, start_new, end_new, epsilon, alpha, gamma):
    # stara wartosc w tabeli ocenianego ruchu
    q_act_val = qtable[pos_row][pos_col][start][end][act_num]
    # wybor nowej akcji
    act_num_new = cf.choose_action(pos_row_new, pos_col_new, start_new, end_new, epsilon, qtable)
    # wartosc wybranej akcji w nowym stanie
    q_opt_val = qtable[pos_row_new][pos_col_new][start_new][end_new][act_num_new]
    # wartosc uaktualnienia w tabeli zgodna SARSA
    q_change = reward + gamma * q_opt_val
    # uaktualnienie tabeli
    qtable[pos_row][pos_col][start][end][act_num] += alpha * (q_change - q_act_val)
    return act_num_new


# wykonuje pojedynczy krok, tzn. wykonuje zaplanowana akcje i ukatualnia taebele Q,
# z ktorej uzyskuje kolejna akcje, zwraca nowa pozycje i nowa akcje
def exec_episode(qtable, pos_row, pos_col, start, end, act_num, rew_sum, epsilon, alpha, gamma):
    pos_row_new, pos_col_new, start_new, end_new, reward = cf.make_action(act_num, pos_row, pos_col, start, end)
    rew_sum += reward  # dodanie nagrody do sumy nagrod w celu pozniejszej oceny
    act_num_new = update_qtable(qtable, pos_row, pos_col, start, end, reward, act_num,
                                pos_row_new, pos_col_new, start_new, end_new, epsilon, alpha, gamma)
    return pos_row_new, pos_col_new, start_new, end_new, act_num_new, rew_sum


# wykonuje pelny algorytm SARSA dla problemu; zwraca w ilu epizodach
# osiagnal wymagany prog oraz tablice z sumami nagrod dla poszczegolnych epizodow
def run_sarsa(epsilon, alpha, gamma):
    QTABLE = cf.generate_qtable()  # inicjacja zmiennych
    episodes = list()
    episode = 0
    rewards_sum = list()
    rew_sum = 0
    while not cf.check_avg_val(rew_sum) or episode < MAX_EPISODES:  # petla az do konca nauki
        episode += 1
        if episode % FEEDBACK_VAL == 0 and episode >= FIRST_EPISODE:
            # sprawdzanie czy ten epizod ma zostac zapamietany
            episodes.append(episode)
        pos_row, pos_col, start, end = cf.generate_start()
        act_num = cf.choose_action(pos_row, pos_col, start, end, epsilon, QTABLE)  # wybor pierwszej akcji
        rew_sum = 0  # inicjacja sumy nagrod
        while end != 4:  # petla az do wysadzenia pasazera
            pos_row, pos_col, start, end, act_num, rew_sum = exec_episode(QTABLE, pos_row, pos_col, start, end,
                                                                          act_num, rew_sum, epsilon, alpha, gamma)
        if episode % 10 == 0 and episode >= 200:
            rewards_sum.append(rew_sum)
    return episodes, rewards_sum

run_sarsa(EPSILON, ALPHA, GAMMA)  # wykoananie algorytmu dla przykladowych parametrow
