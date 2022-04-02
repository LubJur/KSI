import timeit

def moduloFunction(val, length):
    return val % length


def knuthsFunction(val, length):
    return val*2654435761 % length


def shiftFunction(val, length):
    val = ((val >> 16) ^ val) * 0x45d9f3b
    val = ((val >> 16) ^ val) * 0x45d9f3b
    val = (val >> 16) ^ val
    return val % length


def evenShiftFunction(val, length):
    val *= 2
    val = ((val >> 16) ^ val) * 0x45d9f3b
    val = ((val >> 16) ^ val) * 0x45d9f3b
    val = (val >> 16) ^ val
    return val % length


def thomasWangsFunction(val, length):
    val += ~(val << 15)
    val ^= (val >> 10)
    val += (val << 3)
    val ^= (val >> 6)
    val += ~(val << 11)
    val ^= (val >> 16)
    return val % length


def anotherFunction(val, length):
    val *= 0x1eca7d79
    val ^= val >> 20
    val = (val << 8) | (val >> 24)
    val = ~val
    val ^= val << 5
    val += 0x10afe4e7
    return val % length

"""
functions - zoznam funkcii ktore chceme porovnat
test_data - zoznam hodnot na ktorych testujeme
n - velkost hashovacej tabulky

val - hodnota ku zahashovaniu
length - dlzka vystupu

vraciam index funkcie ktora je najlepsia
rozhodujem podla parametrov:
 - pocet kolizii
 - priemerny cas behu funkcie (pouzi kniznicu timeit)
 - smerodajna odchylka (dorob neskor)
 
na koniec to daj do grafov cez kniznicu plotly
"""


def std_deviation(ls):
    #ls = [i for i in ls if i is not None]
    for i in range(len(ls)):
        if ls[i] is None:
            ls[i] = 0
    n = len(ls)
    mean = sum(ls) / n
    var = sum((x - mean)**2 for x in ls) / n
    std_dev = var ** 0.5
    return std_dev


def load_data():
    data = []
    with open("test_data.txt", "r") as file:
        for line in file:
            data.append(int(line.split('","')[3]))
    return data

def choose_best_hash_function(functions, test_data, n):
    result = []
    # do whatever you want
    for f in functions:
        collisions = 0
        time = 0
        table = [None] * n
        print(f)
        for data in test_data:
            # https://stackoverflow.com/questions/31565762/local-variables-in-python-timeit-setup
            time += timeit.timeit(lambda: f(data, n))
            hashed = f(data, n)
            if table[hashed] is not None:
                collisions += 1
                continue
            table[hashed] = data
        #result.append(f(test_data[data], n))
        print(time, collisions, std_deviation(table))
    return len(result) - 1


choose_best_hash_function([moduloFunction, knuthsFunction,
                           shiftFunction, evenShiftFunction,
                           thomasWangsFunction, anotherFunction], load_data(), 1187)

#choose_best_hash_function([moduloFunction, knuthsFunction,
#                           shiftFunction, evenShiftFunction,
#                           thomasWangsFunction, anotherFunction], [383, 4782, 5837], 6)