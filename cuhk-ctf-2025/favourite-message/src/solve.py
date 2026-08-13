from pwn import *
from Crypto.Cipher import AES

HOST = "localhost"
PORT = 3000

with remote(HOST, PORT) as io:
    io.sendlineafter(b"Tell me your favourite message: ", b"0" * 16 + b"{flag}")
    io.recvuntil(b"\nUwU ")
    c = bytes.fromhex(io.recvline().strip().decode())
    key = xor(b"0" * 16, c[:16])
    m = b""
    for i in range(16, len(c), 16):
        cipher = AES.new(key, AES.MODE_ECB)
        block = c[i : i + 16]
        b = cipher.decrypt(block)
        m += b
        key = xor(b, block)
    print(m)
