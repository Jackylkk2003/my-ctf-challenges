# Split tv.mp4 into frames

import cv2

vidcap = cv2.VideoCapture("tv.mp4")
success, image = vidcap.read()

count = 0
while success:
    cv2.imwrite(f"frames/frame_{count}.png", image)
    success, image = vidcap.read()
    print("Read a new frame: ", success)
    count += 1

print("Done")

# Xor frame 0 and frame 1
import numpy as np

frame0 = cv2.imread("frames/frame_0.png", cv2.IMREAD_GRAYSCALE)
frame1 = cv2.imread("frames/frame_1.png", cv2.IMREAD_GRAYSCALE)

frame0[0], frame0[1:-1], frame0[-1] = frame0[1], frame0[2:], frame0[0]

xor = frame0 ^ frame1
cv2.imwrite("xor.png", xor)
