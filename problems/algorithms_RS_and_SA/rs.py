from problem import Problem
from timer import Timer

from utils import Solution


class RandomSearch(Problem):

    def __init__(self, verbose=True):
        self.verbose = verbose

    # @timeit
    def solve(self, task_list, iterations, timeout_in_sec) -> Solution:
        solution = self.get_init_solution(task_list, iterations)
        temp_task_list = solution.task_order

        check_time = Timer().start()
        for _ in range(1, iterations + 1):
            delay = Problem.goal_function(temp_task_list)
            if solution.minimal_delay > delay:
                solution.task_order = task_list.copy()
                solution.minimal_delay = delay
                check_time.reset_time()

            # Print solution if timeout expired or iterations ended, else shuffle a task_list
            if check_time.get_time() > timeout_in_sec:
                if self.verbose:
                    print(solution)
                    print(f"Timeout expired: {round(check_time.stop())} sec")
                    print(f"Iterations: {_}")
                break
            elif _ == iterations:
                if self.verbose:
                    print(solution)
                    print(f"Iterations ended: {_}")
            else:
                temp_task_list.swap_random_elements()

        return solution

    @staticmethod
    def get_init_solution(task_list, iterations):
        solution = Solution()

        temp_task_order = task_list.copy()

        solution.task_order = temp_task_order.copy()
        solution.minimal_delay = Problem.goal_function(temp_task_order)

        for _ in range(iterations):
            temp_task_order.shuffle()
            delay = Problem.goal_function(temp_task_order)
            if delay <= solution.minimal_delay:
                solution.task_order = temp_task_order.copy()
                solution.minimal_delay = delay
        return solution