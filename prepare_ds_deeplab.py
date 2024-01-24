import os
import shutil

import numpy as np
from PIL import Image

from overlay_mask import reColor
dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
        'incision.consensus': 4}
annotator = 'all'
orig_path = '/data/DATA/incision/'+str(annotator) + '/'
# orig_path = 'annotationData/'
dest_path_orig = '/data/projects/IncisionDeepLab/input/incision/orig_data'+str(annotator)+'/train_images'
dest_path_mask = '/data/projects/IncisionDeepLab/input/incision/orig_data'+str(annotator)+'/train_masks'
# dest_path_orig = '/data/projects/IncisionDeepLab/input/incision/Batch10-4/image'
# dest_path_mask = '/data/projects/IncisionDeepLab/input/incision/Batch10-4/mask'

# moving original images
orig_path_image = orig_path + 'image'
for image in os.listdir(orig_path_image):
    # print(os.path.join(dest_path_orig, image))
    shutil.copy(os.path.join(orig_path_image, image), os.path.join(dest_path_orig, image))


# moving masks
path_mask_check = os.path.join(orig_path, 'mask/Check/')
for mask_check in os.listdir(path_mask_check):
    mask = Image.open(os.path.join(path_mask_check, mask_check))
    mask = mask.convert('RGB')
    mask = reColor(mask, color2=(0, 128, 0))
    mask.save(os.path.join(dest_path_mask, mask_check))
#
path_mask_treat = os.path.join(orig_path, 'mask/Treat/')



for mask_treat in os.listdir(path_mask_treat):
    mask = Image.open(os.path.join(path_mask_treat, mask_treat))
    mask = mask.convert('RGB')
    mask = reColor(mask, color2=(128, 0, 0))

    if os.path.exists(os.path.join(dest_path_mask, mask_treat)):
        mask_old = Image.open(os.path.join(dest_path_mask, mask_treat))
        mask_old = mask_old.convert('RGB')


        # Replace (128,128,0) with (128,0,0)
        data1 = np.array(mask)  # "data" is a height x width x 4 numpy array
        data2 = np.array(mask_old)  # "data" is a height x width x 4 numpy array
        data = data1 + data2
        red, green, blue = data.T  # Temporarily unpack the bands for readability
        two_colored_areas = (red == 128) & (blue == 0) & (green == 128)
        data[two_colored_areas.T] = (128, 0, 0)  # Transpose back neede

        mask = Image.fromarray(data)
    mask.save(os.path.join(dest_path_mask, mask_treat))

