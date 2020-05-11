import numpy as np
from functools import partial
from typing import Callable, List
import matplotlib.pyplot as plt

NB_MAX_STEPS = 100
NB_MIN_STEPS = 10

class Simulation:
    def __init__(self, nb_systems, duration, cadence, breakdowns, real_mtff, breakdowns_times, nb_steps):
        self.nb_systems = nb_systems
        self.duration = duration
        self.cadence = cadence
        self.breakdowns = breakdowns
        self.breakdowns_times = breakdowns_times
        self.real_mtff = real_mtff
        self.nb_steps = nb_steps

def step_recommendation(duration):
    if (duration < NB_MIN_STEPS):
        return duration

    counter = NB_MAX_STEPS
    while (counter >= NB_MIN_STEPS and duration % counter != 0):
        counter -= 1
    if counter < NB_MIN_STEPS:
        counter = NB_MAX_STEPS
    return counter

def calcul_simulations(nb_systems, duration, probability, nb_steps, beta):
    if (nb_systems <= 0):
        return (1, [])
    if (duration <= 0):
        return (2, [])
    if (nb_steps <= 0):
        return (4, [])
    if (beta <= 0):
        return (4, [])

    proba_type, proba_value = probability
    if (proba_type == 2):
        cadence = 1 / proba_value
    else:
        cadence = proba_value
    if (cadence <= 0 or cadence > 1):
        return (3, [])

    # nb_remains = []
    # nb_remains.append((nb_systems, 1))
    # remains_before = nb_systems
    # for i in range(1, nb_steps):
    #     nb_breakdowns, reliability = simu_expo(remains_before, cadence, (duration / nb_steps) * i)
    #     remains_before = remains_before - nb_breakdowns
    #     nb_remains.append((remains_before, reliability))
    uniform_values = np.random.uniform(size = nb_systems)
    values = generate_weibull_law(cadence, beta, uniform_values)
    nb_breakdowns = get_nb_element_by_step(duration, nb_steps, values)
    real_mtff = np.mean(values)

    # plt.ion()
    plt.plot(np.sort(values), range(nb_systems, 0, -1))
    plt.title('Courbe de survie v(t)')
    plt.ylabel('Nb Systèmes restants')
    plt.xlabel('Temps (defaut : heure)')
    plt.axvline(x=duration, color='gray', linestyle='--')
    print(weibull_law(cadence, beta, np.sort(values), nb_systems))
    plt.plot(np.sort(values), weibull_law(cadence, beta, np.sort(values), nb_systems))
    plt.show(block=False)

    current_simulation = Simulation(nb_systems, duration, cadence, nb_breakdowns, real_mtff, values, nb_steps)
    return (0, current_simulation)

def weibull_law(alpha, beta, times, nb_systems):
    return np.exp(-((times * alpha) ** beta))* nb_systems

# def simu_expo(nb_systems: int, cadence: float, time: float):
#     return breakdowns_simulation(partial(expo_survival_law, cadence), nb_systems, time)

# def expo_survival_law(alpha: float, t: float)-> float:
#     return np.exp(-alpha * t)

def get_nb_element_by_step(duration, nb_steps, values):
    steps = [0] * nb_steps
    for value in values:
        index = int(value // (duration / (nb_steps) ))
        if (index >= nb_steps):
            continue
        steps[index ] += 1

    for index in range(1, nb_steps):
        steps[index] += steps[index - 1]
    return steps

# def use_expo_survival_law(alpha : float, uniform_values : float):
#     return generate_weibull_law(alpha, 1, uniform_values)

# def weibull_survival_law(alpha : float, time : float, beta : float):
#     return np.exp(-(alpha * time) ** beta)

def generate_weibull_law(alpha: float, beta: float, uniform_values: List[float]) -> List[float]:
    a = -np.log(1 - uniform_values) / np.power(alpha, beta)
    b = 1 / beta
    return a ** b

# def breakdowns_simulation(survival_law: Callable[[float], float], N: int, T: float):
#     uniform_values = np.random.uniform(size=N)
#     reliability = survival_law(T)

#     breakdowns = uniform_values[uniform_values < 1 - reliability]
#     return len(breakdowns), reliability