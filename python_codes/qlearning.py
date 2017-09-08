import pickle

from python_codes import common_functions as cf

# lista akcji N - north, S - south, E - east, W - west, P - pick up, D - drop off
ACTIONS = ['N', 'S', 'E', 'W', 'P', 'D']


# parametry programu
EPSILON = 0.9995  # strategia zachlanna
ALPHA = 0.5  # wspolczynnik wartosci kroku
GAMMA = 0.9  # wspolczynnik dyskontowania
MAX_EPISODES = 1000  # ilosc gier
FEEDBACK_VAL = 10  # ktore okresy sa zwracane
FIRST_EPISODE = 200  # pierwszy oceniany epizod


# wczytujemy uklad wszystkich plansz
file_obj = open("boards_save", 'rb')
BOARDS = pickle.load(file_obj)


# uaktualnia tabele wartosci Q; ma wiedze w jakim stanie byl ruch, ktory ma ocenic,
# w jakim stanie jest po ruchu i jaka nagroda zostala przyznana, na tej podstawie
# ocenia dany ruch
def update_qtable(qtable, pos_row, pos_col, start, end, reward, act_num, pos_row_new, pos_col_new, start_new,
                  end_new, alpha, gamma):
    # stara warosc w tabeli
    q_act_val = qtable[pos_row][pos_col][start][end][act_num]
    # wartosc optymalnego ruchu w nowym stanie
    q_opt_val = cf.qtab_maxi(qtable, pos_row_new, pos_col_new, start_new, end_new)
    # wartosc uaktualnienia w tabeli zgodna z Q-learningiem
    q_change = reward + gamma * q_opt_val
    # uaktualnienie tabeli
    qtable[pos_row][pos_col][start][end][act_num] += alpha * (q_change - q_act_val)


# wykonuje pojedynczy krok, tzn. wybiera nowa akcje, wykonuje ja i aktualizuje tabele Q
# zwraca nowa pozycje
def exec_episode(qtable, pos_row, pos_col, start, end, rew_sum, epsilon, alpha, gamma):
    act_num = cf.choose_action(pos_row, pos_col, start, end, epsilon, qtable)  # wybor akcji
    # wykoananie wybranej akcji
    pos_row_new, pos_col_new, start_new, end_new, reward = cf.make_action(act_num, pos_row, pos_col, start, end)
    rew_sum += reward  # dodanie nagrody do sumy nagrod w celu pozniejszej oceny
    update_qtable(qtable, pos_row, pos_col, start, end, reward, act_num, pos_row_new, pos_col_new, start_new,
                  end_new, alpha, gamma)
    return pos_row_new, pos_col_new, start_new, end_new, rew_sum


# wykonuje pelny algorytm Q-laerning dla problemu; zwraca w ilu epizodach
# osiagnal wymagany prog oraz tablice z sumami nagrod dla poszczegolnych epizodow
def run_qlearning(epsilon, alpha, gamma):
    QTABLE = cf.generate_qtable()  # inicjacja zmiennych
    episodes = list()
    episode = 0
    rewards_sum = list()
    rew_sum = 0
    while not cf.check_avg_val(rew_sum) or episode < MAX_EPISODES:
        episode += 1
        if episode % FEEDBACK_VAL == 0 and episode >= FIRST_EPISODE:
            # sprawdzenie czy ten epizod ma zostac zapamietany
            episodes.append(episode)
        pos_row, pos_col, start, end = cf.generate_start()
        rew_sum = 0  # inicjacja sumy nagrod
        while end != 4:  # petla az do wysadzenia pasazera
            pos_row, pos_col, start, end, rew_sum = exec_episode(QTABLE, pos_row, pos_col, start, end,
                                                                 rew_sum, epsilon, alpha, gamma)
        if episode % 10 == 0 and episode >= 200:
            rewards_sum.append(rew_sum)
    return episodes, rewards_sum

run_qlearning(EPSILON, ALPHA, GAMMA)  # wykoananie algorytmu dla przykladowych parametrow
