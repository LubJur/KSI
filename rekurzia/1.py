# Tuto funkci implementuj.

def penguins_in_group(total: int, group_size: int) -> int:
    groups = 0
    if group_size == 0:
        return 0
    while total > group_size:
        total = total - group_size
        groups += 1
    return groups


"""
1. whats the simplest possible input?
2. play around with examples and visualize
3. relate hard cases to simple cases
4. generalize the pattern
5. write code by combining recursive pattern with the base case
"""

# def penguins_in_group(total: int, group_size: int) -> int:
#     if total <= group_size or group_size == 0:
#         return total
#     else:
#         return = total - penguins_in_group(total-group_size, group_size)


# Testy:
print("Máme 20 tučniakov, potrebujeme 5 tímov, v jednom tíme bude musieť byť ", penguins_in_group(20, 5))  # 4
print(penguins_in_group(393, 4))  # 98
print(penguins_in_group(1, 1))
