import pyzipper
import string
import itertools

alphabet = list(string.ascii_lowercase)

combinations = itertools.product(alphabet, repeat=3)

with pyzipper.AESZipFile("staryarchiv.zip") as my_zip:
    for combination in combinations:
        combination = "".join(combination)
        print("Trying:", combination)
        password = bytes(combination, encoding="utf8")
        try:
            my_zip.extractall(pwd=password)
        except RuntimeError:
            pass
        else:
            print("The password is:", combination)  # pog
            break
