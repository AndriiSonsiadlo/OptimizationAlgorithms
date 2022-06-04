import random
import sys
from abc import ABC
from dataclasses import dataclass

import numpy as np
import pandas as pd


def indexing_decorator(func):
    def decorated(self, index, *args, **kwargs):
        if kwargs.get("value"):
            TaskList.check_value(kwargs["value"], Task)

        if index == 0:
            raise IndexError('Indices start from 1')
        elif index > 0:
            index -= 1
        elif index < 0:
            raise IndexError('Indices start from 1')
        return func(self, index, *args, **kwargs)

    return decorated


@dataclass(init=True, repr=True)
class Task(ABC):
    __variables = ["i", "p", "w", "d", "pi_i"]

    i: int
    p_i: int
    w_i: int
    d_i: int
    pi_i: int

    # """i"""
    #
    # @property
    # def i(self):
    #     pass
    #
    # @i.setter
    # def i(self, value):
    #     self._i = value
    #
    # @i.getter
    # def i(self):
    #     return self._i
    #
    # """p_i"""
    #
    # @property
    # def p_i(self):
    #     pass
    #
    # @p_i.setter
    # def p_i(self, value):
    #     self._p_i = value
    #
    # @p_i.getter
    # def p_i(self):
    #     return self._p_i
    #
    # """w_i"""
    #
    # @property
    # def w_i(self):
    #     pass
    #
    # @w_i.setter
    # def w_i(self, value):
    #     self._w_i = value
    #
    # @w_i.getter
    # def w_i(self):
    #     return self._w_i
    #
    # """d_i"""
    #
    # @property
    # def d_i(self):
    #     pass
    #
    # @d_i.setter
    # def d_i(self, value):
    #     self._d_i = value
    #
    # @d_i.getter
    # def d_i(self):
    #     return self._d_i
    #
    # """pi_i"""
    #
    # @property
    # def pi_i(self):
    #     pass
    #
    # @pi_i.setter
    # def pi_i(self, value):
    #     self._pi_i = value
    #
    # @pi_i.getter
    # def pi_i(self):
    #     return self._pi_i

    @staticmethod
    def variables():
        return Task.__variables

    # def __str__(self):
    #     return str(self.get())
    #
    # def __repr__(self):
    #     return str(self.get())

    def get(self):
        return (self.i, self.p_i, self.w_i, self.d_i, self.pi_i)

    def copy(self):
        return Task(self.i, self.p_i, self.w_i, self.d_i, self.pi_i)


class TaskList(list):

    @staticmethod
    def check_value(value, type=Task):
        if not isinstance(value, type):
            raise TypeError()

    def append(self, value):
        super(TaskList, self).append(value)

    @indexing_decorator
    def insert(self, index, value):
        super(TaskList, self).insert(index, value)

    def __getstate__(self):
        return super(TaskList, self)

    def __call__(self):
        return super(TaskList, self)

    @indexing_decorator
    def __getitem__(self, index):
        return super(TaskList, self).__getitem__(index)

    @indexing_decorator
    def __delitem__(self, index):
        super(TaskList, self).__delitem__(index)

    @indexing_decorator
    def __setitem__(self, index, value):
        super(TaskList, self).__setitem__(index, value)

    def __repr__(self):
        return super(TaskList, self).__repr__()

    def copy(self):
        temp_list = TaskList()
        for task in self:
            temp_list.append(task.copy())
        return temp_list

    def to_np(self):
        return np.array([task.get() for task in self])

    def to_df(self):
        columns = Task.variables()
        index = ["" for _ in range(len(self))]
        return pd.DataFrame(data=self.to_np(), columns=columns, index=index)

    def shuffle(self):
        shuffled_list = np.array(self.copy())
        np.random.shuffle(shuffled_list)
        self.clear()
        self.extend(shuffled_list)
        self.renumerate()

    def renumerate(self):
        for i, task in enumerate(self, start=1):
            task.pi_i = i

    @staticmethod
    def swap_elements(task_order, pos1: int, pos2: int):
        new_task_order = task_order.copy()
        new_task_order[pos1], new_task_order[pos2] = new_task_order[pos2], new_task_order[pos1]
        return new_task_order

    def swap_random_elements(self):
        pos1, pos2 = random.randint(1, len(self)), random.randint(1, len(self))
        self[pos1], self[pos2] = self[pos2], self[pos1]
        self.renumerate()

    def sort(self, **kwargs):
        for_sorted = self.copy()
        self.clear()
        self.extend(sorted(for_sorted, key=lambda x: x.pi_i))


@dataclass
class Solution:
    minimal_delay = sys.maxsize
    task_order: TaskList = None

    time = 0
    iterations = 0
    n = 0

    def __str__(self):
        start_banner = f"\n\n{'=' * 12} SOLUTION {'=' * 12}\n\n"
        end_banner = f"\n{'=' * 32}\n"

        task_order_str = f"Task order:\n{self.task_order.to_df()}\n"
        delay_str = f"Minimal delay: {self.minimal_delay}\n"

        solution = start_banner + task_order_str + delay_str + end_banner
        return solution
