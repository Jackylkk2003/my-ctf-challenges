from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import subprocess

print("Welcome to the Key Exchange Protocol!")
print("This service is currently in version 1.1")

change_log = open("change_log_v1.1.txt", "r").read()
print("Change Log:")
print(change_log)

output = subprocess.check_output(["./generate"]).decode().strip().split("\n")

G = list(map(int, output[0].split()))
public_a = list(map(int, output[1].split()))
public_b = list(map(int, output[2].split()))
shared_key = list(map(int, output[3].split()))

print("G:", G)
print("Alice's public key:", public_a)
print("Bob's public key:", public_b)

key = sha256(bytes(shared_key)).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)

flag = open("flag.txt", "rb").read()
ciphertext = cipher.encrypt(pad(flag, 16))

print("Flag:", ciphertext.hex())
