import os
import shutil

import cv2
import numpy as np
from PIL import Image
from functions import createDIR

from overlay_mask import reColor

dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
        'incision.consensus': 4}

base_path = '/data/DATA/incision/'
orig_path1 = os.path.join(base_path, str(6))
orig_path2 = os.path.join(base_path, str(5))
savepath = os.path.join(base_path,'56')


if os.path.exists(savepath):
    shutil.rmtree(savepath)
createDIR(savepath)
createDIR(savepath, 'mask')
createDIR(savepath, 'image')
createDIR(os.path.join(savepath,'mask'), 'Treat')
createDIR(os.path.join(savepath,'mask'), 'Check')

orig_path_image1 = os.path.join(orig_path1, 'image')
orig_path_image2 = os.path.join(orig_path2, 'image')
path_mask_check1 = os.path.join(orig_path1, 'mask/Check/')
path_mask_check2 = os.path.join(orig_path2, 'mask/Check/')
path_mask_treat1 = os.path.join(orig_path1, 'mask/Treat/')
path_mask_treat2 = os.path.join(orig_path2, 'mask/Treat/')

images1 = os.listdir(os.path.join(orig_path1, 'image/'))
images2 = os.listdir(os.path.join(orig_path2, 'image/'))
images3 = os.listdir(os.path.join(base_path, str(4),'image'))

images_intersect = set(images1).intersection(set(images2)) - set(images3)
# Convert the resulting set to a list, if needed
images_intersect_list = list(images_intersect)

for name in images_intersect:
    print(name)
    orig_image = cv2.imread(os.path.join(orig_path_image1, name))
    height, width, _ = orig_image.shape
    if width == 853:
        width = 854
    if os.path.exists(os.path.join(path_mask_treat1, name)):
        t1 = cv2.imread(os.path.join(path_mask_treat1, name))
    else:
        t1 = np.zeros((height, width, 3), dtype=np.uint8)

    if os.path.exists(os.path.join(path_mask_treat2, name)):
        t2 = cv2.imread(os.path.join(path_mask_treat2, name))
    else:
        t2 = np.zeros((height, width, 3), dtype=np.uint8)

    if os.path.exists(os.path.join(path_mask_check1, name)):
        c1 = cv2.imread(os.path.join(path_mask_check1, name))
    else:
        c1 = np.zeros((height, width, 3), dtype=np.uint8)

    if os.path.exists(os.path.join(path_mask_check2, name)):
        c2 = cv2.imread(os.path.join(path_mask_check2, name))
    else:
        c2 = np.zeros((height, width, 3), dtype=np.uint8)

    mask_treat = cv2.bitwise_and(t1, t2)

    mask_check = cv2.bitwise_or(cv2.bitwise_or(t1, t2), cv2.bitwise_or(t1, c2))
    mask_check = cv2.bitwise_or(mask_check, cv2.bitwise_or(t2, c1))
    mask_check = cv2.bitwise_or(mask_check, cv2.bitwise_or(c2, c1))

    cv2.imwrite(os.path.join(savepath, 'mask/Treat', name), mask_treat)
    cv2.imwrite(os.path.join(savepath, 'mask/Check', name), mask_check)
    shutil.copy(os.path.join(orig_path_image1, name), os.path.join(savepath, 'image', name))

# from functions import find_missing_images
# # Call the function to find and copy missing images
# find_missing_images(orig_path_image1, os.path.join(savepath, 'image'))
# find_missing_images(orig_path_image2, os.path.join(savepath, 'image'))
#
# find_missing_images(path_mask_treat1, os.path.join(savepath, 'mask/Treat'))
# find_missing_images(path_mask_treat2, os.path.join(savepath, 'mask/Treat'))
#
# find_missing_images(path_mask_check1, os.path.join(savepath, 'mask/Check'))
# find_missing_images(path_mask_check2, os.path.join(savepath, 'mask/Check'))
