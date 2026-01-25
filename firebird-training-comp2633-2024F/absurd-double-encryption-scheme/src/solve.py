from pwn import *
from Crypto.Cipher import AES, DES
from Crypto.Util.number import long_to_bytes
from Crypto.Util.Padding import pad
from tqdm import tqdm
import itertools

HOST = "localhost"
PORT = 3000
context.log_level = "debug"
p = remote(HOST, PORT)

p.sendline(b"2")
p.sendline(b"3")
p.sendline(b"00")

p.recvuntil(b"Your lucky number today: ")
known_bytes = long_to_bytes(int(p.recvline().strip().decode())).hex().encode()
p.recvuntil(b"List of iv:\r\n")
iv1 = p.recvline().strip().decode()
iv2 = p.recvline().strip().decode()
p.recvuntil(b"Encrypted message: ")
enc = bytes.fromhex(p.recvline().strip().decode())
p.recvuntil(b"Flag: ")
flag = bytes.fromhex(p.recvline().strip().decode())

p.close()

table = {}
m = pad(bytes.fromhex("00"), 8)
for key in tqdm(itertools.product(b"abdf02468", repeat=6), total=9**6):
    cipher = DES.new(bytes(key) + known_bytes, 3, iv=bytes.fromhex(iv2))
    table[cipher.decrypt(enc)] = bytes(key) + known_bytes

for key in tqdm(itertools.product(b"abdf02468", repeat=8), total=9**8):
    cipher = DES.new(bytes(key), 2, iv=bytes.fromhex(iv1))
    if cipher.encrypt(m) in table:
        cipher = DES.new(bytes(key), 2, iv=bytes.fromhex(iv1))
        key1 = bytes(key)
        key2 = table[cipher.encrypt(m)]
        break

print(key1)
print(key2)
cipher1 = DES.new(key1, 2, iv=bytes.fromhex(iv1))
cipher2 = DES.new(key2, 3, iv=bytes.fromhex(iv2))
assert cipher2.encrypt(cipher1.encrypt(m)).hex() == enc.hex()
combined_key = key1 + key2
for offset in tqdm(itertools.product(b"\x00\x01", repeat=16), total=2**16):
    key = xor(combined_key, offset)
    cipher = AES.new(key, AES.MODE_ECB)
    if cipher.decrypt(flag[:16])[:5] == b"flag{":
        print(cipher.decrypt(flag))
        break
