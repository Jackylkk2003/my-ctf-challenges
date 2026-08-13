from Crypto.Util.number import getPrime, bytes_to_long

def main():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    phi = (p - 1) * (q - 1)    

    with open("flag.txt", "rb") as f:
        flag = f.read().strip()

    encrypted_flag = pow(bytes_to_long(flag), 0x10001, n)
    print(f"{n = }")
    print(f"{encrypted_flag = }")

    for _ in range(2):
        e = int(input("e: "))
        assert e >= 100 # Credit to Mystiz for this idea
        try:
            d = pow(e, -1, phi)
            c = pow(d, e, n)
            print("c:", c)
        except ValueError:
            print("GG")
            return

if __name__ == "__main__":
    main()
