from pwn import remote
import re

HOST = "shell2017.picoctf.com"
PORT = 41123

r = remote(HOST, PORT)
prompt = r.recv(1024)
print prompt
match = re.search("Please give me the '(\w)' character '(\d+)' times, followed by a single '(.)'", prompt)
ans = (match.group(1) * int(match.group(2))) + match.group(3)
r.send(ans + "\n")
print r.recv(1024)

# with_some_recognition_and_training_delusions_become_glimpses_040b5dbaa85682f120e15e7d1224f09c
