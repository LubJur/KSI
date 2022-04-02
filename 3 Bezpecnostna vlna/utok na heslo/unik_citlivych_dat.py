import pyzipper
import itertools

words = ["Homer", "Jay", "Simpson", "Springfield", "Abraham", "Mona", "Marge", "Bart", "Lisa", "Maggie", "Spasitel",
         "Snehulka", "donut", "pivo", "burger", "baseball", "fotbal", "basketbal"]
numbers = ["12", "5", "05", "1956", "56", "19"]

words_up = [i.upper() for i in words]
words_lo = [i.lower() for i in words]

info = words + words_up + words_lo + numbers

comb2 = itertools.product(info, repeat=2)
comb3 = itertools.product(info, repeat=3)

with open("passwords.txt", "a") as dictionary:
    for i in info:
        dictionary.write(i+"\n")

    for i in comb2:
        dictionary.write("".join(i)+"\n")

    for i in comb3:
        dictionary.write("".join(i)+"\n")

with pyzipper.AESZipFile("homer_simpson.zip") as my_zip:
    with open("passwords.txt") as dictionary:
        for word in dictionary:
            word = word.strip()
            print("Trying:", word)
            password = bytes(word, encoding="utf8")
            try:
                my_zip.extractall(pwd=password)
            except:
                pass
            else:
                print("The password is:", word)  # Maggie1956
                break
