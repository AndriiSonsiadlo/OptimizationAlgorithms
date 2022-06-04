from docplex.mp.model import Model

from generator import RandomNumberGenerator
from timer import timeit

"""
Problem dyskretny
Problem dwuplecakowy
"""


def DiscreteKnapsackProblem_gen(n, verbose):
    seed = 114
    gen = RandomNumberGenerator(seedValue=seed)

    B: int
    n = n

    c, w = [], []
    for i in range(1, n + 1):
        c.append(gen.nextInt(1, 30))
        w.append(gen.nextInt(1, 30))

    B = gen.nextInt(5 * n, 10 * n)

    if verbose:
        print("c: ", c)
        print("w: ", w)
        print("B: ", B)

    return c, w, B


@timeit
def problem(c, w, B):
    m = Model(name='model')
    x = m.binary_var_list(keys=len(c), name='x')

    m.maximize(m.sum(x[i] * c[i] for i in range(len(c))))
    m.add_constraint(m.sum(x[i] * w[i] for i in range(len(c))) <= B)

    m.solve(log_output=True)
    m.print_solution()
    m.print_information()


if __name__ == '__main__':
    c, w, B = DiscreteKnapsackProblem_gen(1000, True)
    B = round(B / 5)
    problem(c, w, B)
