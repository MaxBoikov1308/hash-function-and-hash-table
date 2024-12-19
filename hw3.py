from functools import reduce

def left_rotate(n: int, b: int) -> int:
    """Выполняет циклический сдвиг влево для 32-битного числа."""
    return ((n << b) | (n >> (32 - b))) & 0xFFFFFFFF

def genW(x: int) -> callable:
    # Создаём список для всех 80 значений
    W = [0] * 80

    # Инициализируем первые 16 слов
    for i in range(16):
        W[i] = (x >> (512 - (i + 1) * 32)) & 0xFFFFFFFF

    # Вычисляем оставшиеся 64 слова
    for i in range(16, 80):
        W[i] = left_rotate(W[i - 3] ^ W[i - 8] ^ W[i - 14] ^ W[i - 16], 1)

    # Создаём замыкание и возвращаем его
    def MakeGenerator(j: int) -> int:
        return W[j]

    return MakeGenerator

def padding(message: str):
    """Добавляет padding к сообщению для обработки."""
    original_byte_len = len(message)
    original_bit_len = original_byte_len * 8

    # Добавляем 1 бит и заполняем нулями до ближайшего 512-битного блока
    message += '\x80'
    while (len(message) * 8) % 512 != 448:
        message += '\x00'

    # Добавляем длину сообщения в битах как 64-битное число
    message += original_bit_len.to_bytes(8, 'big').decode('latin1')

    # Разбиваем сообщение на блоки по 512 бит (64 байта)
    for i in range(0, len(message), 64):
        yield int.from_bytes(message[i:i + 64].encode('latin1'), 'big')

def sha1(message: str) -> str:
    # Стандартные значия для инициализации алгоритма (H[0])
    H = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]

    # Используем генератор для выдачи x[i]
    for x in padding(message):
        # Создаём замыкание для выдачи W[j]
        W = genW(x)

        # Инициализируем временные переменные
        A, B, C, D, E = H

        # Проходим все 80 раундов
        for i in range(80):
            if 0 <= i <= 19:
                F = (B & C) | (~B & D)
                K = 0x5A827999
            elif 20 <= i <= 39:
                F = B ^ C ^ D
                K = 0x6ED9EBA1
            elif 40 <= i <= 59:
                F = (B & C) | (B & D) | (C & D)
                K = 0x8F1BBCDC
            else:
                F = B ^ C ^ D
                K = 0xCA62C1D6

            # Основное уравнение
            TEMP = (left_rotate(A, 5) + F + E + K + W(i)) & 0xFFFFFFFF
            E = D
            D = C
            C = left_rotate(B, 30)
            B = A
            A = TEMP

        # Суммируем результирующие значения A, B, C, D, E с исходными
        H = [
            (H[0] + A) & 0xFFFFFFFF,
            (H[1] + B) & 0xFFFFFFFF,
            (H[2] + C) & 0xFFFFFFFF,
            (H[3] + D) & 0xFFFFFFFF,
            (H[4] + E) & 0xFFFFFFFF,
        ]

    # Выводим результат в шестнадцатеричном виде
    return makeHashStr(H)

def makeHashStr(H: list) -> str:
    res = hex(reduce(lambda a, b: (a << 32) | b, H, 0))[2:]
    return res if len(res) == 40 else '0' * (40 - len(res)) + res

# Пример использования
message = "hello world!"
print(sha1(message))
