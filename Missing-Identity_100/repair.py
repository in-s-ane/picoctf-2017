f = open("file", "rb").read()
f = "\x50\x4b\x03\x04\x50\x4b" + f[6:]
open("repaired.zip", "wb").write(f)
