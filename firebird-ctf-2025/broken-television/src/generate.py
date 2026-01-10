# Generate a small video of qr code

# Video dimension
h, w = 108 * 2, 192 * 2

# Number of frames
n_frames = 1000
import cv2
from Crypto.Cipher import AES
import numpy as np
from hashlib import sha256
from tqdm import tqdm
import qrcode

flag = "firebird{wh3n_w1ll_Th3_QR_C0d3_hIt_th3_c0rNeR}"

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=3,
    border=0,
)
qr.add_data(flag)
qr.make(fit=True)

img = qr.make_image(fill_color="black", back_color="white")
img.save("qr.png")

# Change img to numpy array
img = 255 - np.array(img) * 255
print(img)

# Create a black and white canvas, with only black or white color, no gray
# Randomize the color of the canvas
canvas = np.random.randint(0, 2, (h, w)) * 255

qr_pos = np.random.randint(0, h - img.shape[0]), np.random.randint(0, w - img.shape[1])

dx, dy = 1, 1
for i in tqdm(range(n_frames)):
    # Copy the qr code to the canvas

    canvas[0], canvas[1:-1], canvas[-1] = canvas[1], canvas[2:], canvas[0]

    canvas[
        qr_pos[0] : qr_pos[0] + img.shape[0], qr_pos[1] : qr_pos[1] + img.shape[1]
    ] ^= img

    # Save the frame
    cv2.imwrite(f"frames/frame_{i}.png", canvas)

    # Move the qr code
    qr_pos = qr_pos[0] + dx, qr_pos[1] + dy
    if qr_pos[0] + img.shape[0] >= h or qr_pos[0] <= 0:
        dx *= -1
    if qr_pos[1] + img.shape[1] >= w or qr_pos[1] <= 0:
        dy *= -1

# Combine the frames into a video
import os

os.system(
    f"ffmpeg -r 30 -i frames/frame_%d.png -c:v libx264 -vf fps=25 -pix_fmt yuv420p tv.mp4"
)
print("Done")
