import random, string


def caesar(char, shift):
    alphabet = ""
    if char.islower():
        alphabet = string.ascii_lowercase
    elif char.isupper():
        alphabet = string.ascii_uppercase
    elif char.isdigit():
        alphabet = string.digits
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = string.maketrans(alphabet, shifted_alphabet)
    return char.translate(table)

random.seed("random")

enc = "BNZQ:4pg33e44sdu4wu8198y15q685vpx8041"

shifts = []
flag = ""
for c in enc:
    if c.isdigit():
        shift = random.randrange(0, 10)
    elif c in string.ascii_letters:
        shift = random.randrange(0, 26)
    else:
        shift = 0

    flag += caesar(c, -shift)

print flag
