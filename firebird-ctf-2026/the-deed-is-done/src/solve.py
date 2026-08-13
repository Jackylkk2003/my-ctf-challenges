from sage.all import *
from pwn import *
from Crypto.Util.number import long_to_bytes
from tqdm import tqdm

# Using the implementation of related message attack from https://github.com/jvdsn/crypto-attacks
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
    g0 = ring(e.list()[m // 2:])
    g1 = ring(f.list()[m // 2:])
    S00, S01, S10, S11 = _polynomial_hgcd(ring, g0, g1)
    return S01 * R00 + (S00 - q * S01) * R10, S01 * R01 + (S00 - q * S01) * R11, S11 * R00 + (S10 - q * S11) * R10, S11 * R01 + (S10 - q * S11) * R11

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

def attack(N, e1, e2, c1, c2, f1, f2):
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
    g1 = f1(x) ** e1 - c1
    g2 = f2(x) ** e2 - c2
    g = -fast_polynomial_gcd(g1, g2).monic()
    return int(g[0])

def try_get_flag(n, e1, e2, c1, c2, k1, k2, encrypted_flag):
    f1 = lambda x: x
    f2 = lambda x: (e1*k2*x+k1-k2)*pow(e2*k1, -1, n)
    try:
        d1 = attack(n, e1, e2, c1, c2, f1, f2)
        if (d1 * e1 - 1) % k1 != 0:
            return None
        phi = (d1 * e1 - 1) // k1
        d = pow(0x10001, -1, phi)
        flag = pow(encrypted_flag, d, n)
        return long_to_bytes(flag)
    except Exception as e:
        return None

def main():
    HOST = "localhost"
    PORT = 3000

    with remote(HOST, PORT) as io:
        io.recvuntil(b'n = ')
        n = int(io.recvline().strip())
        io.recvuntil(b'encrypted_flag = ')
        encrypted_flag = int(io.recvline().strip())

        io.sendlineafter(b'e: ', b'101')
        res = io.recvuntil((b'c: ', b'GG'))
        if b'GG' in res:
            return
        e1 = 101
        c1 = int(io.recvline().strip())

        io.sendline(b'103')
        res = io.recvuntil((b'c: ', b'GG'))
        if b'GG' in res:
            return
        e2 = 103
        c2 = int(io.recvline().strip())

        for k1 in tqdm(range(1, e1)):
            for k2 in (range(1, e2)):
                flag = try_get_flag(n, e1, e2, c1, c2, k1, k2, encrypted_flag)
                if flag is not None and flag.startswith(b'firebird{'):
                    print(f'Found flag: {flag}')
                    return

if __name__ == '__main__':
    main()