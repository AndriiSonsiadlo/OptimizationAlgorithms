from docplex.mp.model import Model

from generator import RandomNumberGenerator
from timer import timeit

"""
Problem ciągły
Problem dwuplecakowy
"""


@timeit
def ConKnapsackProblem_gen(n, verbose):
    seed = 114
    gen = RandomNumberGenerator(seedValue=seed)

    n = n
    B: int
    c, w, v = [], [], []

    for i in range(n):
        c.append(gen.nextFloat(1, 10))
        w.append(gen.nextFloat(1, 10))
        v.append(gen.nextFloat(1, 10))

    B = gen.nextInt(n, 4 * n)

    if verbose:
        print("c: ", c)
        print("w: ", w)
        print("v: ", v)
        print("B: ", B)

    return c, w, v, B


def problem(c, w, v, B):
    m = Model(name='model')
    x = m.continuous_var_list(keys=len(c), lb=0, ub=1, name='x')
    y = m.continuous_var_list(keys=len(c), lb=0, ub=1, name='y')

    m.maximize(m.sum((x[i] + y[i]) * c[i] for i in range(len(c))))

    for i in range(len(c)):
        m.add_constraint(x[i] + y[i] <= 1)
        m.add_constraint(x[i] >= 0)
        m.add_constraint(x[i] <= 1)
        m.add_constraint(y[i] >= 0)
        m.add_constraint(y[i] <= 1)

    m.add_constraint(m.sum(x[i] * w[i] for i in range(len(c))) <= B)
    m.add_constraint(m.sum(y[i] * v[i] for i in range(len(c))) <= B)

    m.solve(log_output=True)
    m.print_solution()
    m.print_information()


if __name__ == '__main__':
    c, w, v, B = ConKnapsackProblem_gen(50, True)
    problem(c, w, v, B)
