from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from pwn import *
from tqdm import tqdm
import os
import itertools


def PoW_solve(target):
    hex_set = "0123456789abcdef"
    length = 5
    for ch in itertools.product(hex_set, repeat=length):
        ch = "".join(ch).encode()
        a = pad(ch, 16)
        h = AES.new(a, AES.MODE_ECB).encrypt(a).hex()[:4]
        if h == target:
            return ch


# context.log_level = "DEBUG"
with remote("...", 3000) as io:
    io.recvuntil(b"h = ")
    target = io.recvline().strip().decode()
    io.sendline(PoW_solve(target))
    io.recvline()
    ciphertext = bytes.fromhex(io.recvline().strip().decode())
    iv = ciphertext[:16]
    ciphertext = ciphertext[16:]

    def attack(iv: bytes, block: bytes):
        known_enc = b""
        for i in reversed(range(16)):
            padding = b"\x00" * i + bytes([16 - i]) * (16 - i)
            for j in range(256):
                test = b"\x00" * i + bytes([j]) + known_enc
                iv_ = xor(test, padding)
                block1 = os.urandom(16)
                block2 = os.urandom(16)
                payload = block1 + block2 + xor(block1, block2, iv_) + block
                io.sendline(payload.hex().encode())
            candidates = []
            for j in range(256):
                io.recvuntil(b":")
                if b")" in io.recvline():
                    candidates += [j]
            for j in candidates:
                test = b"\xff" * i + bytes([j]) + known_enc
                iv_ = xor(test, padding)
                block1 = os.urandom(16)
                block2 = os.urandom(16)
                payload = block1 + block2 + xor(block1, block2, iv_) + block
                io.sendline(payload.hex().encode())
            for j in candidates:
                io.recvuntil(b":")
                if b")" in io.recvline():
                    known_enc = bytes([j]) + known_enc
        return xor(known_enc, iv)

    plaintext = b""
    for i in tqdm(range(0, len(ciphertext), 16)):
        block = ciphertext[i : i + 16]
        plaintext += attack(iv, block)
        iv = xor(iv, block)
    print(plaintext)
