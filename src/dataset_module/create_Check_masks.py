import os

import cv2
import numpy as np


def reColor_check(mask, color1=(128, 0, 0), color2=(100, 0, 0)):  # this function replaces color1 with color2 in mask
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == color1[0]) & (blue == color1[2]) & (green == color1[1])
    data[black_areas.T] = color2  # Transpose back needed
    return data

annotator = 6
mask_path = os.path.join('/data/DATA/annotator-consensus-deeplab/',str(annotator),'masks')  #the path to the 'annotator-consensus' folder
mask_path2='/data/DATA/annotator-consensus2/'
os.makedirs(os.path.join(mask_path2,str(annotator),'mask/Treat'),exist_ok=True)
os.makedirs(os.path.join(mask_path2,str(annotator),'mask/Check'),exist_ok=True)

for mask in os.listdir(mask_path):
    image = cv2.imread(os.path.join(mask_path, mask))
    mask2 = reColor_check(image,(0,128,0),(0,0,0))
    mask2 = reColor_check(mask2,(0,0,128),(255,255,255))
    cv2.imwrite(os.path.join(mask_path2,str(annotator),'mask/Treat',mask), mask2)

    image = cv2.imread(os.path.join(mask_path, mask))
    mask2 = reColor_check(image, (0, 128, 0), (255, 255, 255))
    mask2 = reColor_check(mask2, (0, 0, 128), (0, 0, 0))
    cv2.imwrite(os.path.join(mask_path2,str(annotator),'mask/Check',mask), mask2)

