from pandas import DataFrame
from tqdm import tqdm

from problem import Problem
from rs import RandomSearch
from sa import SimulatedAnnealing
from timer import *

"""
Szeregowanie zadań na jednej maszynie z ważoną sumą opóźnień
(Scheduling on a single machine with total weighted tardiness)
"""


def test_iter_value(seed, iterations_list: list, n: int, timeout_in_sec: int, epoch_length: int = 10, verbose=True):
    ls = Problem.generate(n, seed, verbose)

    # Random Search
    print("=" * 11, "Random Search", "=" * 11)

    solutions_rs = []
    rs = RandomSearch(verbose)
    timer = Timer().start()
    for iterations in tqdm(iterations_list):
        solution_rs = rs.solve(ls, iterations, timeout_in_sec)
        solution_rs.n = n
        solution_rs.iterations = iterations
        solution_rs.time = timer.stop()
        solutions_rs.append(solution_rs)

    # Simulated Annealing
    print("=" * 8, "Simulated Annealing", "=" * 8)

    solutions_sa = []
    sa = SimulatedAnnealing(verbose)
    timer = Timer().start()
    for iterations in tqdm(iterations_list):
        solution_sa = sa.solve(ls, iterations, timeout_in_sec, epoch_length)
        solution_sa.n = n
        solution_sa.iterations = iterations
        solution_sa.time = timer.stop()
        solutions_sa.append(solution_sa)

    print(solutions_to_str(solutions_rs, "RS"))
    print(solutions_to_str(solutions_sa, "SA"))


def test_n_time(seed, n_list: list, iterations: int, timeout_in_sec: int, epoch_length: int = 10, verbose=True):
    # Random Search
    print("=" * 11, "Random Search", "=" * 11)

    solutions_rs = []
    rs = RandomSearch(verbose)
    timer = Timer().start()

    for n in tqdm(n_list):
        ls = Problem.generate(n, seed, verbose)
        solution_rs = rs.solve(ls, iterations, timeout_in_sec)
        solution_rs.n = n
        solution_rs.iterations = iterations
        solution_rs.time = timer.stop()
        solutions_rs.append(solution_rs)

    # Simulated Annealing
    print("=" * 8, "Simulated Annealing", "=" * 8)

    solutions_sa = []
    sa = SimulatedAnnealing(verbose)
    timer = Timer().start()

    for n in tqdm(n_list):
        ls = Problem.generate(n, seed, verbose)
        solution_sa = sa.solve(ls, iterations, timeout_in_sec, epoch_length)
        solution_sa.n = n
        solution_sa.iterations = iterations
        solution_sa.time = timer.stop()
        solutions_sa.append(solution_sa)

    print(solutions_to_str(solutions_rs, "RS"))
    print(solutions_to_str(solutions_sa, "SA"))


def solutions_to_str(solutions: list, algorithm="RS | SA"):
    start_banner = f"{'=' * 12} {algorithm} SOLUTION {'=' * 12}\n\n"

    # sol_str = ""
    # for solution in solutions:
    #     sol_str += f"{solution.n}\t{solution.iterations}\t{solution.minimal_delay}\t\t{solution.time}\n"

    sol = []
    for solution in solutions:
        sol.append([solution.n, solution.iterations, solution.minimal_delay, round(solution.time, 3)])

    sol = DataFrame(data=sol, columns=["n", "iterations", "minimal_cost", "time"],
                    index=["" for i in range(len(solutions))])

    solution_str = f"{start_banner}{sol}\n\n"
    return solution_str


def compare_RS_and_SA(iterations, n, timeout_in_sec, seed, verbose=True):
    solutions_rs = []
    rs = RandomSearch(verbose)
    ls = Problem.generate(n, seed, verbose)
    solution_rs = rs.solve(ls, iterations, timeout_in_sec)
    solution_rs.n = n
    solution_rs.iterations = iterations
    solutions_rs.append(solution_rs)

    print(solutions_to_str(solutions_rs, "RS"))

    solutions_sa = []
    sa = SimulatedAnnealing(verbose)
    ls = Problem.generate(n, seed, verbose)
    solution_sa = sa.solve(ls, iterations, timeout_in_sec)
    solution_sa.n = n
    solution_sa.iterations = iterations
    solutions_sa.append(solution_sa)

    print(solutions_to_str(solutions_sa, "SA"))


# compare_RS_and_SA(1000, 20, 60, 114, verbose=False)

if __name__ == '__main__':
    # INIT PARAMS
    verbose = False
    seed = 1144457
    timeout_in_sec = 60
    epoch_length = 10

    iterations_list = [1_000, 2_000, 3_000, 4_000, 5_000, 6_000, 7_000, 8_000, 9_000, 10_000]
    n = 30

    iterations = 5000
    n_list = [10, 20, 30, 40, 50, 60, 70, 80]

    # ls = Problem.generate(n, seed, True)

    compare_RS_and_SA(iterations, n, 30, 20, verbose)

    print("=" * 57)
    print("=" * 20, "test_iter_value", "=" * 20)
    print("=" * 57)

    test_iter_value(seed=seed, iterations_list=iterations_list, n=n, timeout_in_sec=timeout_in_sec,
                    epoch_length=epoch_length, verbose=verbose)

    print("=" * 57)
    print("=" * 22, "test_n_time", "=" * 22)
    print("=" * 57)

    test_n_time(seed=seed, n_list=n_list, iterations=iterations, timeout_in_sec=timeout_in_sec,
                epoch_length=epoch_length, verbose=verbose)
