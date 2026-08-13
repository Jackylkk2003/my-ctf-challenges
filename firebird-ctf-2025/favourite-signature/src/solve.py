import hashlib
from pwn import *
from chall import *

HOST = "localhost"
PORT = 3000

# context.log_level = "DEBUG"
with remote(HOST, PORT) as io:
    io.recvuntil(b"RNG with a=")
    a = int(io.recvline().strip().decode())
    io.recvuntil(b"Signature = ")
    m = int(hashlib.sha256(welcome.encode()).hexdigest(), 16)

    # r1 = (e1 * G).x
    # s1 = (m + priv * r1) * e1^-1
    r1, s1 = map(int, io.recvline().strip().decode().split())
    io.sendlineafter(b"Enter the message to sign: ", welcome.encode())
    io.recvuntil(b"Signature = ")

    # r2 = (e2 * G).x
    # s2 = (m + priv * r2) * e2^-1

    r2, s2 = map(int, io.recvline().strip().decode().split())
    io.sendlineafter(b"Enter the message to sign, again: ", give_flag.encode())

    # e2 = a * e1
    # s2 = (m + priv * r2) * (a * e1)^-1
    # a * s2 = (m + priv * r2) * e1^-1
    # a * s2 - s1 = priv * (r2 - r1) * e1^-1
    # priv * e1^-1 = (a * s2 - s1) * (r2 - r1)^-1

    # s1 = m * e1^-1 + priv * e1^-1 * r1
    # s1 = m * e1^-1 + (a * s2 - s1) * (r2 - r1)^-1 * r1
    # s1 - (a * s2 - s1) * (r2 - r1)^-1 * r1 = m * e1^-1

    # e1 = (s1 - (a * s2 - s1) * (r2 - r1)^-1 * r1)^-1 * m
    e1 = pow(s1 - (a * s2 - s1) * pow(r2 - r1, -1, q) * r1, -1, q) * m % q

    # priv = (a * s2 - s1) * (r2 - r1)^-1 * e1
    priv = (a * s2 - s1) * pow(r2 - r1, -1, q) * e1 % q

    def sign_without_rng(m, priv, e):
        m = int(hashlib.sha256(m.encode()).hexdigest(), 16)
        r, _ = xy(secp256k1.mul(e, G))
        r = r % q
        s = (m + priv * r) * pow(e, -1, q) % q
        return r, s

    r3, s3 = sign_without_rng(give_flag, priv, (a * a * e1 + 1) % q)
    io.sendlineafter(b"Now sign it yourself: ", f"{r3} {s3}".encode())

    print(io.recvall())
