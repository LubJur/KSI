from typing import List

# Túto funkciu implementuj.
def compute_hashes(string: str, x: int, m: int) -> List[int]:
    alph = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    last = 0
    hashed = [last]
    for i in string:
        num = (last * x + (alph.index(i) + 1)) % m
        last = num
        hashed.append(num)
    return hashed

# Testy:
print(compute_hashes("ksix", 100, 10**9 + 7))  # [0, 11, 1119, 111909, 11190924]
print(compute_hashes("karlik", 3391, 10**9 + 7))  # [0, 11, 37302, 126491100, 931317116, 96318259, 615213998]
