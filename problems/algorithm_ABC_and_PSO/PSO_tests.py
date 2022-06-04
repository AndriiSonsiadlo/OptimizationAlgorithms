from problems.algorithm_ABC_and_PSO.PSO_algorithm import ParticleSwarmOptimizer


def learning_factor_test(seed):
    print("\n", "-"*100)
    print(f"\nseed={seed}")
    base_c = 0.1
    for i in range(0, 11):
        c = base_c * i
        print(f"\nlearning factor c={round(c, 1)}:")
        pso = ParticleSwarmOptimizer(
            n=10,        # n zmiennych w funkcji
            k=500,      # liczba cząstek
            w=0.25,     # parametr algorytmu
            fl=0.3,     # parametr algorytmu
            fg=0.45,    # parametr algorytmu
            c=c,        # tempo uczenia
            iterations=1000,
            seed=seed
        )
        result = pso.optimize()
        print(round(pso.goal_func(result), 2))


if __name__ == '__main__':
    # print("\n# Instance 1:")
    # pso1 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=0.25,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso1.optimize()
    #
    # print("\n# Instance 2:")
    # pso2 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=1000,
    #     w=0.25,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso2.optimize()
    #
    # print("\n# Instance 3:")
    # pso3 = ParticleSwarmOptimizer(
    #     n=7,
    #     k=1000,
    #     w=0.25,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso3.optimize()
    #
    # print("\n# Instance 4:")
    # pso4 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=0.25,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.1,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso4.optimize()
    #
    # print("\n# Instance 5:")
    # pso5 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=0.25,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.9,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso5.optimize()
    #
    # print("\n# Instance 6:")
    # pso6 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=0.9,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso6.optimize()
    #
    # print("\n# Instance 7:")
    # pso7 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=1.1,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso7.optimize()
    #
    # print("\n# Instance 8:")
    # pso8 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=0.25,
    #     fl=5,
    #     fg=10,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso8.optimize()
    #
    # print("\n# Instance 9:")
    # pso9 = ParticleSwarmOptimizer(
    #     n=3,
    #     k=500,
    #     w=0.25,
    #     fl=10,
    #     fg=5,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso9.optimize()
    #
    # print("\n# Instance 10:")
    # pso10 = ParticleSwarmOptimizer(
    #     n=20,
    #     k=500,
    #     w=0.25,
    #     fl=0.3,
    #     fg=0.45,
    #     c=0.5,
    #     iterations=1000,
    #     seed=12345
    # )
    # pso10.optimize()

    learning_factor_test(seed=12345)
    # learning_factor_test(seed=67890)
    # learning_factor_test(seed=2142037)
