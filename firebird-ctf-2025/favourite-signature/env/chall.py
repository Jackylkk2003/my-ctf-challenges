import hashlib
from Crypto.Random.random import randint as insecure_randint  # I don't trust this :<
from elliptic_curve import *

welcome = "Welcome to Firebird CTF!"
give_flag = "Gib flag plsssss UwU"


class RNG:  # I only trust what I write myself :>
    def __init__(self, a=None, c=None, seed=None):
        if a is None:
            a = insecure_randint(2, q - 1)
        if seed is None:
            seed = insecure_randint(2, q - 1)
        if c is None:
            c = 0
        self.m = q
        self.a = a
        self.c = c
        self.seed = seed

    def next(self):
        old_value = self.seed
        self.seed = (self.seed * self.a + self.c) % self.m
        self.c += 1
        return old_value

    def __repr__(self):
        return f"RNG with a={self.a}"


def get_key_pair(priv=None):
    if priv is None:
        priv = insecure_randint(2, q - 1)
    V = secp256k1.mul(priv, G)
    return V, priv


def sign(m, priv, rng):
    m = int(hashlib.sha256(m.encode()).hexdigest(), 16)
    e = rng.next()
    r, _ = xy(secp256k1.mul(e, G))
    r = r % q
    s = (m + priv * r) * pow(e, -1, q) % q
    return r, s


def verify(m, V, r, s):
    m = int(hashlib.sha256(m.encode()).hexdigest(), 16)
    v1 = m * pow(s, -1, q) % q
    v2 = r * pow(s, -1, q) % q
    x_coor, _ = xy(secp256k1.add(secp256k1.mul(v1, G), secp256k1.mul(v2, V)))
    return x_coor == r


if __name__ == "__main__":
    rng = RNG()
    print(rng)
    V, priv = get_key_pair()

    print("Verification point V = ... Imma keep it a secret UwU")
    print(f"I can tell you that V = (???, ???, {V[2]}) though")

    # Signature 1
    r1, s1 = sign(welcome, priv, rng)
    print("Signature =", r1, s1)
    assert verify(welcome, V, r1, s1)

    # Signature 2
    message = input("Enter the message to sign: ").strip()
    assert all(c.isprintable() for c in message)
    assert message != give_flag
    r2, s2 = sign(message, priv, rng)
    print("Signature =", r2, s2)
    assert verify(message, V, r2, s2)

    # Signature 3
    message = input("Enter the message to sign, again: ").strip()
    assert all(c.isprintable() for c in message)
    r3, s3 = sign(message, priv, rng)
    assert verify(message, V, r3, s3)
    r4, s4 = map(int, input("Now sign it yourself: ").split())

    if message != give_flag:
        print("Umm... Maybe try to solve the sanity check challenge first?")
    elif r3 == r4 and s3 == s4:
        print(open("flag.txt").read())
    else:
        print("I don't like this signature >.<")
