from pprint import pp

# Класс хеш-таблицы
class HashTable:
    def __init__(self, size: int = 10, hash_func=None):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.hash_func = hash_func

    def insert(self, key: str):
        index = self.hash_func(key)
        if key not in self.table[index]:
            self.table[index].append(key)

    def __contains__(self, key: str) -> bool:
        index = self.hash_func(key)
        return key in self.table[index]

    def __iter__(self):
        for chain in self.table:
            yield len(chain)


# Хеш-функция
HT_LEN = 15

def get_hash(string: str) -> int:
    
    hash_value = 0
    for char in string:
        hash_value = (hash_value * 31 + ord(char)) % HT_LEN
    return hash_value

# Функция генерации строки длины m
def get_str(m):
    return "".join([chr(i + 97 * (m - 1)) for i in range(m)])

if __name__ == "__main__":
    hash_table = HashTable(size=HT_LEN, hash_func=get_hash)

    for chain_length in hash_table:
        print(chain_length)

    # pp(hash_table.table)
