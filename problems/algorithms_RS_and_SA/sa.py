import random
from math import e

from problem import Problem
from timer import Timer
from utils import Solution, TaskList


class SimulatedAnnealing(Problem):

    def __init__(self, verbose=True):
        self.verbose = verbose

    # # @timeit
    def solve(self, task_list, iterations, timeout_in_sec, epoch_length=10) -> Solution:

        n = len(task_list)
        temp_modifier = 0.9999
        lowest_temp_modifier = 0.95
        epoch_count = int(iterations / epoch_length)

        solution, initial_temperature = self.get_init_solution(task_list, iterations)
        # new_task_order = solution.task_order.copy()
        temperature = temp_modifier * initial_temperature
        cooling_step = (temp_modifier - lowest_temp_modifier) / epoch_count

        if self.verbose:
            print(f"\n\nInitial Solution: {solution}")
            print(f"Goal function value (minimal delay): {solution.minimal_delay}")

        check_time = Timer().start()
        for i in range(1, iterations + 1):
            if i % epoch_length == 0 and i != 0:
                temp_modifier -= cooling_step
                temperature = temp_modifier * initial_temperature

            new_task_order = TaskList.swap_elements(solution.task_order, random.randint(1, n), random.randint(1, n))
            delay = self.goal_function(new_task_order)
            test_passed = self.acceptance_test(solution.minimal_delay, delay, temperature)

            # print("Temperature:", temperature)
            # print("Value:", delay)
            # print("Probability test passed:", test_passed)

            if (solution.minimal_delay > delay) or test_passed:
                solution.task_order = new_task_order.copy()
                solution.minimal_delay = delay
                check_time.reset_time()
                # print("New best value:", solution.minimal_delay)

            solution.task_order.sort()
            if check_time.get_time() > timeout_in_sec:
                if self.verbose:
                    print(solution)
                    print(f"Timeout expired: {round(check_time.stop())} sec")
                    print(f"Iterations: {i}")
                break
            elif i == iterations:
                if self.verbose:
                    print(solution)
                    print(f"Iterations ended: {i}")

        return solution

    @staticmethod
    def get_init_solution(task_list, iterations):
        solution = Solution()

        temp_task_order = task_list.copy()
        solution.task_order = temp_task_order.copy()
        solution.minimal_delay = Problem.goal_function(solution.task_order)

        best_value = solution.minimal_delay
        worst_value = 0

        for _ in range(iterations):
            temp_task_order.shuffle()
            delay = Problem.goal_function(temp_task_order)
            if delay <= best_value:
                solution.task_order = temp_task_order.copy()
                solution.minimal_delay = best_value = delay
            elif delay > worst_value:
                worst_value = delay

        initial_temperature = abs(best_value - worst_value)

        return solution, initial_temperature

    @staticmethod
    def acceptance_test(old_value, new_value, temperature) -> bool:
        fp = e ** ((-(new_value - old_value)) / temperature)
        probability = 1 - fp
        # print("Probability:", probability)
        if probability > 0:
            return random.choices([True, False], weights=[probability * 10, fp])[0]
        else:
            return False
