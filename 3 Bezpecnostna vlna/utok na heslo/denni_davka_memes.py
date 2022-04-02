import pyzipper

with pyzipper.AESZipFile("downloaded.zip") as my_zip:
    with open("rockyou.txt") as dictionary:
        for word in dictionary:
            word = word.strip()
            print("Trying:", word)
            password = bytes(word, encoding="utf8")
            try:
                my_zip.extractall(pwd=password)
            except:
                pass
            else:
                print("The password is:", word)  # Snickers1
                break
