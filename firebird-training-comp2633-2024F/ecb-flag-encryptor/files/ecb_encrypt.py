import cv2
from Crypto.Cipher import AES
import numpy as np
from hashlib import sha256
from tqdm import tqdm
from secret import key, flag
import qrcode

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=16,
    border=1,
)
qr.add_data(flag)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")

img.save("qrcode.png")


def read_image(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    return image


class Encryptor:
    def __init__(self, key):
        self.cipher = AES.new(key, AES.MODE_ECB)
        self.used_ciphertext = set()

    def encrypt(self, message):
        message_bytes = bytes(message)
        encrypted_bytes = b""

        for i in tqdm(range(0, len(message_bytes), 16)):
            block = message_bytes[i : i + 16]
            ciphertext = self.cipher.encrypt(block)

            while ciphertext in self.used_ciphertext:
                ciphertext = sha256(ciphertext).digest()[:16]

            self.used_ciphertext.add(ciphertext)
            encrypted_bytes += ciphertext

        return encrypted_bytes


img = read_image("qrcode.png")
shape = img.shape
img = img.flatten()

img_bytes = bytes(img)

assert len(img_bytes) % 16 == 0

cipher = Encryptor(key)
encrypted = cipher.encrypt(img_bytes)
encrypted = np.array(list(encrypted))

encrypted = encrypted.reshape(shape)
cv2.imwrite("encrypted.png", encrypted)
