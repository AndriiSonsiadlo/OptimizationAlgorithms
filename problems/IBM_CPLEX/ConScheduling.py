import numpy as np
from docplex.mp.model import Model

from generator import RandomNumberGenerator
from timer import timeit

"""
Problem ciągły
Problem szeregowania na równoległych maszynach
"""

def ConScheduling_gen(seed, n, m, verbose=False):
    gen = RandomNumberGenerator(seedValue=seed)

    p_range = (1, 20)
    a_range = (1, m)
    S_range = (m, 2 * m)

    p = np.zeros(shape=(n), dtype=np.float32)
    a = np.zeros(shape=(n), dtype=np.int32)
    S: float

    for i in range(n):
        p[i] = gen.nextFloat(*p_range)
        a[i] = gen.nextInt(*a_range)

    S = gen.nextFloat(*S_range)

    if verbose:
        print(f"{'*' * 20} Generowanie instancji {'*' * 20}", end="\n\n")

        print(f"p: \n{p}", end="\n\n")
        print(f"a: \n{a}", end="\n\n")
        print(f"S: \n{S}", end=f"\n\n")

    return p, a, S


@timeit
def problem(p, a, S, m, n, verbose=False):
    # Niewykorzystane maszyny w probleme, dla nich szybkość 0 ustawia się

    unused_machines = np.arange(1, m + 1)
    unused_machines = list(set(unused_machines) - set(a))

    if verbose:
        print(f"{'*' * 25} Solution {'*' * 25}\n\n")

        print("Unused machines: ", unused_machines, end="\n") if unused_machines else print("All machines are used",
                                                                                            end="\n")
        print("Used machines"
              ": ", sorted(list(set(a) - set(unused_machines))), end="\n\n")

    # Inicjowanie modelu i zmiennych CPLEX

    model = Model(name='model')
    s = model.continuous_var_list(keys=m, name='s')

    # Problem

    model.minimize(model.max(p[i] * s[a[i] - 1] for i in range(n)))

    # Ograniczenia

    for i in range(1, m):
        if i not in unused_machines:
            model.add_constraint(s[i - 1] >= 0.0001)
        else:
            model.add_constraint(s[i - 1] == 0)

    model.add_constraint(model.sum(s[i] for i in range(m)) == S)

    # Rozwiazanie i wyniki problemu

    model.solve(log_output=True)
    model.print_solution()
    model.print_information()


if __name__ == '__main__':
    n = 50
    m = 5

    p, a, S = ConScheduling_gen(seed=114, n=n, m=m, verbose=True)
    problem(p, a, S, m, n, verbose=True)
