import pyzipper

with pyzipper.AESZipFile("downloaded.zip") as my_zip:
    with open("rockyou.txt") as dictionary:
        # https://www.kite.com/python/answers/how-to-iterate-through-the-lines-of-a-file-in-python
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
