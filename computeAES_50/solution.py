from Crypto.Cipher import AES

ciphertext = "t1h0qbcOhRQF5E46bsNLimfbcI6egrKP4LHtKR3lT4UdWjhssM8RQSBT7S/8rcRy".decode("base64")
key = "T5uVzYtuBNv6vwjohslV4w==".decode("base64")
cipher = AES.AESCipher(key, AES.MODE_ECB)
print cipher.decrypt(ciphertext)

# flag{do_not_let_machines_win_1e6b4cf4}
