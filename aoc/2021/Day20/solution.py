from pathlib import Path
import os
import copy
import numpy as np
from scipy.ndimage import correlate

entry_file = Path(os.path.abspath(__file__)).parent / "entry.txt"
example_file = Path(os.path.abspath(__file__)).parent / "example.txt"

with entry_file.open("r") as f:
    entries = f.readlines()

for i in range(len(entries)):
    if entries[i][-1] == '\n':
        entries[i] = entries[i][:-1]

optimization = [0 if c == "." else 1 for c in entries[0]]

size_x = len(entries[2])
size_y = len(entries[2:])

max_size = 5

even_image = np.zeros((size_x*max_size, size_y * max_size), dtype=np.uint16)
odd_image = np.ones((size_x*max_size, size_y * max_size), dtype=np.uint16) * optimization[0]
filter = np.array([[256, 128, 64], [32, 16, 8], [4, 2, 1]], dtype=np.uint16)

start = (size_x * (max_size // 2) , size_y * (max_size // 2))
end = (start[0] + size_x, start[1] + size_y)

for i in range(size_x):
    for j in range(size_y):
        even_image[start[0] + i, start[1] + j] = 0 if entries[2 + i][j] == "." else 1

def print_image(i, s, e):
    for x in range(e[0]-s[0]):
        for y in range(e[1]-s[1]):
            print("#" if i[s[0]+x,s[1]+y] == 1 else " ", end='')
        print()
    print()

# print_image(image, start, end)

nb_passes = 50
for iter in range(nb_passes):
    if iter == 2:
        image = even_image if nb_passes % 2 == 0 else odd_image
        print_image(image, start, end)

        print("First answer:", np.sum(image, dtype=np.uint64))

    # Enhance the image
    start = (start[0] - 1, start[1] - 1)
    end = (end[0] + 1, end[1] + 1)
    image = even_image if iter % 2 == 0 else odd_image
    other_image = even_image if iter % 2 == 1 else odd_image
    if i == 0 or optimization[0] == 0:
        constant = 0
    else:
        constant = optimization[-1] if iter % 2 == 0 else optimization[0]

    temp = correlate(image[start[0]:end[0],start[1]:end[1]], filter, mode="constant", cval=constant)
    for i in range(end[0] - start[0]):
        for j in range(end[1] - start[1]):
            image[start[0]+i,start[1]+j] = optimization[temp[i,j]]
            other_image[start[0]+i,start[1]+j] = optimization[temp[i,j]]

image = even_image if nb_passes % 2 == 0 else odd_image
print_image(image, start, end)

print("Second answer:", np.sum(image, dtype=np.uint64))