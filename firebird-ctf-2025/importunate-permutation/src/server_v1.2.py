from Crypto.Random import random
from hashlib import sha256
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

print("Welcome to the Importunate Permutation Service!")
print("This service is currently in version 1.2")

change_log = open("change_log_v1.2.txt", "r").read()
print("Change Log:")
print(change_log)

N = 100
factorial = lambda n: 1 if n == 0 else n * factorial(n - 1)
factorials = [factorial(i) for i in range(101)]


def order(nums):
    """
    A permutation has order k means that it is obtained by calling next_permutation k times on the sorted list.
    """

    if nums == []:
        return 0
    cnt = sum([1 for i in nums[1:] if i < nums[0]])
    return cnt * factorials[len(nums) - 1] + order(nums[1:])


def generate(nums, k):
    """
    Apply next_permutation k times on the sorted list.
    """
    if nums == []:
        return []
    n = len(nums)
    i = k // factorials[n - 1]
    k = k % factorials[n - 1]
    return [nums[i]] + generate(nums[:i] + nums[i + 1 :], k)


G_order = private_a = private_b = factorials[N]
G = list(range(N))
random.shuffle(G)
G_order = order(G)

private_a = random.randrange(factorials[N])
private_b = random.randrange(factorials[N])

public_a = generate(list(range(N)), (G_order + private_a) % factorials[N])
public_b = generate(list(range(N)), (G_order + private_b) % factorials[N])

print("G:", G)
print("Alice's public key:", public_a)
print("Bob's public key:", public_b)

shared_key = generate(list(range(N)), (G_order + private_a + private_b) % factorials[N])

key = sha256(bytes(shared_key)).digest()[:16]
cipher = AES.new(key, AES.MODE_ECB)

flag = open("flag.txt", "rb").read()
ciphertext = cipher.encrypt(pad(flag, 16))

print("Flag:", ciphertext.hex())
