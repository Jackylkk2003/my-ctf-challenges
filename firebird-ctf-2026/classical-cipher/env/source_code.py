import abc
from string import ascii_lowercase
from typing import override # https://www.youtube.com/watch?v=LLjfal8jCYI
from Crypto.Random.random import shuffle, choice, randint

# Classical Cipher means the ciphers are implemented with heavy use of classes, right?

class Cipher(abc.ABC):
    # 誰だこんな親クラス作ったのは
    @abc.abstractmethod
    def encrypt(self, plaintext: str) -> str:
        pass

    @abc.abstractmethod
    def decrypt(self, ciphertext: str) -> str:
        pass

    class Convertor:
        @staticmethod
        def chr_to_int(c):
            return ord(c) - ord('a')

        @staticmethod
        def int_to_chr(i):
            return chr(i + ord('a'))

class SubstitutionCipher(Cipher):
    def __init__(self, key=None):
        if key is None:
            self.key = list(ascii_lowercase)
            shuffle(self.key)
        else:
            self.key = key

    @override
    def encrypt(self, plaintext):
        assert all(c in ascii_lowercase for c in plaintext), "Plaintext must only contain lowercase letters"
        return ''.join(self.key[ascii_lowercase.index(char)] for char in plaintext)

    @override
    def decrypt(self, ciphertext):
        assert all(c in ascii_lowercase for c in ciphertext), "Ciphertext must only contain lowercase letters"
        return ''.join(ascii_lowercase[self.key.index(char)] for char in ciphertext)

class VigenereCipher(Cipher):
    def __init__(self, key=None, key_length=10):
        if key is None:
            key = ''.join(choice(ascii_lowercase) for _ in range(key_length))
        self.key = key
        self.key_length = len(key)

    @override
    def encrypt(self, plaintext):
        assert all(c in ascii_lowercase for c in plaintext), "Plaintext must only contain lowercase letters"
        return ''.join(self.Convertor.int_to_chr((self.Convertor.chr_to_int(ch) + self.Convertor.chr_to_int(self.key[i % self.key_length])) % 26) for i, ch in enumerate(plaintext))

    @override
    def decrypt(self, ciphertext):
        assert all(c in ascii_lowercase for c in ciphertext), "Ciphertext must only contain lowercase letters"
        return ''.join(self.Convertor.int_to_chr((self.Convertor.chr_to_int(ch) - self.Convertor.chr_to_int(self.key[i % self.key_length])) % 26) for i, ch in enumerate(ciphertext))

class TranspositionCipher(Cipher):
    def __init__(self, key=None, key_length=16):
        if key is None:
            self.key = list(range(key_length))
            shuffle(self.key)
        else:
            self.key = key
        self.key_length = len(self.key)
        self.inverse_key = [self.key.index(i) for i in range(self.key_length)]

    @override
    def encrypt(self, plaintext):
        assert len(plaintext) % self.key_length == 0, "Plaintext length must be a multiple of key length"
        return ''.join(
            ''.join(block[kj] for kj in self.key)
            for block in (plaintext[i:i+self.key_length] for i in range(0, len(plaintext), self.key_length))
        )
    
    @override
    def decrypt(self, ciphertext):
        assert len(ciphertext) % self.key_length == 0, "Plaintext length must be a multiple of key length"
        return ''.join(
            ''.join(block[kj] for kj in self.inverse_key)
            for block in (ciphertext[i:i+self.key_length] for i in range(0, len(ciphertext), self.key_length))
        )

class SuperCipher(Cipher):
    def __init__(self, ciphers):
        self.ciphers = ciphers

    @override
    def encrypt(self, plaintext):
        for cipher in self.ciphers:
            plaintext = cipher.encrypt(plaintext)
        return plaintext
    
    @override
    def decrypt(self, ciphertext):
        for cipher in reversed(self.ciphers):
            ciphertext = cipher.decrypt(ciphertext)
        return ciphertext

class Challenge:
    @staticmethod
    def uwu(message):
        cipher_types = (SubstitutionCipher, VigenereCipher, TranspositionCipher)
        ciphers = []
        for _ in range(100):
            t = choice(cipher_types)
            if t is SubstitutionCipher:
                ciphers.append(SubstitutionCipher())
            elif t is VigenereCipher:
                ciphers.append(VigenereCipher(key_length=choice(range(1, len(message)+1))))
            else:
                ciphers.append(TranspositionCipher(key_length=len(message)))

        super_cipher = SuperCipher(ciphers)
        encrypted_message = super_cipher.encrypt(message)
        decrypted_message = super_cipher.decrypt(encrypted_message)
        assert decrypted_message == message, "Decryption failed"

        for round_num in range(0b01): # 0b01 = 11 * 16**2 + 1 = 2817 rounds
            c = input("c: ").strip()
            if len(c) == len(message) and all(ch in ascii_lowercase for ch in c):
                m = super_cipher.decrypt(c)
                print("m:", m)
            else:
                return -1

        print("ciphertext:", encrypted_message)
        return 0

    @staticmethod
    def main():
        message = "".join(choice(ascii_lowercase) for _ in range(randint(60, 80)))
        print("Length of the message:", len(message))

        for round_num in range(0x0b01): # 0 times 0b01 = 0, this loop does nothing
            ret = Challenge.uwu(message)
            if ret == -1:
                break
        
        guess = input("Message: ").strip()

        if guess == message:
            with open("flag.txt", "r") as f:
                flag = f.read().strip()
            print("Flag:", flag)
            print("UwU")
        else:
            print("Wrong answer.")
            print("Try harder!")

if __name__ == "__main__":
    Challenge.main()