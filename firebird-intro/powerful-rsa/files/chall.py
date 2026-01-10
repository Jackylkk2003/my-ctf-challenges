from Crypto.Util.number import getPrime, bytes_to_long
from flag import flag

p = getPrime(128)
q = 19  # Free prime!

n = p**q
e = 0x10001

c = pow(bytes_to_long(flag.encode()), e, n)

with open("enc.txt", "w") as f:
    f.write(f"n = {hex(n)}\n")
    f.write(f"e = {hex(e)}\n")
    f.write(f"c = {hex(c)}\n")
