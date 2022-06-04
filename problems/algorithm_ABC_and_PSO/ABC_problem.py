import numpy as np
from pandas import DataFrame

from generator import RandomNumberGenerator

"""
Kwadratowe zagadnienie przydziału 
(Quadratic Assignment Problem, QAP)
"""

class Problem:
    """ Scheduling on a single machine with total weighted tardiness """

    @staticmethod
    def generate_data(seed, n, verbose=False):
        gen = RandomNumberGenerator(seedValue=seed)

        w_range = (1, 50)
        d_range = (1, 50)

        w = np.zeros(shape=(n, n), dtype=np.int32)
        d = w.copy()

        for i in range(n):
            for j in range(n):
                w[i][j], d[i][j] = (gen.nextInt(*w_range), gen.nextInt(*d_range)) if i != j else (0, 0)

        if verbose:
            cols = list(range(1, n + 1))

            print(f"w:")
            print(DataFrame(data=w, columns=cols, index=cols))
            print()
            print(f"d:")
            print(DataFrame(data=d, columns=cols, index=cols))

        #            print(f"w: \n{w}", end="\n\n")
        #           print(f"d: \n{d}", end="\n\n")



        data = {
            'n': n,
            'w': w,
            'd': d
        }

        return data


if __name__ == '__main__':
    Problem.generate_data(126, 5, True)
