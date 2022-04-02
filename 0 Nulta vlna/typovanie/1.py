pairing = {(1, "test"), (2, "foo")}
val = "test"
def mul_two(val, pairing):
    return 2 * pairing[val]

print(mul_two(val, pairing))