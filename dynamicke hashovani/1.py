from typing import Callable, Optional, List

class CuckooHashTable:
    """Třída CuckooHashTable reprezentuje kukaččí hašovací tabulku.

    Atributy:
        array1  první pole
        array2  druhé pole
        hash1   hašovací funkce pro první pole
        hash2   hašovací funkce pro druhé pole

    Hašovací funkce voláme takto – je-li table objekt typu CuckooHashTable:
        table.hash1(key)
        table.hash2(key)

    Velikost polí musí během libovolných operací s tabulkou zůstat fixní.
    (Tj. chovejte se k nim skutečně jako k polím, ne jako k rozšiřitelným
     seznamům.)
    """
    __slots__ = "array1", "array2", "hash1", "hash2"

    def __init__(self, size: int,
                 hash1: Callable[[int], int],
                 hash2: Callable[[int], int]):
        self.array1: List[Optional[int]] = [None for _ in range(size)]
        self.array2: List[Optional[int]] = [None for _ in range(size)]
        self.hash1 = hash1
        self.hash2 = hash2


# Část 1.
# Implementuje predikát contains, který ověří, zda tabulka obsahuje zadaný
# klíč. Tabulku nijak nemodifikujte.

def contains(table: CuckooHashTable, key: int) -> bool:
    """
    vstup: ‹table› – korektní kukaččí hašovací tabulka
           ‹key› – celé číslo
    výstup: ‹True›, pokud tabulka ‹table› obsahuje klíč ‹key›
            ‹False› jinak
    očekávaná časová složitost: O(1), tedy konstantní
    """
    if key in table.array1 or key in table.array2:
        return True
    else:
        return False

# Část 2.
# Implementujte funkci delete, která ze zadané tabulky odstraní zadaný klíč.

def delete(table: CuckooHashTable, key: int) -> bool:
    """
    vstup: ‹table› – korektní kukaččí hašovací tabulka
           ‹key› – celé číslo
    výstup: ‹True›, pokud skutečně došlo k odstranění klíče
            ‹False› jinak
            Funkce z tabulky ‹table› odstraní klíč ‹key›, pokud jej
            tabulka obsahuje.
    očekávaná časová složitost: O(1), tedy konstantní
    """
    if key in table.array1:
        table.array1[table.array1.index(key)] = None
        return True
    elif key in table.array2:
        table.array2[table.array2.index(key)] = None
        return True
    else:
        return False


# Část 3.
# Implementujte funkci insert, která do tabulky vloží klíč.
# Pro návratovou hodnotu použijte následující konstanty (jejich hodnoty
# nijak neměňte):

ALREADY_PRESENT = 0
INSERT_SUCCESSFUL = 1
INSERT_FAILED = 2
origin_state_1 = []
origin_state_2 = []

def insert(table: CuckooHashTable, key: int, max_kicks: int) -> int:
    """
    vstup: ‹table› – korektní kukaččí hašovací tabulka
           ‹key› – celé číslo
           ‹max_kicks› – nezáporné celé číslo
           (Smíte předpokládat, že hodnota ‹max_kicks› je nižší než
            limit rekurze.)
    výstup: ‹ALREADY_PRESENT›, pokud tabulka ‹table› už klíč ‹key› obsahuje
            ‹INSERT_SUCCESSFUL›, pokud se vkládání podařilo
            ‹INSERT_FAILED›, pokud se vkládání nepodařilo
            Funkce se pokusí vložit klíč ‹key› do tabulky ‹table› dle
            postupu popsaného na začátku tohoto souboru.
            Parametr ‹max_kicks› označuje maximální počet „vykopnutí“,
            které smí funkce provést.
            V případě, že se vkládání nepodaří, je třeba tabulku uvést
            do původního stavu.
    očekávaná časová složitost: O(max_kicks)
    """
    global origin_state_1
    global origin_state_2
    origin_state_1 = list(table.array1)
    origin_state_2 = list(table.array2)

    if table.array1[table.hash1(key)] is None:
        table.array1[table.hash1(key)] = key
        return INSERT_SUCCESSFUL
    elif table.array2[table.hash2(key)] is None:
        table.array2[table.hash2(key)] = key
        return INSERT_SUCCESSFUL
    else:
        while max_kicks > 0:
            kicked = table.array1[h1(key)]
            table.array1[h1(key)] = key
            key = kicked
            max_kicks -= 1
            if table.array2[h2(key)] == None:
                table.array2[h2(key)] = key
                return INSERT_SUCCESSFUL
            else:
                kicked = table.array2[h2(key)]
                table.array2[h2(key)] = key
                key = kicked
                max_kicks -=1
                if table.array1[h1(key)] == None:
                    table.array1[h1(key)] = key
                    return INSERT_SUCCESSFUL
        table.array1 = origin_state_1
        table.array2 = origin_state_2
        return INSERT_FAILED

"""
            i=i+1

            print("skusam po", max_kicks, "vkladam", key)
            print("davam do pozicie", key % 5, "v tabulke", table.array1, "kluc", key)
            kicked = table.array1[table.hash1(key)]
            table.array1[table.hash1(key)] = key
            key = kicked
            print("skusam ci miesto", key // 5 % 5, "v tabulke", table.array2, "pre kluc", key, "je prazdne")
            if table.array2[table.hash2(key)] == None:
                table.array2[table.hash2(key)] = key
                print("SUCCESS")
                return INSERT_SUCCESSFUL
            else:
                print("davam do pozicie", key // 5 % 5, "v tabulke", table.array2, "kluc", key)
                kicked = table.array2[table.hash2(key)]
                table.array2[table.hash2(key)] = key
                key = kicked
                print("pred opakovanim vyzeraju tabulky, chcem vlozit", key)
                print(table.array1)
                print(table.array2)
                if table.array1[table.hash1(key)] == None:
                    table.array1[table.hash1(key)] = key
                    print("SUCCESS")
                    return INSERT_SUCCESSFUL
                if key == None:
                    return INSERT_SUCCESSFUL
                max_kicks -= 1
            print(i)
        table.array1 = origin_state_1
        table.array2 = origin_state_2
        saved = False
        print("FAIL")
        return INSERT_FAILED
"""
def h1(key: int) -> int:
    return key % 5

def h2(key: int) -> int:
    return key // 5 % 5

# základní testy, kterými by mělo zadání projít
def test() -> None:
    my_table = CuckooHashTable(5, h1, h2)
    assert insert(my_table, 10, 10) == INSERT_SUCCESSFUL
    assert my_table.array1 == [10, None, None, None, None]
    assert insert(my_table, 11, 10) == INSERT_SUCCESSFUL
    assert my_table.array1 == [10, 11, None, None, None]
    assert insert(my_table, 12, 10) == INSERT_SUCCESSFUL
    assert my_table.array1 == [10, 11, 12, None, None]
    assert insert(my_table, 20, 10) == INSERT_SUCCESSFUL
    assert my_table.array2 == [None, None, None, None, 20]

    table = CuckooHashTable(5, h1, h2)
    for key in 7, 22, 47, 5, 25:
        assert insert(table, key, 10) == INSERT_SUCCESSFUL

    assert table.array1 == [5, None, 47, None, None]
    assert table.array2 == [25, 7, None, None, 22]

    assert insert(table, 27, 100) == INSERT_FAILED

    assert table.array1 == [5, None, 47, None, None]
    assert table.array2 == [25, 7, None, None, 22]

    assert insert(table, 11, 0) == INSERT_SUCCESSFUL

    assert contains(table, 25)
    assert delete(table, 25)
    assert not contains(table, 25)

    assert table.array1 == [5, 11, 47, None, None]
    assert table.array2 == [None, 7, None, None, 22]

    assert insert(table, 76, 0) == INSERT_SUCCESSFUL
    assert insert(table, 25, 8) == INSERT_FAILED
    assert insert(table, 25, 9) == INSERT_SUCCESSFUL

    assert table.array1 == [5, 76, 22, None, None]
    assert table.array2 == [25, 7, 11, None, 47]


test()