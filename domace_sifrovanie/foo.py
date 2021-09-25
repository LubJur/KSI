def encode(n, plain_text):
    plain_text = list(plain_text)
    return_text = []
    to_flip = []

    for i in plain_text:
        to_flip.append(i)
        if len(to_flip) == n:
            return_text.extend(to_flip[::-1])
            to_flip = []

    return_text.extend(to_flip[::-1])  # ked sa neda rozdelit pekne
    return "".join(return_text)

print(encode(2, "Ahoj"))
