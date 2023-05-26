import os
import shutil

import numpy as np
from PIL import Image

from overlay_mask import reColor

orig_path = '/data/DATA/DELPHI_incision/'
dest_path_orig = '/data/projects/DeeplabV3/input/incision/orig_data/train_images'
dest_path_mask = '/data/projects/DeeplabV3/input/incision/orig_data/train_masks'

# moving original images
orig_path_image = orig_path + 'image'
for image in os.listdir(orig_path_image):
    shutil.copy(os.path.join(orig_path_image, image), os.path.join(dest_path_orig, image))
def replaceColor(mask, color1, color2):
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace (leaves alpha values alone...)
    black_areas = (red == color1[0]) & (blue == color1[2]) & (green == color1[1])
    data[black_areas.T] = color2  # Transpose back needed
    mask2 = Image.fromarray(data)
    return mask2

# moving masks
path_mask_check = os.path.join(orig_path, 'maskCheckI')
for mask_check in os.listdir(path_mask_check):
    mask = Image.open(os.path.join(path_mask_check, mask_check))
    mask = mask.convert('RGB')
    mask = replaceColor(mask, (0, 0, 0), (0, 128, 0))
    mask = replaceColor(mask, (255, 255, 255), (0, 0, 0))
    mask.save(os.path.join(dest_path_mask, mask_check))
#
path_mask_treat = os.path.join(orig_path, 'maskTreatI')




for mask_treat in os.listdir(path_mask_treat):
    mask = Image.open(os.path.join(path_mask_treat, mask_treat))
    mask = mask.convert('RGB')
    mask = replaceColor(mask, (0, 0, 0), (128, 0, 0))
    mask = replaceColor(mask, (255, 255, 255), (0, 0, 0))

    if os.path.exists(os.path.join(dest_path_mask, mask_treat)):
        mask_old = Image.open(os.path.join(dest_path_mask, mask_treat))
        mask_old = mask_old.convert('RGB')


        # Replace (128,128,0) with (128,0,0)
        data1 = np.array(mask)  # "data" is a height x width x 4 numpy array
        data2 = np.array(mask_old)  # "data" is a height x width x 4 numpy array
        data = data1 + data2
        red, green, blue = data.T  # Temporarily unpack the bands for readability
        # for i in range(len(red)):
        #     for j in range(len(red[i])):
        #         if red[i][j] != 255 and  red[i][j] != 254:
        #             print(red[i][j], green[i][j])
        two_colored_areas = (red == 128) & (blue == 0) & (green == 128)
        data[two_colored_areas.T] = (128, 0, 0)  # Transpose back neede

        mask = Image.fromarray(data)
    mask.save(os.path.join(dest_path_mask, mask_treat))


