# ECC2
##### Description:
More elliptic curve cryptography fun for everyone!
[handout.txt](handout.txt)
(Yes, the flag will just be the number n.)

#### Hints:
Using SageMath (or something similar which supports working with elliptic curves) will be very helpful.

#### Solution:

Looking up elliptic curve attacks, we find [this pdf](http://security.cs.pub.ro/hexcellents/wiki/_media/10.1.1.132.6034.pdf).
Inside, we find the Pohlig-Hellman method, which lets us solve for the exponent since the order of the curve has multiple factors.

Following the steps described in the pdf, we can solve for n.

```
$ sage solution.sage
152977126447386808276536247114
```
