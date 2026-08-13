from aes import *
import os
import random

def main():
    my_favourite_box = [random.randint(0, 255) for _ in range(16)]
    print("My favourite box is:", *my_favourite_box)

    print("Now, tell me your favourite box!")

    your_favourite_box = list(map(int, input("Your favourite box: ").split()))
    set_s_box(your_favourite_box)

    key = os.urandom(16)
    m = pad(open("flag.txt", "rb").read())
    cipher = AES(key)

    c = b""
    for i in range(0, len(m), 16):
        c += cipher.encrypt_block(m[i:i+16])

    print("The flag in your favourite box:", c.hex())

    m = bytes(list(map(lambda x: your_favourite_box[x], my_favourite_box)))

    cipher = AES(key)
    c = cipher.encrypt_block(m)
    
    print("Your favourite box in my favourite box in your favourite box:", c.hex())

if __name__ == "__main__":
    main()