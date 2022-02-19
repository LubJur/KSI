# to open the database, change filepath to match database location

from lzma import open

filepath = "src/db/__main__"

with open(filepath, "rb") as file:
    print(file.read().decode())
