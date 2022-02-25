from typing import List

# Túto funkciu implementuj.
def find_substring_hash(hashes: List[int], x: int, m: int, begin: int, end: int) -> int:
    podr = end - begin
    print(podr)
    if podr == 0:
        return []
    else:
        return (hashes[end] - ((x ** podr) * hashes[begin])) % m

# Testy:
print(find_substring_hash([0, 11, 1119, 111909, 11190924], 100, 10**9 + 7, 0, 3))  # 111909 - hash "ksi" z retazca "ksix"
print(find_substring_hash([0, 11, 1119, 111909, 11190924], 100, 10**9 + 7, 1, 4))  # 190924 - hash "six" z retazca "ksix"
print(find_substring_hash([0, 11, 37302, 126491100, 931317116, 96318259, 615213998], 3391, 10**9 + 7, 3, 5))  # 40701 - hash "li" z retazca "karlik"
