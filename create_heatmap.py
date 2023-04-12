import os.path

import cv2
from overlay_mask import *
import numpy as np
import matplotlib.pyplot as plt

# Load the three black and white masks
image_dir = 'annotationData/image'
mask1_dir = 'annotationData/maskCheckN'
mask2_dir = 'annotationData/maskCheckJ'
mask3_dir = 'annotationData/maskCheckG'
mask4_dir = 'annotationData/maskCheckF'
image_name = '2022-03-02_042629_VID001_11367_11595.mp4_00047.png'
dest_folder = 'heatmaps/'
mask1 = 1 - plt.imread(os.path.join(mask1_dir, image_name))
mask2 = 1 - plt.imread(os.path.join(mask2_dir, image_name))
mask3 = 1 - plt.imread(os.path.join(mask3_dir, image_name))
mask4 = 1 - plt.imread(os.path.join(mask4_dir, image_name))

# Create a new numpy array to represent the heatmap
heatmap = np.ones((mask1.shape[0], mask1.shape[1], 3))

# Loop over the pixels in the heatmap and assign a color based on the number of masks that have that pixel masked
for i in range(mask1.shape[0]):
    for j in range(mask1.shape[1]):
        num_masks = mask1[i, j] + mask2[i, j] + mask3[i, j] + mask4[i, j]
        if num_masks == 0:
            heatmap[i, j] = [255, 255, 255]  # White color for unmasked pixels
        elif num_masks == 1:
            heatmap[i, j] = [0, 0, 255]  # Yellow color for pixels masked in one image
        elif num_masks == 2:
            heatmap[i, j] = [0, 255, 0]  # Orange color for pixels masked in two images
        elif num_masks == 3:
            heatmap[i, j] = [255, 255, 0]  # Red color for pixels masked in all three images
        else:
            heatmap[i, j] = [255, 0, 0]  # Red color for pixels masked in all three images



image_orig = Image.open(os.path.join(image_dir,image_name))
bg = image_orig.convert('RGB')
overlay = Image.fromarray(heatmap.astype('uint8'), 'RGB')

mask = overlay.convert('L')
mask = mask.point(lambda p: 80 if p < 250 else 0)  # if the point is white it is become transparent
bg.paste(overlay, None, mask)  # paste the overlay to image when a mask exists
bg.save(dest_folder + image_name)
