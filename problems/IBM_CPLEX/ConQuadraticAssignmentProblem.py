import numpy as np
from docplex.mp.model import Model

from generator import RandomNumberGenerator
from timer import timeit

"""
Problem ciągły
Kwadratowe zagadnienie przydziału
"""


def ConQuadraticAssignmentProblem_gen(seed, n, verbose=False):
    gen = RandomNumberGenerator(seedValue=seed)

    a_range = (5, 35)
    b_range = (5, 35)
    r_range = (1, 7)
    f_range = (1, 20)

    a = np.zeros(shape=(n), dtype=np.float32)
    b = a.copy()
    r = a.copy()
    f = np.zeros(shape=(n, n), dtype=np.float32)

    for i in range(n):
        a[i] = gen.nextFloat(*a_range)
        b[i] = gen.nextFloat(*b_range)
        r[i] = gen.nextFloat(*r_range)

        for j in range(n):
            f[i][j] = gen.nextFloat(*f_range) if i != j else 0

    if verbose:
        print(f"a: \n{a}", end="\n\n")
        print(f"b: \n{b}", end="\n\n")
        print(f"r: \n{r}", end="\n\n")
        print(f"f: \n{f}", end="\n\n")

    return a, b, r, f, n


@timeit
def problem(a, b, r, f, n):
    m = Model(name='model')

    x = m.continuous_var_list(keys=n, name='x')
    y = m.continuous_var_list(keys=n, name='y')

    m.minimize(
        m.sum(f[i][j] * m.sum([m.abs(x[ind] - y[ind]) for ind in range(n)]) for i in range(n) for j in range(i, n)))

    for i in range(n):
        m.add_constraint((x[i] - a[i]) ** 2 + (y[i] - b[i]) ** 2 <= r[i] ** 2)

    m.solve(log_output=True)
    m.print_solution()
    m.print_information()


if __name__ == '__main__':
    a, b, r, f, n = ConQuadraticAssignmentProblem_gen(seed=114, n=5, verbose=True)
    problem(a, b, r, f, n)
