import os
from Crypto.Cipher import AES


def main():
    try:
        with open("flag.txt", "rb") as f:
            m = f.read()
    except:
        m = b"flag{this_is_a_test_flag}"

    key = os.urandom(16)
    nonce = os.urandom(12)

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    flag_enc = cipher.encrypt(m).hex()

    print(f"{flag_enc = }")

    message = input("Gimme a hex message, UwU: ")
    message = bytes.fromhex(message)

    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    message_enc = cipher.encrypt(message).hex()

    print(f"{message_enc = }")


if __name__ == "__main__":
    main()
