from functools import reduce
from math import sqrt, sin
from random import randint

# Генератор псевдо случайных чисел через замыкание
def gen_prng(seed: int) -> callable:
    x = seed
    def prng() -> int:
        nonlocal x
        x = int(abs(sin(x) * 10000)) % 10
        return x
    return prng

# проверка генератора
def evaluate(my_prng: callable, tries: int) -> None:
    f = [0 for i in range(10)]

    # подсчёт сгенерированных цифр
    for i in range(tries):
        f[my_prng()] += 1

    # вычисление плотности
    density = [i * 100 for i in list(map(lambda x: (x / tries), f))]

    # вычисление среднеквадратичного отклонения через лямбда-функцию
    s = sqrt(reduce(lambda x, y: x + (y - 10) ** 2, density, 0) / 10)

    print(f"Результат: {f}")
    print(f"Плотность: {density}")
    print(f"Среднеквадратичное отклонение: {s}")

    # вычисление длины периода через цикл
    seen = set()
    while True:
        val = my_prng()
        if val in seen:
            break
        seen.add(val)

    print(f"Длина периода: {len(seen)}")


my_prng = gen_prng(1)

evaluate(my_prng, 4000)

# сравнение с библиотекой random
print("".join(map(str, [my_prng() for i in range(10)])))
print("".join(map(str, [randint(0, 9) for i in range(10)])))