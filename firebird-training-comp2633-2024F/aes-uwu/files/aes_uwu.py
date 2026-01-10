from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import datetime
import os
import random


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))


def PoW():
    hex_set = "0123456789abcdef"
    length = random.randint(5, 10) * 2
    a = "".join(random.choice(hex_set) for i in range(length))
    a = a.encode()
    a = pad(a, 16)
    h = AES.new(a, AES.MODE_ECB).encrypt(a).hex()[:4]

    print("======== Proof-of-Work enabled ========")
    print(f"Send me a hex code (in lowercase) such that:")
    print(f"<The condition is obfuscated by the king of UwU from Track A>")
    print(f"h = {h}")

    ans = input("> ")
    ans = pad(ans.encode(), 16)
    if len(ans) != 16:
        print("Try harder!")
        exit()

    if AES.new(ans, AES.MODE_ECB).encrypt(ans).hex()[:4] != h:
        print("Proof-of-Work failed!")
        exit()


class AES_UWU:
    def __init__(self, key: bytes):
        self.key: bytes = key
        self.cipher = AES.new(self.key, AES.MODE_ECB)  # I like ECB mode!
        self.used_iv = set()

    # Encrypt the plaintext with AES-UWU mode (?)
    # Returns ciphertext in hex string
    def encrypt(self, plaintext: str) -> str:
        plaintext: bytes = pad(plaintext.encode(), AES.block_size)
        iv: bytes = os.urandom(16)
        self.used_iv.add(iv)
        ciphertext: bytes = iv

        for i in range(0, len(plaintext), AES.block_size):
            block = plaintext[i : i + AES.block_size]
            block = xor(block, iv)
            block = self.cipher.encrypt(block)
            ciphertext += block
            iv = xor(iv, block)
        return ciphertext.hex()

    # Decrypt the ciphertext from hex string
    def decrypt(self, ciphertext: str):
        ciphertext = bytes.fromhex(ciphertext)
        iv = ciphertext[: AES.block_size]

        assert iv not in self.used_iv  # iv reuse is vulnerable!

        self.used_iv.add(iv)

        plaintext = b""
        for i in range(AES.block_size, len(ciphertext), AES.block_size):
            block = ciphertext[i : i + AES.block_size]
            decrypted = self.cipher.decrypt(block)
            decrypted = xor(decrypted, iv)
            plaintext += decrypted
            iv = xor(iv, block)
        try:
            plaintext = unpad(plaintext, AES.block_size)
        except:
            # Ciphertext modified! u bad bad!
            return ":("

        # You didn't modify the ciphertext, so u good good!
        return ":)"


if __name__ == "__main__":
    PoW()

    starttime = datetime.datetime.now()  # Don't worry, PoW is not counted in time limit

    key = os.urandom(16)
    cipher = AES_UWU(key)

    try:
        with open("message.txt", "r") as f:
            message = f.read()
    except:
        message = """
Too lazy to test the cipher, let's test in production.
Here is a fake flag for u: flag{Fake Flag UwU}
"""

    encrypted = cipher.encrypt(message)
    assert len(encrypted) == 256

    print("Here is my message to you")
    print(encrypted)

    while (datetime.datetime.now() - starttime).seconds < 300:
        ciphertext = input("> ")

        # I don't want u do decrypt my message, so I will check the length of the ciphertext
        assert len(ciphertext) == 128

        # This is not a pwn challenge! This is track B!
        assert all(c in "0123456789abcdef" for c in ciphertext)

        print(cipher.decrypt(ciphertext))

    print("OK I go to sleep now, bye bye!")
