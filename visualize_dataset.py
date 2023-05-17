# Author: Yanan Liu
# Date: 17/05/2023 14:45
# Location:
# Version:
# Description: Enter a brief description here.

import cv2
import numpy as np
import matplotlib.pyplot as plt

def read_grasping_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.readlines()
    rectangles = []
    for i in range(0, len(lines), 4):
        points = [list(map(float, line.split())) for line in lines[i:i+4]]
        rectangles.append(points)
    return rectangles

# replace these with your actual paths
rgb_image_path = 'data/bosch_obj/0/2.png'
grasping_file_path = 'data/bosch_obj/0/2_annotations_pos.txt'
grasping_file_path_neg = 'data/bosch_obj/0/2_annotations_neg.txt'

rgb_image = cv2.imread(rgb_image_path)
rgb_image = cv2.cvtColor(rgb_image, cv2.COLOR_BGR2RGB)  # OpenCV reads images in BGR format by default
rectangles = read_grasping_file(grasping_file_path)
rectangles_neg = read_grasping_file(grasping_file_path_neg)

for rect in rectangles:
    pts = np.array(rect, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(rgb_image, [pts], True, (0, 255, 0), 3)

for rect in rectangles_neg:
    pts = np.array(rect, dtype=np.int32).reshape((-1, 1, 2))
    cv2.polylines(rgb_image, [pts], True, (255, 0, 0), 3)


plt.imshow(rgb_image)
plt.show()
