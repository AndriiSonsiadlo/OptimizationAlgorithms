from tqdm import tqdm

from generator import RandomNumberGenerator

"""
Sphere function 
"""


class ParticleSwarmOptimizer:
    def __init__(self, n, k, w, fl, fg, c, iterations, seed):
        self.iterations = iterations
        self.gen_spfr = RandomNumberGenerator(seed)
        self.n = n  # liczba zmiennych
        self.k = k  # liczba cząstek
        self.w = w  # parametr algorytmu
        self.fl = fl  # parametr algorytmu
        self.fg = fg  # parametr algorytmu
        self.c = c  # tempo uczenia
        self.l, self.u = self.get_l_and_u()
        self.best_locals = []  # l
        self.best_global = None  # g
        self.x = []  # wektor rozwiązania
        self.v = []  # velocity

    def optimize(self):

        self.generate_initial_swarm()

        for iteration in tqdm(range(self.iterations)):
            for j in range(self.k):
                for i in range(self.n):
                    rl = self.gen_spfr.nextFloat(0, 1)
                    rg = self.gen_spfr.nextFloat(0, 1)
                    self.v[j][i] = (
                            self.w * self.v[j][i]
                            + self.fl * rl * (self.best_locals[j][i] - self.x[j][i])
                            + self.fg * rg * (self.best_global[i] - self.x[j][i])
                    )
                    self.x[j][i] = self.x[j][i] + self.c * self.v[j][i]
                if self.goal_func(self.x[j]) < self.goal_func(self.best_locals[j]):
                    self.best_locals[j] = self.x[j]
                    if self.goal_func(self.best_locals[j]) < self.goal_func(self.best_global):
                        print(f"iter: {j}, {self.goal_func(self.best_global), self.best_global}")
                        self.best_global = self.best_locals[j]

        pretty_solution = [round(val, 3) for val in self.best_global]
        print(f"Solution: {pretty_solution}")
        return self.best_global

    def generate_initial_swarm(self):
        self.x.append(self.get_position())  # (l, u)
        self.best_locals.append(self.x[0])  # best_local_sol = pierwszy wylosowany wektor
        self.best_global = self.x[0]  # best_global_sol = pierwszy wylosowany wektor
        self.v.append(self.get_velocity())


        for j in range(1, self.k):
            self.x.append(self.get_position())
            self.best_locals.append(self.x[j])
            if self.goal_func(self.x[j]) < self.goal_func(self.best_global):
                self.best_global = self.x[j]
                print(f"iter: {j}, {self.goal_func(self.best_global), self.best_global}")

            self.v.append(self.get_velocity())

    def get_l_and_u(self):
        l, u = [], []
        for i in range(self.n):
            floats = [self.gen_spfr.nextFloat(-100, 100), self.gen_spfr.nextFloat(-100, 100)]
            while len(set(floats)) == 1:
                floats = [self.gen_spfr.nextFloat(-100, 100), self.gen_spfr.nextFloat(-100, 100)]
            l.append(min(floats))
            u.append(max(floats))
        return l, u

    def goal_func(self, x):

        # SPHERE

        i_sum = 0
        for i in range(self.n):
            i_val = pow(x[i], 2)
            i_sum += i_val
        return i_sum

    def get_position(self):
        # jednostajny rozkład prawdopodobieństwa
        vector = [self.gen_spfr.nextFloat(self.l[i], self.u[i]) for i in range(self.n)]
        return vector

    def get_velocity(self):
        velocity = [self.gen_spfr.nextFloat(self.l[i] - self.u[i], self.u[i] - self.l[i]) for i in range(self.n)]
        return velocity
