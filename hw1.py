from functools import reduce
from math import sqrt
from random import randint

def gen_prng(seed):
    x = seed
    def prng():
        nonlocal x
        x = ((x * (x - 1)) + 12312 * (x + 1)) % 10
        return x
    return prng


def evaluate(my_prng, tries):
    f = [0 for i in range(10)]

    for i in range(tries):
        f[my_prng()] += 1

    density = [i * 100 for i in list(map(lambda x: (x / tries), f))]

    s = sqrt(reduce(lambda x, y: x + (y - 10) ** 2, density, 0) / 10)

    print(f"Результат: {f}")
    print(f"Плотность: {density}")
    print(f"Среднеквадратичное отклонение: {s}")

my_prng = gen_prng(1)
evaluate(my_prng, 4000)
