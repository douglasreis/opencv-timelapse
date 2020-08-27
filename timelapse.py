import requests
import numpy as np
import cv2

filenames = ["1.jpg", "2.jpg", "3.jpg"]
columns = []

for i, filename in enumerate(filenames):
    img: np.array = cv2.imread(f"p/{filename}")
    height: int = len(img)
    width: int = len(img[0])
    column_start = 2 * i
    column_end = 2 * i + 2
    print(f"filename: {filename}, height: {height}, width: {width}, {column_start}-{column_end}")
    column = img[0:height, column_start:column_end]
    columns.append(column)

matrix = [[] for _ in range(height)]

for row_idx in range(height):
    row = []
    for col_idx in range(len(columns)):
        pixels = columns[col_idx][row_idx]
        matrix[row_idx] += list(pixels)

new_img = np.array([np.array(list(row)) for row in matrix])
cv2.imwrite('output.jpg', new_img)


# import cv2

# vid = cv2.VideoCapture('./assets/key.mov')
# frames = []
# success = 1
# count = 0
# speed = 8

# while success:
#     success, image = vid.read()
#     if(count % speed == 0):
#         frames.append(image)
#     count += 1

# writer = cv2.VideoWriter('./output/tl.mp4', cv2.VideoWriter_fourcc(*"MP4V"), 29.98, (1280, 720))

# for frame in frames:
#     writer.write(frame)
# writer.release()