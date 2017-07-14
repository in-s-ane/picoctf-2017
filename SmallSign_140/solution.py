from pwn import remote
import operator
import sys

# https://stackoverflow.com/a/1638415
def prime(i, primes):
    for prime in primes:
        if not (i == prime or i % prime):
            return False
    primes.add(i)
    return i

def historic(n):
    primes = set([2])
    i, p = 2, 0
    while True:
        if prime(i, primes):
            p += 1
            if p == n:
                return primes
        i += 1

def get_factors(n):
    # https://stackoverflow.com/a/16996439
    primfac = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            primfac.append(d)
            n //= d
        d += 1
    if n > 1:
        primfac.append(n)
    return primfac

signatures = {}

primes = historic(400)
r = remote("shell2017.picoctf.com", 25893)
print r.recvline()
n = int(r.recvline()[3:])
e = int(r.recvline()[3:])
print n
print e
for x in primes:
    print r.recv(1024)
    r.send("%d\n" % x)
    print x
    signature = int(r.recvline()[11:])
    print signature
    signatures[x] = signature

print r.recv(1024)
r.send("-1\n")
print r.recv(1024)
challenge = int(r.recvline())
print challenge
print r.recv(1024)
factors = get_factors(challenge)

print factors
for factor in factors:
    if factor not in signatures:
        print "Bad factors!"
        sys.exit(0)

new_signature = reduce(operator.mul, [signatures[factor] for factor in factors])
r.send("%d\n" % new_signature)
print r.recv(1024)
print r.recv(1024)

"""
We're given access to a service that will sign any number we want.
The formula for signing a message is s(m) = m^d % n.
To verify it, we can calculate v(c) = c^e % n.

Because of the multiplicative properties of signing, we know that s(m) * s(n) = s(mn)
Knowing this, we can generate a table of prime numbers and their corresponding signatures, and
use them to sign the challenge by factoring it for prime numbers.

This script might fail because the challenge number may have prime factors that aren't present
in the lookup table, but you'll eventually get the flag:
635f086917498ec123623c39ef31a81c
"""
