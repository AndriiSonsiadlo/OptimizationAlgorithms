import numpy as np
from pandas import DataFrame

from problems.algorithm_ABC_and_PSO.ABC_algorithm import ArtificialBeeColony
from problems.algorithm_ABC_and_PSO.ABC_problem import Problem
from timer import Timer


def test(option):
    print(f"test pop: {option}")
    n = 25
    seeds = [1234, 6753, 2345, 7852, 9081, 2341, 9999]
    iterations = 50
    populations = [i for i in range(50, 400, 50)]
    limit = 3
    option = option
    # data = generate_data(seed, n)
    # abc = ArtificialBeeColony(data, population, iterations, limit, option)
    # sol = abc.find_solution()
    # abc.print_solution()
    filename = "res1_" + option + ".txt"
    with open(filename, "w+") as file:
        for pop in populations:
            sum_solutions = 0
            for seed in seeds:
                data = Problem.generate_data(seed, n)
                abc = ArtificialBeeColony(data, pop, iterations, limit, option)
                sum_solutions += abc.goal_func(abc.find_solution())
            avg = round(sum_solutions / len(seeds))
            file.write(f"{pop}, {avg}\n")
            print(pop)


def test1(option):
    print(f"test iter {option}")
    n = 25
    seeds = [1234, 6753, 2345, 7852, 9081, 2341, 9999]
    iterations = [i for i in range(50, 350, 50)]
    population = 50
    limit = 3
    option = option
    # data = generate_data(seed, n)
    # abc = ArtificialBeeColony(data, population, iterations, limit, option)
    # sol = abc.find_solution()
    # abc.print_solution()
    filename = "iter_" + option + ".txt"
    with open(filename, "w+") as file:
        for it in iterations:
            sum_solutions = 0
            for seed in seeds:
                data = Problem.generate_data(seed, n)
                abc = ArtificialBeeColony(data, population, it, limit, option)
                sum_solutions += abc.goal_func(abc.find_solution())
            avg = round(sum_solutions / len(seeds))
            file.write(f"{it}, {avg}\n")
            print(it)


def test2(option):
    print(f"test n {option}")
    ns = [i for i in range(10, 60, 10)]
    seeds = [1234, 6753, 2345, 7852, 9081, 2341, 9999]
    iterations = 50
    population = 50
    limit = 3
    option = option
    # data = generate_data(seed, n)
    # abc = ArtificialBeeColony(data, population, iterations, limit, option)
    # sol = abc.find_solution()
    # abc.print_solution()
    filename = "n_" + option + ".txt"
    with open(filename, "w+") as file:
        for n in ns:
            sum_solutions = 0
            for seed in seeds:
                data = Problem.generate_data(seed, n)
                abc = ArtificialBeeColony(data, population, iterations, limit, option)
                sum_solutions += abc.goal_func(abc.find_solution())
            avg = round(sum_solutions / len(seeds))
            file.write(f"{n}, {avg}\n")
            print(n)


def test3(option):
    print(f"test limit {option}")
    n = 15
    seeds = [1234, 6753, 2345, 7852, 9081, 2341, 9999]
    iterations = 50
    population = 50
    limits = [i for i in range(1, 6)]
    option = option
    # data = generate_data(seed, n)
    # abc = ArtificialBeeColony(data, population, iterations, limit, option)
    # sol = abc.find_solution()
    # abc.print_solution()
    filename = "limit_" + option + ".txt"
    with open(filename, "w+") as file:
        for limit in limits:
            sum_solutions = 0
            for seed in seeds:
                data = Problem.generate_data(seed, n)
                abc = ArtificialBeeColony(data, population, iterations, limit, option)
                sum_solutions += abc.goal_func(abc.find_solution())
            avg = round(sum_solutions / len(seeds))
            file.write(f"{limit}, {avg}\n")
            print(limit)


def test4(option):
    timer = Timer()

    print(f"test limit {option}")
    n = 20
    seeds = [123456454]
    iterations = 50
    populations = [i for i in range(50, 550, 50)]
    limit = 5
    option = option
    # data = generate_data(seed, n)
    # abc = ArtificialBeeColony(data, population, iterations, limit, option)
    # sol = abc.find_solution()
    # abc.print_solution()

    filename = "time_population_" + option + ".txt"
    with open(filename, "w+") as file:
        for population in populations:
            timer.start()
            # sum_solutions = 0
            for seed in seeds:
                data = Problem.generate_data(seed, n)
                abc = ArtificialBeeColony(data, population, iterations, limit, option)
                abc.find_solution()
                # sum_solutions += abc.goal_func(abc.find_solution())
            # avg = round(sum_solutions / len(seeds))
            file.write(f"{population}, {timer.stop()}\n")


def test5(option):
    timer = Timer()

    print(f"test limit {option}")
    ns = [i for i in range(10, 70, 10)]
    seeds = [123456454]
    iterations = 300
    population = 100
    limit = 5
    option = option
    # data = generate_data(seed, n)
    # abc = ArtificialBeeColony(data, population, iterations, limit, option)
    # sol = abc.find_solution()
    # abc.print_solution()

    filename = "time_n_" + option + ".txt"
    with open(filename, "w+") as file:
        for n in ns:
            timer.start()
            # sum_solutions = 0
            for seed in seeds:
                data = Problem.generate_data(seed, n)
                abc = ArtificialBeeColony(data, population, iterations, limit, option)
                abc.find_solution()
                # sum_solutions += abc.goal_func(abc.find_solution())
            # avg = round(sum_solutions / len(seeds))
            file.write(f"{n}, {timer.stop()}\n")


# print(sol)
if __name__ == "__main__":
    n = 30
    seed = 456
    iterations = 2000
    population = 50
    limit = 50
    option = "swap"

    data = Problem.generate_data(seed, n, verbose=True)
    abc = ArtificialBeeColony(data, population, iterations, limit, option)
    sol = abc.find_solution()

    abc.print_solution()

    d_sol = np.zeros(shape=(n, n), dtype=np.int32)
    order = abc.solution
    for i in range(n):
        for j in range(n):
            d_sol[i][j] = data["d"][order[i] - 1][order[j] - 1]

    print(f"\nw:")
    print(DataFrame(data=data["w"], columns=list(range(1, n + 1)), index=list(range(1, n + 1))))
    print()
    print(f"d:")
    print(DataFrame(data=d_sol, index=order, columns=order))

    # # var cost (population)
    # test("swap")
    # test("twist")
    #
    # # var cost (iteration)
    # test1("swap")
    # test1("twist")
    #
    # # var cost (n)
    # test2("swap")
    # test2("twist")
    #
    # # var cost (limit)
    # test3("swap")
    # test3("twist")
    #
    # var time (population)
    # test4("swap")
    # test4("twist")

    # var time (n)
    # test5("swap")
    # test5("twist")
