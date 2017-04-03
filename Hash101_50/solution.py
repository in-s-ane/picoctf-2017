from pwn import remote
import re

HOST = "shell2017.picoctf.com"
PORT = 9661

r = remote(HOST, PORT)

# Level 1
print r.recv(1024)
prompt = r.recv(1024)
print prompt
enc = re.search("ASCII representation of (.*)", prompt).group(1)
# Decode from binary
ans = hex(int(enc, 2))[2:].decode("hex")
print ans
r.send(ans + "\n")
print r.recv(1024)

# Level 2
print r.recv(1024)
# Encode to hex
ans = ans.encode("hex")
r.send(ans + "\n")
print r.recv(1024)
print r.recv(1024)
# Convert to int
ans = int(ans, 16)
r.send(str(ans) + "\n")
print r.recv(1024)

# Level 3
prompt = r.recv(1024)
print prompt
end = re.search("result in a (\d+)", prompt).group(1)
r.send(chr(int(end)) + "\n")
print r.recv(1024)

# Level 4
print r.recv(1024)
# Look up the hash on https://www.hashkiller.co.uk/md5-decrypter.aspx, and submit the original string
r.interactive()

# c3ee093f26ba147ccc451fd13c91ffce
