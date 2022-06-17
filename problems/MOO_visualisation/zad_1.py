import numpy as np
import xlsxwriter as xlsxwriter

import classes
import statistics


def HVI(z, xf, yf):
    hvi = 0
    points = [[xf[i], yf[i]] for i in range(len(xf))]
    points = sorted(points, key=lambda x: x[0])

    lst = abs(z[0] - points[-1][0]) * abs(z[1] - points[-1][1])

    for i in range(len(points) - 1):
        hvi += abs(points[i][0] - points[i + 1][0]) * abs(points[i][1] - z[1])

    hvi += lst

    return hvi


def test_hvi():
    n = 50
    seeds = [1234, 4567, 9876, 3456, 7777]
    machines = 3
    # data = generate_data(seed, n, machines)
    maxIter = [100, 200, 400, 800, 1600]

    hvi = [[] for i in range(len(maxIter))]
    hvi_res = []

    #print((hvi))

    ZZZ1 = []
    ZZZ2 = []

    for i in range(10):



        z1 = 0
        z2 = 0
        xf_res = []
        yf_res = []
        for j in range(len(maxIter)):
            data = classes.generate_data(45687, n, machines)
            fs = classes.FlowShop(data)
            F = fs.solve(maxIter[j])
            xf = []
            yf = []
            for f in F:
                sol = classes.Solution(f)
                xf.append(sol.criteria[0])
                yf.append(sol.criteria[1])
                if sol.criteria[0] > z1:
                    z1 = 1.0 * sol.criteria[0]
                if sol.criteria[1] > z2:
                    z2 = 1.0 * sol.criteria[1]
            xf_res.append(xf)
            yf_res.append(yf)
            # print(xf)
            # print(yf)
        for xf, yf, j in zip(xf_res, yf_res, range(len(maxIter))):
            hvi[j].append(HVI([z1, z2], xf, yf))
            if j == 0:
                ZZZ1.append(z1)
                ZZZ2.append(z2)
        # print(hvi)
        print("Done ", i, " reps")

    # print(hvi[0])
    # print(statistics.mean(hvi[0]))
    for j in range(len(maxIter)):
        hvi_res.append(statistics.mean(hvi[j]))

    print("Z:", f"{statistics.mean(ZZZ1), statistics.mean(ZZZ2)}")

    print("$" * 25)
    print("HVI FOR ITERS:", maxIter)
    print(hvi_res)


# pierwsze badanie -> badania wartości maxIter
def test_maxIter():
    n = 50
    seeds = [1234, 4567, 9876, 3456, 7777]
    machines = 3
    # data = generate_data(seed, n, machines)
    maxIter = [100, 200, 400, 800, 1600]

    xp_res = []
    yp_res = []
    xf_res = []
    yf_res = []
    xp_fin = []
    yp_fin = []
    xf_fin = []
    yf_fin = []


    workbook = xlsxwriter.Workbook('export_data/zto_zad1_2.xlsx')

    for mi in maxIter:
        worksheet = workbook.add_worksheet(name=f"{mi}")

        data = classes.generate_data(45687, n, machines)
        fs = classes.FlowShop(data)
        F = fs.solve(mi)
        P = fs.P

        print("MaxIter:", mi)
        #print("F:", np.array(F))

        #print("P:", P)

        xf = []
        yf = []
        xp = []
        yp = []
        for p in P:
            sol = classes.Solution(p)
            xp.append(sol.criteria[0])
            yp.append(sol.criteria[1])
        xp_res.append(xp)
        yp_res.append(yp)
        for f in F:
            sol = classes.Solution(f)
            xf.append(sol.criteria[0])
            yf.append(sol.criteria[1])
        xf_res.append(xf)
        yf_res.append(yf)



        print(len(F))
        print("xf\n", np.array(xf))
        print("yf\n", np.array(yf))


        # Write to excel
        for row_num, (x, y) in enumerate(zip(xf, yf)):
            worksheet.write(row_num, 0, x+1)
            worksheet.write(row_num, 1, y+1)

        for row_num, (x, y) in enumerate(zip(xp, yp)):
            worksheet.write(row_num, 3, x+1)
            worksheet.write(row_num, 4, y+1)


        # Write to file
        with open("F" + str(mi) + ".txt", "w+") as file:
            for x, y in zip(xf, yf):
                file.write(f"{x}, {y}\n")

        with open("P" + str(mi) + ".txt", "w+") as file:
            for x, y in zip(xp, yp):
                file.write(f"{x}, {y}\n")

    workbook.close()






    # df = pd.DataFrame(xf_res)
    # df = df.transpose()
    # xlsfile = 'pandas_simple.xlsx'
    # writer = pd.ExcelWriter(xlsfile, engine='xlsxwriter')
    # df.to_excel(writer, sheet_name="Sheet1Name", startrow=1, startcol=1, header=False, index=False)
    #workbook = load_workbook(filename="zto.xlsx")


def main():
    n = 10
    seed = 123
    machines = 3
    data = classes.generate_data(seed, n, machines)

    # FlowShop -> zawiera rozwiązanie początkowe, zbiór P, i wyliczany jest front Pareto
    fs = classes.FlowShop(data)
    F = fs.solve(50)
    P = fs.P

    print(f"P:\n{P}")
    print(f"Front Pareto:\n{F}")

    xf = []
    yf = []
    xp = []
    yp = []

    for p in P:
        sol = classes.Solution(p)
        xp.append(sol.criteria[0])
        yp.append(sol.criteria[1])

    for f in F:
        sol = classes.Solution(f)
        xf.append(sol.criteria[0])
        yf.append(sol.criteria[1])

    test_maxIter()
    test_hvi()


if __name__ == "__main__":
    main()
