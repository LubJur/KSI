# https://tkdocs.com/tutorial/tree.html
with open("contacts.vcf", "rw") as file:
    list_of_xy = []
    line = file.readline()
    while line != "":
        line = file.readline()
        if line.startswith("$GPGGA"):
            line = line.split(",")

