import sys
import string as S

key = "yuoteavpxqgrlsdhwfjkzi_cmbn"
STRING = "DLLDLDLLLLLDLLLLRLDLLDLDLLLRRDLLLLRDLLLLLDLLRLRRRDLLLDLLLDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLLRLDLLDLLRLRRDLLLDLLRLRRRDLLRDLLLLLDLLLRLDLLDLLRLRRDLLLLLDLLRDLLLRRLDLLLDLLLLLDLLRDLLRLRRDLLLDLLLDLLRLRRRDLLLLLDLLLLRLDLLLRRLRRDDLLLRRDLLLRRLRDLLLRLDLRRDDLLLRLDLLLRRRDLLRLRRRDLRRLD"

def init2(a,b):
    result = []
    if a:
        if (a[2] >= b):
            a[0] = init2(a[0], b)
            result = a
        else:
            a[1] = init2(a[1], b)
            result = a
    else:
        result = [0,0,b]
    return result


def init_data(a):
    result = 0
    i = 0
    while i < len(a):
        result = init2(result, a[i])
        i += 1
    return result

def validate2(f, s, p):
    if not (f and len(s) > 0):
        return False
    if p == f[2]:
        return s[0] == 'D'
    if p > f[2]:
        if s[0] == 'R':
            return validate2(f[1], s[1:], p)
        return False
    if s[0] == 'L':
        return validate2(f[0], s[1:], p)

def validate(f, s, p):
    if not (f and s and p):
        return False
    truth = 1
    si = 0
    pi = 0
    while si < len(s) and pi < len(p):
        truth = truth and validate2(f, s[si:], p[pi])
        while s[si] == 'L' or s[si] == 'R':
            si += 1
        si += 1
        pi += 1
    #return si == len(s) and pi == len(p) and truth
    return truth

def main(string):
    forest = init_data(key)
    print forest

    known = ""
    i = 0
    while i < 100:
        for guess in (S.lowercase+"0123456789_{}"):
            print "Guessing {}, Total {}".format(guess,known+guess)
            if validate(forest, string, known+guess):
                print "Found another! {}. Total: {}".format(guess,known+guess)
                known = known+guess
                break
        i += 1

main(STRING)
