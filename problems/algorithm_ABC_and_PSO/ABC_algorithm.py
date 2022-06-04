import random
from copy import copy

from utils import get_neighbour

"""
Kwadratowe zagadnienie przydziału 
(Quadratic Assignment Problem, QAP)
"""

class ArtificialBeeColony:
    def __init__(self, data: dict, population: int, iterations: int, limit: int, neighbourhood: str):
        self.n = data['n']
        self.weights = [[data['w'][i][j] for j in range(self.n)] for i in range(self.n)]
        self.distances = [[data['d'][i][j] for j in range(self.n)] for i in range(self.n)]
        self.population = population
        self.iterations = iterations
        self.limit = limit
        self.neighbourhood = neighbourhood
        self.solution = []
        self.best_val = 0

    def print_solution(self):
        print("#" * 30)
        print(
            f"Artificial Bee Colony, N: {self.n}, Population: {self.population}, Iterations: {self.iterations},\nLimit: {self.limit}, Neighbourhood type: {self.neighbourhood}")
        print(f"Solution: {self.solution}")
        print(f"Cost: {self.goal_func(self.solution)}")

    def roulette(self, solutions: list):

        # sum_val = np.sum([self.goal_func(sol) for sol in solutions])
        # roulette = np.array([ 1 - self.goal_func(sol) / sum_val for sol in solutions])

        roulette = []
        val = 0
        for sol in solutions:
            val += 1 / self.goal_func(sol)
            roulette.append(val)

        roulette = self.normalize(roulette.copy())

        return roulette

    def normalize(self, array):

        amin, amax = min(array), max(array)
        for i, val in enumerate(array):
            array[i] = (val - amin) / (amax - amin)

        return array

    def find_solution(self):
        c = dict()

        #############   1   #############

        x_1 = [i for i in range(1, self.n + 1)]
        random.shuffle(x_1)

        x_best = x_1.copy()
        best_val = self.goal_func(x_best)

        solutions = [x_1]
        c[1] = [0]

        #############   2   #############

        for i_for_c, i in enumerate(range(self.population), start=1):
            x_i = [i for i in range(1, self.n + 1)]
            random.shuffle(x_i)
            solutions.append(x_i)
            c[i_for_c] = 0

            if self.goal_func(x_i) < best_val:
                x_best = copy(x_i)  # x_best - aktualna najlepsza kolejność zakładów
                best_val = self.goal_func(x_i)  # best_val - aktualny najmniejszy (najlepszy) koszt
                print(best_val)  # goal_func - wzór problemu

        #############   3   #############

        for it in range(self.iterations):  # warunek końca

            #############   3.1   #############

            for i_for_c, i in enumerate(range(self.population), start=1):

                x_prime = get_neighbour(solutions[i],
                                        self.neighbourhood)  # generowanie losowego sąsiada, neighbourhood - metoda losowania
                val_prime = self.goal_func(x_prime)  # koszt dla wylosowanego sąsiada

                x_i_val = self.goal_func(solutions[i])  # koszt dla aktualnego wylosowanego rozwiązania

                if val_prime < x_i_val:
                    c[i_for_c] = 0
                    solutions[i] = x_prime
                else:
                    c[i_for_c] += 1

                if val_prime < best_val:
                    print(f"{val_prime}, iter: {it}")
                    x_best = copy(x_prime)
                    best_val = val_prime

            #############   3.2   #############

            probabilities = self.roulette(solutions)

            #############   3.3   #############

            for i_for_c, i in enumerate(range(self.population), start=1):

                ran = random.uniform(min(probabilities), max(probabilities))
                j = 0

                # sprawdzamy czy wylosowane praw-stwo jest w zakresie każdego rozwiązania.
                for l in range(len(probabilities)):
                    if ran < probabilities[
                        l]:  # jeśli tak - to wykonujemy to zadanie, jeśli nie, to sprawdzamy kolejne praw-stwo dla kolejnego zadania
                        j = l
                        break

                x_prime = get_neighbour(solutions[j], self.neighbourhood)
                prime_val = self.goal_func(x_prime)

                x_i_val = self.goal_func(solutions[i])

                if prime_val < x_i_val:
                    c[i_for_c] = 0
                    solutions[i] = x_prime
                else:
                    c[i_for_c] += 1

                if prime_val < best_val:
                    print(f"{prime_val}, iter: {it}")
                    x_best = copy(x_prime)
                    best_val = prime_val

            #############   3.4   #############

            for i_for_c, i in enumerate(range(self.population), start=1):
                if c[i_for_c] > self.limit:
                    c[i_for_c] = 0
                    random.shuffle(solutions[i])
                    x_i_val = self.goal_func(solutions[i])
                    if x_i_val < best_val:
                        print(f"{x_i_val}, iter: {it}")
                        x_best = copy(solutions[i])
                        best_val = x_i_val

        #############   4   #############

        self.solution = x_best
        self.best_val = best_val

        return x_best

    def goal_func(self, solution: list):
        val = 0
        for i in range(self.n):
            for j in range(self.n):
                val += self.weights[i][j] * self.distances[solution[i] - 1][solution[j] - 1]

        return val
