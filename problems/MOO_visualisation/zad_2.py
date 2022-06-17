from math import floor
import random
from io import StringIO
import pandas as pd
import xlsxwriter

from generator import RandomNumberGenerator


class MachinesWithScalarization:
    def __init__(self, n, max_iter, seed, c_set, sw1, sw2, sw3):

        self.seed = seed
        self.max_iter = max_iter
        self.c_set = c_set
        self.n = n  # n zadań
        self.p_array = []  # czas wykonwynia zadania
        self.d_array = []  # deadline
        self.seed_weight_k1 = sw1
        self.seed_weight_k2 = sw2
        self.seed_weight_k3 = sw3
        self.generate_instance()
        self.task_order = self.get_initial_solution()  # pierwsze losowe rozwiązanie
        self.C_array = self.calculate_C()  # czas zakończenia
        self.best_solution = self.get_solution()

    def get_average_result(self):
        results = []
        for _ in range(10):
            self.find_optimal_solution()
            results.append(self.best_solution)
        average_result = round(sum(results) / 10, 3)
        with StringIO() as output:
            output.write("-" * 100)
            output.write(f"\nSeed = {self.seed}\n")
            output.write(f"Ilość zadań n = {self.n}\n")
            output.write(f"Ilość iteracji = {self.max_iter}\n")
            output.write(f"Zestaw {self.c_set} parametrów normalizacji kryteriów\n")
            output.write(f"Średnie s(x) = {average_result}\n")
            print(output.getvalue())
        return [
            self.seed,
            self.max_iter,
            self.c_set,
            average_result
        ]

    ###################### 4 ######################
    def find_optimal_solution(self):
        for _ in range(self.max_iter):
            self.random_swap(self.task_order)
            self.calculate_C()
            new_solution = self.get_solution()
            if new_solution < self.best_solution:
                self.best_solution = new_solution
            else:
                probability_test = random.randint(1, 10)
                if probability_test == 10:  # probability 10 %
                    self.best_solution = new_solution

    def random_swap(self, array):
        indexes = random.sample(range(0, self.n), 2)
        array[indexes[0]], array[indexes[1]] = array[indexes[1]], array[indexes[0]]

    def generate_instance(self):
        rng = RandomNumberGenerator(self.seed)
        A = 0
        for machine in range(3):
            p_for_machine = []
            for task in range(self.n):
                p = rng.nextInt(1, 99)
                p_for_machine.append(p)
                A += p
            self.p_array.append(p_for_machine)
        B = floor(A / 2)
        A = floor(A / 6)
        for task in range(self.n):
            self.d_array.append(
                rng.nextInt(A, B))  # [A, B] - zakres czasu w którym generuje się deadline dla każdego zadania

        print(self.p_array)
        print(self.d_array)

    def get_initial_solution(self):
        task_order = [j for j in range(self.n)]
        random.shuffle(task_order)
        return task_order

    def calculate_C(self):
        C_array = []
        for i in range(3):  # i - maszyna, wykonujemy na 3 maszynach
            C_for_machine = []  # j - zadanie
            for j in range(self.n):
                if j == 0 and i == 0:
                    C = self.p_array[i][self.task_order[j]]
                elif j > 0 and i == 0:
                    C = C_for_machine[i - 1] + self.p_array[i][self.task_order[j]]
                elif j == 0 and i > 0:
                    C = C_array[i - 1][j] + self.p_array[i][self.task_order[j]]
                elif j > 0 and i > 0:
                    C = max([C_array[i - 1][j], C_for_machine[j - 1]]) + self.p_array[i][self.task_order[j]]

                C_for_machine.append(C)
            C_array.append(C_for_machine)
        return C_array  # harmonogram C na podstawie kolejności π || dla każdej maszyny

    def makespan_value(self):  # 1 kryterium - Czas zakończenia wszystkich zadań
        C_max = max(self.C_array[2])
        return C_max

    def total_flowtime_value(self):  # 2 kryterium - Suma czasów zakończenia wszystkich zadań
        F_array = [self.C_array[2][j] for j in range(self.n)]
        F_sum = sum(F_array)
        return F_sum

    def total_tardiness_values(self):  # 4 kryterium - Suma spóźnień zadań
        T_array = [max([self.C_array[2][j] - self.d_array[self.task_order[j]], 0]) for j in range(self.n)]
        T_sum = sum(T_array)
        return T_sum

    def max_lateness_value(self):  # 5 kryterium - Maksymalna nieterminowość zadania
        L_max = max([self.C_array[2][j] - self.d_array[self.task_order[j]] for j in range(self.n)])
        return L_max

    def get_solution(self):
        k1 = self.makespan_value()
        k2 = self.total_flowtime_value()
        k3 = self.total_tardiness_values()

        c_sets = {
            1: (1.257, 1, 3.184),
            2: (1.2, 1, 3),
            3: (2, 1, 4)
        }
        c1 = c_sets[self.c_set][0]
        c2 = c_sets[self.c_set][1]
        c3 = c_sets[self.c_set][2]
        #solution = self.seed_weight_k1 * c1 * k1 + self.seed_weight_k2 * c2 * k2 + self.seed_weight_k3 * c3 * k3
        solution = c1 * k1 + c2 * k2 + c3 * k3
        return solution


def main():
    excel_data, to_excel = [], []
    # seed weight
    seeds = {
        1234: {
            "sw1": 1.03,
            "sw2": 2.01,
            "sw3": 1.29,
        },
        4567: {
            "sw1": 1,
            "sw2": 1,
            "sw3": 1,
        },
        9876: {
            "sw1": 1.16,
            "sw2": 2.26,
            "sw3": 1.41,
        },
        3456: {
            "sw1": 1.16,
            "sw2": 1.84,
            "sw3": 1.29,
        },
        7777: {
            "sw1": 1.06,
            "sw2": 1.84,
            "sw3": 1.23,
        },
    }
    iters = [100, 200, 400, 800, 1600]
    for c_set in [1, 2, 3]:  # machines
        for sd in seeds:
            for max_iter in iters:
                mws = MachinesWithScalarization(
                    n=25,
                    max_iter=max_iter,
                    seed=sd,
                    c_set=c_set,
                    sw1=seeds[sd]['sw1'],
                    sw2=seeds[sd]['sw2'],
                    sw3=seeds[sd]['sw3']
                )
                row = mws.get_average_result()
                excel_data.append(row)
            print(f"\n{'#' * 100}\n")
        print(f"\n\n{'@' * 100}\n\n")

    template = {
        1: {
            100: [],
            200: [],
            400: [],
            800: [],
            1600: [],
        },
        2: {
            100: [],
            200: [],
            400: [],
            800: [],
            1600: [],
        },
        3: {
            100: [],
            200: [],
            400: [],
            800: [],
            1600: [],
        },
    }

    for e_row in excel_data:
        template[e_row[2]][e_row[1]].append(e_row[3])

    for c_val in template:
        for it in template[c_val]:
            template[c_val][it] = round(sum(template[c_val][it]) / len(template[c_val][it]), 3)

    print(template)

    workbook = xlsxwriter.Workbook('export_data/zto_zad2_2.xlsx')
    worksheet = workbook.add_worksheet(name=f"zto")

    # Write to excel
    for col_var, (i_machine, i_data) in enumerate(template.items()):
        worksheet.write(0, 3*(i_machine-1), i_machine)
        for row_num, (iter, value) in enumerate(i_data.items(), start=1):
            worksheet.write(row_num, 3*(i_machine-1), iter)
            worksheet.write(row_num, 3*(i_machine-1) + 1, value)

    # for row_num, (iter, value) in enumerate(template[1].items()):
    #     worksheet.write(row_num + 1, 0, iter)
    #     worksheet.write(row_num + 1, 1, value)
    #
    # for row_num, (iter, value) in enumerate(template[2].items()):
    #     worksheet.write(row_num + 1, 3, iter)
    #     worksheet.write(row_num + 1, 4, value)
    #
    # for row_num, (iter, value) in enumerate(template[3].items()):
    #     worksheet.write(row_num + 1, 6, iter)
    #     worksheet.write(row_num + 1, 7, value)

    workbook.close()

    # for seed in seeds:
    #     table = [
    #         ["Max iters", "Zestaw c nr 1", "Zestaw c nr 2", "Zestaw c nr 3"]
    #     ]
    #     iter_rows = {it: [it] for it in iters}
    #     for row in excel_data:
    #         if row[0] == seed:
    #             iter_rows[row[1]].append(row[3])
    #     for table_row in iter_rows.values():
    #         table.append(list(table_row))
    #     table += ["", "", "", ""]
    #     to_excel += table
    #
    # df = pd.DataFrame(to_excel)
    # with pd.ExcelWriter("Dane_zad_2.xlsx", mode="w") as writer:
    #     df.to_excel(writer, index=False, header=False)


# def normalize():
#     seeds = [
#             1234,
#             4567,
#             9876,
#             3456,
#             7777,
#         ]
#     for seed in seeds:
#         mws = MachinesWithScalarization(
#             n=25,
#             max_iter=500,
#             seed=seed,
#             c_set=1,
#             sw1=[],
#             sw2=[],
#             sw3=[]
#         )
#         row = mws.get_average_result()


if __name__ == '__main__':
    main()
    # normalize()
