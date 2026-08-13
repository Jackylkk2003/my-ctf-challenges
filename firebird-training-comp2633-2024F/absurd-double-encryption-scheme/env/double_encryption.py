import os
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad
from typing import List


class DESDES:
    def __init__(self, key: bytes, modes: List[int]):
        self.key = key.hex().encode()
        ivs = [os.urandom(8) for _ in range(2)]
        print("List of iv:")
        for iv in ivs:
            print(iv.hex())

        self.des_ciphers = [
            DES.new(self.key[i * 8 : i * 8 + 8], modes[i % 2], iv=ivs[i % 2])
            for i in range(len(self.key) // 8)
        ]

    def encrypt(self, message: bytes) -> bytes:
        c = message
        for des_cipher in self.des_ciphers:
            c = des_cipher.encrypt(c)
        return c


def main():
    try:
        with open("flag.txt", "rb") as f:
            m = f.read()
    except:
        m = b"flag{this_is_a_test_flag}"

    key = os.urandom(8)
    print(f"Your lucky number today: {key[-1]}")

    allowed_list = [DES.MODE_CBC, DES.MODE_CFB, DES.MODE_OFB]

    mode1 = int(input("Encryption mode 1: "))
    if mode1 not in allowed_list:
        print("Invalid mode")
        return

    mode2 = int(input("Encryption mode 2: "))
    if mode2 not in allowed_list or mode2 == mode1:  # Same mode no good :<
        print("Invalid mode")
        return

    des = DESDES(key, [mode1, mode2])

    message = input("Enter message in hex: ")
    message = bytes.fromhex(message)
    message = pad(message, 8)

    print(f"Encrypted message: {des.encrypt(message).hex()}")

    aes = AES.new(key.hex().encode(), AES.MODE_ECB)  # Same mode really no good :<
    m = pad(m, 16)
    print(f"Flag: {aes.encrypt(m).hex()}")


if __name__ == "__main__":
    main()
