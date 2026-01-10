from pwn import *

# Code adapted from https://github.com/jvdsn/crypto-attacks
import logging
from itertools import product
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm

from sage.all import Zmod


def _polynomial_hgcd(ring, a0, a1):
    assert a1.degree() < a0.degree()

    if a1.degree() <= a0.degree() / 2:
        return 1, 0, 0, 1

    m = a0.degree() // 2
    b0 = ring(a0.list()[m:])
    b1 = ring(a1.list()[m:])
    R00, R01, R10, R11 = _polynomial_hgcd(ring, b0, b1)
    d = R00 * a0 + R01 * a1
    e = R10 * a0 + R11 * a1
    if e.degree() < m:
        return R00, R01, R10, R11

    q, f = d.quo_rem(e)
    g0 = ring(e.list()[m // 2 :])
    g1 = ring(f.list()[m // 2 :])
    S00, S01, S10, S11 = _polynomial_hgcd(ring, g0, g1)
    return (
        S01 * R00 + (S00 - q * S01) * R10,
        S01 * R01 + (S00 - q * S01) * R11,
        S11 * R00 + (S10 - q * S11) * R10,
        S11 * R01 + (S10 - q * S11) * R11,
    )


def fast_polynomial_gcd(a0, a1):
    """
    Uses a divide-and-conquer algorithm (HGCD) to compute the polynomial gcd.
    More information: Aho A. et al., "The Design and Analysis of Computer Algorithms" (Section 8.9)
    :param a0: the first polynomial
    :param a1: the second polynomial
    :return: the polynomial gcd
    """
    # TODO: implement extended variant of half GCD?
    assert a0.parent() == a1.parent()

    if a0.degree() == a1.degree():
        if a1 == 0:
            return a0
        a0, a1 = a1, a0 % a1
    elif a0.degree() < a1.degree():
        a0, a1 = a1, a0

    assert a0.degree() > a1.degree()
    ring = a0.parent()

    # Optimize recursive tail call.
    while True:
        logging.debug(f"deg(a0) = {a0.degree()}, deg(a1) = {a1.degree()}")
        _, r = a0.quo_rem(a1)
        if r == 0:
            return a1.monic()

        R00, R01, R10, R11 = _polynomial_hgcd(ring, a0, a1)
        b0 = R00 * a0 + R01 * a1
        b1 = R10 * a0 + R11 * a1
        if b1 == 0:
            return b0.monic()

        _, r = b0.quo_rem(b1)
        if r == 0:
            return b1.monic()

        a0 = b1
        a1 = r


def attack(N, e, c1, c2, f1, f2):
    """
    Recovers the shared secret if p1 and p2 are affinely related and encrypted with the same modulus and exponent.
    Uses a fast GCD algorithm from "Polynomial Division and Greatest Common Divisors"
    :param N: the modulus
    :param e: the public exponent
    :param c1: the ciphertext of the first encryption
    :param c2: the ciphertext of the second encryption
    :param f1: the first function to apply to the shared secret
    :param f2: the second function to apply to the shared secret
    :return: the shared secret
    """
    x = Zmod(N)["x"].gen()
    g1 = f1(x) ** e - c1
    g2 = f2(x) ** e - c2
    g = -fast_polynomial_gcd(g1, g2).monic()
    return int(g[0])


with remote("...", 3000) as io:
    io.sendline(b"1\n1")
    io.recvuntil(b"n = ")
    n = int(io.recvline().strip().decode())
    io.recvuntil(b"Here is your encrypted message: ")
    c1 = int(io.recvline().strip().decode())
    io.recvuntil(b"Here is your encrypted message: ")
    c2 = int(io.recvline().strip().decode())
    c1_list = []
    while c1 > 0:
        c1_list.append(c1 % n)
        c1 //= n
    if len(c1_list) == 0:
        c1_list.append(0)
    c2_list = []
    while c2 > 0:
        c2_list.append(c2 % n)
        c2 //= n
    if len(c2_list) == 0:
        c2_list.append(0)
    m = len(c1_list)

    print(f"{m = }")

    messages = []
    for i, m1, m2 in tqdm(zip(range(m), c1_list, c2_list), total=m):
        x = attack(n, 0x10001, m1, m2, lambda x: x + i + 1, lambda x: x + m + i + 1)
        messages.append(x)
        assert pow(x + i + 1, 0x10001, n) == m1
        assert pow(x + m + i + 1, 0x10001, n) == m2

    plaintext = 0
    for x in reversed(messages):
        plaintext = plaintext * n + x

    print(long_to_bytes(plaintext))
