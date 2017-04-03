import sys

def mips_main(x):
    L = [0]*17
    L[4] = x
    L[6] = L[4] & -16777216
    L[16] = L[4] & 16711680
    L[7] = L[4] & 65280
    L[4] = L[4] & 255
    L[3] = L[6] >> 24
    L[2] = L[0]

    while 1:
        if L[2] < 13:
            L[5] = 1
        else:
            L[5] = 0
        L[2] += 1
        if L[5] == 0:
            break
        L[3] -= 13

    L[3] -= 6
    L[5] = (L[3] << 24) % (-2**31)
    L[16] = L[16] >> 16
    L[2] = L[16] - 81
    L[8] = L[2] << 6
    L[3] = L[2] << 8
    L[3] = L[3] - L[8]
    L[3] = L[2] - L[3]
    L[7] = L[7] >> 8
    L[2] = L[4] << 1
    L[2] += 3
    L[3] = L[3] << 16
    if L[7] != L[2]:
        L[2] = 165
    else:
        L[2] = 94

    L[2] = L[2] - 94
    L[2] = L[2] << 8
    L[6] = L[6] >> 24
    L[16] = L[6] - L[16]
    L[4] = L[4] - L[16]
    L[3] = (L[5] + L[3]) % (2**31) #lol
    L[3] = L[2] + L[3]
    L[16] = L[4] + L[3]
    print L
    if L[16] != L[0]:
        return 0
    return 1

print mips_main(10)
print mips_main(1000000000)
# i = 0
# while i < 4300000000:
#     if i % 500000 == 0:
#         print i
#     if mips_main(i):
#         print "Success! i={}".format(hex(i))
#         with open("OUT", "a") as f:
#             f.write("Success w/ i: {}\n".format(i))
#         sys.exit(1)
#     i += 1
# print "Done"
