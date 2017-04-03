from sage.all import *

A = 130
B = 565
F = GF(719)

E = EllipticCurve(F, [A, B])

P = E(107, 443)
Q = E(608, 427)

_order = order(E)
factors = [f[0]*f[1] for f in factor(_order)]
l = []

for factor in factors:
    t = int(_order / factor)
    tP = t*P
    tQ = t*Q
    for j in range(factor):
        if j*tP == tQ:
            l.append(j)
            break
    print l

n = crt(l, factors)
assert P*n == Q

# vim: set ft=python:
