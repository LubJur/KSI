def fib_medzi(od, do):
    a, b = 0, 1
    while a <= do:
        if a >= od:
            print(a, end=", ")
        a, b = b, a+b
    print()

fib_medzi(10, 100)
fib_medzi(1000, 3000)