import numpy as np
from functools import partial
from typing import Callable

NB_MAX_STEPS = 100
NB_MIN_STEPS = 10

def stepRecommendation(duration):
    if (duration < NB_MIN_STEPS):
        return duration
    
    counter = NB_MAX_STEPS
    while (counter >= NB_MIN_STEPS and duration % counter != 0):
        counter -= 1
    if counter < NB_MIN_STEPS:
        counter = NB_MAX_STEPS
    return counter

def calculSimulations(nbSystems, duration, probability, nbSteps):
    probaType, probaValue = probability
    if (probaType == 2):
        cadence = 1 / probaValue
    else:
        cadence = probaValue

    nb_remains = []
    nb_remains.append((nbSystems, 1))
    remains_before = nbSystems
    for i in range(1, nbSteps):
        nb_breakdowns, reliability = simu_expo(remains_before, cadence, (duration / nbSteps) * i)
        remains_before = remains_before - nb_breakdowns
        nb_remains.append((remains_before, reliability))
    return nb_remains


def simu_expo(nb_systems: int, cadence: float, time: float):
    return breakdowns_simulation(partial(expo_survival_law, cadence), nb_systems, time)


def expo_survival_law(alpha: float, t: float)-> float:
    return np.exp(-alpha * t)


def breakdowns_simulation(survival_law: Callable[[float], float], N: int, T: float):
    uniform_values = np.random.uniform(size=N)
    reliability = survival_law(T)

    breakdowns = uniform_values[uniform_values < 1 - reliability]
    return len(breakdowns), reliability