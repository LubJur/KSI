from Cryptodome.Cipher import DES
"""
with open("testfile", "rb") as file:
    subor = file.read()
    print(subor)
    secret = b"\x00\xF1\xF0\x00\x00\x4B\x61\x72"
    key = DES.new(secret, DES.MODE_ECB)
with open("testfile", "wb") as file:
    file.write(key.encrypt(subor))
"""

with open("prisonerDetails", "rb") as file:
    subor = file.read()
    for i in range(0, 16777216):
        byty = i.to_bytes(3, "big")
        secret = b"".join([b"\x00\xF1", byty, b"\x4B\x61\x72"])
        key = DES.new(secret, DES.MODE_ECB)
        dec = key.decrypt(subor)
        try:
            print(dec.decode())
        except (UnicodeDecodeError, TypeError):
            pass
        else:
            print("FOUND", i, secret)
