import random
from math import floor
from random import shuffle
import numpy as np
import copy

from generator import RandomNumberGenerator


def generate_data(seed, n, machines):
    rng = RandomNumberGenerator(seed)
    p_array = []
    d_array = []
    A = 0
    for machine in range(machines):
        p_for_machine = []
        for task in range(n):
            p = rng.nextInt(1, 99)
            p_for_machine.append(p)
            A += p
        p_array.append(p_for_machine)
    B = floor(A / 2)
    A = floor(A / 6)
    for task in range(n):
        d_array.append(
            rng.nextInt(A, B))  # [A, B] - zakres czasu w którym generuje się deadline dla każdego zadania

    return {"n": n,
            "machines": machines,
            "pij": p_array,
            "dj": d_array
            }



class Task:
    def __init__(self, p=0, d=0, id=0):
        self.p = p
        self.d = d
        self.id = id

    def __str__(self):
        #return "TASK ID " + str(self.id)
        return f"Task(p={self.p}, d={self.d})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        if not isinstance(other, Task):
            return NotImplemented
        return self.id == other.id


class Harmonogram:
    def __init__(self, machines=0, tasks=[]):
        self.machines = machines
        self.tasks = tasks
        self.n = len(tasks)
        self.times = [[] for i in range(machines)]

        self.find_harmonogram()
        # print(self.times)

    # funkcja obliczająca harmonogram
    def find_harmonogram(self):
        for machine in range(self.machines):
            for task, j in zip(self.tasks, range(self.n)):
                if j == 1 - 1 and machine == 1 - 1:
                    self.times[machine].append(task.p[machine])
                elif j > 1 - 1 and machine == 1 - 1:
                    self.times[machine].append(self.times[machine][j - 1] + task.p[machine])
                elif j == 1 - 1 and machine > 1 - 1:
                    self.times[machine].append(self.times[machine - 1][j] + task.p[machine])
                elif j > 1 - 1 and machine > 1 - 1:
                    self.times[machine].append(
                        max(self.times[machine - 1][j], self.times[machine][j - 1]) + task.p[machine])

    # 1 kryterium - Czas zakończenia wszystkich zadań
    def makespan(self):
        c_max = 0
        for j in range(self.n):
            if c_max < self.times[self.machines - 1][j]:
                c_max = self.times[self.machines - 1][j]
        return c_max

    # 2 kryterium - Suma czasów zakończenia wszystkich zadań
    def total_flowtime(self):
        F_array = [self.times[self.machines - 1][j] for j in range(self.n)]
        F_sum = sum(F_array)
        return F_sum


class Solution:
    def __init__(self, tasks=None):
        if tasks is None:
            tasks = []

        self.tasks = tasks
        self.harm = Harmonogram(3, tasks)
        self.criteria = [self.harm.makespan(), self.harm.total_flowtime()]



def swap_tasks(tasks, id1, id2):
    newtasks = copy.copy(tasks)
    newtasks[id1], newtasks[id2] = newtasks[id2], newtasks[id1]
    return newtasks


class FlowShop:
    def __init__(self, data):
        self.n = data["n"]
        self.machines = data["machines"]
        self.pij = data['pij']
        self.dj = data["dj"]

        # self.solution = Solution()
        # self.harmonogram = Harmonogram()
        self.P = []

        # rozwiązanie początkowe - x
        self.tasks = []
        for i in range(self.n):
            pj = []
            for j in range(self.machines):
                pj.append(self.pij[j][i])
            self.tasks.append(Task(pj, self.dj[i], i))
        shuffle(self.tasks)



    def solve(self, max_iter):

        ######################### 4 #########################

        self.P.append(self.tasks)

        ######################### 5 #########################

        for it in range(max_iter):
            x_prime = swap_tasks(self.tasks, random.randrange(self.n), random.randrange(self.n))

            ######################### 5.1 #########################
            # rozwiązanie początkowe losowane w inicjalizacji danej klasy

            ######################### 5.2 #########################
            # x_prime (nowe rozwiązanie) dominuje x (tasks - aktualne rozwiązanie) względem dobranych kryteriów

            if self.if_dominates(x_prime, self.tasks):
                self.tasks = x_prime
                self.P.append(x_prime)
                # print(x_prime[i].id for i in range(self.n))
            else:
                self.tasks = x_prime
                if random.random() <= 0.995 ** it:
                    # print(f"Prawdopodobienstwo: {0.995**i}, it: {i}")
                    self.P.append(x_prime)

        ######################### 6 #########################
        # wyznaczanie front Pareto
        ##################### 1 ####################
        F = copy.deepcopy(self.P)
        for it in range(len(self.P)):
            for j in range(len(self.P)):
                if j == it:
                    continue
                elif self.P[j] == self.P[it]:
                    continue
                else:
                    if self.if_dominates(self.P[j], self.P[it]):
                        F[:] = [sol for sol in F if sol != self.P[it]]
                        break

        # print(f"P:\n {self.P}")
        # print(f"Front Pareto: {F}")
        return F
        # print(np.unique(F))

    def if_dominates(self, solution1, solution2):
        """Check if solution1 dominates solution2"""
        h1 = Harmonogram(self.machines, solution1)
        h2 = Harmonogram(self.machines, solution2)
        if h1.makespan() <= h2.makespan() and h1.total_flowtime() <= h2.total_flowtime():
            if h1.makespan() < h2.makespan() or h1.total_flowtime() < h2.total_flowtime():
                return True
        return False

    # TODO: wyznaczanie losowego sąsiada - czy używać klasy Solution?
    # TODO: uproszczone SA