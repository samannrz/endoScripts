import os

import cv2
import numpy as np


def reColor(mask, color1=(128, 0, 0), color2=(100, 0, 0)):  # this function replaces color1 with color2 in mask
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == color1[0]) & (blue == color1[2]) & (green == color1[1])
    data[black_areas.T] = color2  # Transpose back needed
    return data


mask_path = '/data/projects/IncisionDeepLab/input/incision/Batch9-4/mask'
for mask in os.listdir(mask_path):
    image = cv2.imread(os.path.join(mask_path, mask))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(os.path.join(mask_path, mask), gray)
for i in range(gray.shape[0]):
 for j in range(gray.shape[1]):
     if gray[i,j]<75 and gray[i,j]>0:
        print (gray[i,j])
