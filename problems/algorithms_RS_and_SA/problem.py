from abc import abstractmethod

import numpy as np

from generator import RandomNumberGenerator
from utils import TaskList, Task, Solution


"""
Szeregowanie zadań na jednej maszynie z ważoną sumą opóźnień
(Scheduling on a single machine with total weighted tardiness)
"""



class Problem:
    """ Scheduling on a single machine with total weighted tardiness """

    @staticmethod
    def generate(n, seed, verbose=False):
        gen = RandomNumberGenerator(seedValue=seed)

        # generate p-list
        p_range = (1, 30)
        p = [gen.nextInt(*p_range) for _ in range(n)]

        # generate w-list
        w_range = (1, 30)
        w = [gen.nextInt(*w_range) for _ in range(n)]

        S = np.sum(p)

        # generate d-list
        d_range = (1, S)
        d = [gen.nextInt(*d_range) for _ in range(n)]

        _task_list = TaskList()
        for i, (p_i, w_i, d_i) in enumerate(zip(p, w, d), start=1):
            _task_list.append(Task(i, p_i, w_i, d_i, i))

        if verbose:
            print(f'\n{"=" * 12}', "GENERATED", "=" * 12, end="\n")
            print("n: ", n)
            print("S: ", S)
            print("task_list:")
            print(_task_list.to_df(), end="\n\n")
            print("=" * 35, end="\n\n")

        return _task_list.copy()

    @staticmethod
    def goal_function(task_list):
        n = len(task_list)

        p_pi_i = lambda pi_i, task_list: task_list[pi_i].p_i
        w_pi_i = lambda pi_i, task_list: task_list[pi_i].w_i
        d_pi_i = lambda pi_i, task_list: task_list[pi_i].d_i

        C_pi_i = lambda pi_i, task_list: p_pi_i(1, task_list) if pi_i == 1 else C_pi_i(pi_i - 1, task_list) + \
                                                                                p_pi_i(pi_i, task_list)
        T_pi_i = lambda pi_i, task_list: max(0, C_pi_i(pi_i, task_list) - d_pi_i(pi_i, task_list))

        delay = 0
        for i in range(1, n + 1):
            delay += w_pi_i(i, task_list) * T_pi_i(i, task_list)

        return delay

    @abstractmethod
    def solve(self, task_list, iterations, timeout_in_sec) -> Solution:
        pass
