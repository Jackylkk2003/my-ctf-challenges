from Crypto.Util.number import getPrime, bytes_to_long

p, q = getPrime(1024), getPrime(1024)
n = p * q
e = 0x10001
ctr = 0


def rsa_encrypt(m):
    global ctr
    ctr += 1
    return pow(m + ctr, e, n)


def encrypt(x):
    m = []
    while x > 0:
        m.append(x % n)
        x //= n
    if len(m) == 0:
        m.append(0)
    c = [rsa_encrypt(mi) for mi in m]
    ciphertext = 0
    for ci in reversed(c):
        ciphertext = ciphertext * n + ci
    return ciphertext


def choice():
    print("1. Encrypt hidden message")
    print("2. Encrypt a message of your choice")
    return int(input("Your choice: ")) == 1


def main():
    print(f"{n = }")
    for _ in range(2):
        if choice():
            m = open("hidden_message.txt", "rb").read()
            m = bytes_to_long(m)
        else:
            m = int(input("Enter the message to encrypt: "))
        c = encrypt(m)
        print(f"Here is your encrypted message: {c}")
    print("Bye!")
    return


if __name__ == "__main__":
    main()
