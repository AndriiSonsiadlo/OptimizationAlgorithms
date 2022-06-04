import random
from copy import copy


def get_neighbour(solution: list, option="swap"):
    n = len(solution)
    if option == "swap":  # zamienia dwie losowe liczby z listy
        return list_swap(random.randrange(n), random.randrange(n), solution)

    if option == "twist":  # zamienia losową liczbę i liczbę obok niej
        elem = random.randrange(n - 1)
        return list_twist(elem, solution)


def list_twist(elem, solution):
    return list_swap(elem, elem + 1, solution)


def list_swap(ind1, ind2, source):
    neighbour = copy(source)
    neighbour[ind1], neighbour[ind2] = neighbour[ind2], neighbour[ind1]
    return neighbour
