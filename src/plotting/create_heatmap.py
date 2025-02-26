import os.path

import cv2
from overlay_mask import *
import numpy as np
common_path = 'annotationDatas/annotationData21'
image_dir = 'annotationDatas/annotationData21/image'
dest_folder = 'heatmap2/'
colors = ([0,0,128],[0,0,255],[0,128,0],[255,255,0],[255,165,0],[255,0,0])
colors = [
    [0, 0, 128],    # Dark Blue
    [0, 0, 255],    # Blue
    [0, 128, 0],    # Green
    [255, 255, 0],  # Yellow
    [255, 165, 0],  # Orange
    [255, 0, 0]     # Red
]
# for image_name in os.listdir(image_dir):
#     # Load the three black and white masks
#     mask1_dir = os.path.join(common_path,'maskTreat_ni')
#     mask2_dir = os.path.join(common_path,'maskTreat_Je')
#     mask3_dir = os.path.join(common_path,'maskTreat_Er')
#     mask4_dir = os.path.join(common_path,'maskTreat_eb')
#     mask5_dir = os.path.join(common_path,'maskTreat_gi')
#     mask6_dir = os.path.join(common_path,'maskTreat_fi')
#
#
#     mask1 = np.array(Image.open(os.path.join(mask1_dir, image_name)).convert('1'), dtype=np.uint8)
#     mask2 = np.array(Image.open(os.path.join(mask2_dir, image_name)).convert('1'), dtype=np.uint8)
#     mask3 = np.array(Image.open(os.path.join(mask3_dir, image_name)).convert('1'), dtype=np.uint8)
#     mask4 = np.array(Image.open(os.path.join(mask4_dir, image_name)).convert('1'), dtype=np.uint8)
#     mask5 = np.array(Image.open(os.path.join(mask5_dir, image_name)).convert('1'), dtype=np.uint8)
#     mask6 = np.array(Image.open(os.path.join(mask6_dir, image_name)).convert('1'), dtype=np.uint8)
#     # Create a new numpy array to represent the heatmap
#     heatmap = np.ones((mask1.shape[0], mask1.shape[1], 3))
#
#     # Loop over the pixels in the heatmap and assign a color based on the number of masks that have that pixel masked
#     for i in range(mask1.shape[0]):
#         for j in range(mask1.shape[1]):
#             num_masks = mask1[i, j] + mask2[i, j] + mask3[i, j] + mask4[i, j] + mask5[i, j] + mask6[i, j]
#             if num_masks == 0:
#                 heatmap[i, j] = [0,0,0]  # White color for unmasked pixels
#             elif num_masks == 1:
#                 heatmap[i, j] = colors[0]  # Yellow color for pixels masked in one image
#             elif num_masks == 2:
#                 heatmap[i, j] = colors[1]  # Orange color for pixels masked in two images
#             elif num_masks == 3:
#                 heatmap[i, j] = colors[2]  # Red color for pixels masked in all three images
#             elif num_masks == 4:
#                 heatmap[i, j] = colors[3]  # Red color for pixels masked in all three images
#             elif num_masks ==5:
#                 heatmap[i, j] = colors[4]  # Red color for pixels masked in all three images
#             else:
#                 heatmap[i, j] = colors[5]  # Red color for pixels masked in all three images
#
#
#
#     image_orig = Image.open(os.path.join(image_dir,image_name))
#     bg = image_orig.convert('RGB')
#     overlay = Image.fromarray(heatmap.astype('uint8'), 'RGB')
#     mask = overlay.convert('L')
#     mask = mask.point(lambda p: 90 if p > 2 else 0)  # if the point is white it is become transparent
#     bg.paste(overlay, None, mask)  # paste the overlay to image when a mask exists
#     bg.save(dest_folder + image_name)

import numpy as np
import matplotlib.pyplot as plt

# Define the heatmap colors
colors = [
    [80, 80, 178],  # Modified Dark Blue
    [80, 80, 255],  # Modified Blue
    [80, 255, 80],  # Modified Green
    [255, 255, 80], # Modified Yellow
    [255, 205, 80], # Modified Orange
    [255, 80, 80]   # Modified Red
]
colors = [
    tuple(colors[0]), tuple(colors[1]),tuple(colors[2]),tuple(colors[3]),tuple(colors[4]),tuple(colors[5])
]


# Define the percentages corresponding to each color
percentages = [16, 33, 50, 66, 83, 100]
color_array = [[colors[i]] for i in range(len(colors))]  # Each color in its own row

fig, ax = plt.subplots(figsize=(1.5, 12))  # Adjust figsize for better appearance
ax.imshow(color_array, aspect='auto')  # Use the 2D array of colors

# Hide ticks and labels
ax.set_xticks([])
ax.set_yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])

# Add percentages to each color
for i, percentage in enumerate(percentages):
    ax.text(0, i, f'{percentage}%', ha='center', va='center', color='black',fontsize=14)

# Save the figure
plt.savefig(os.path.join(dest_folder, 'color_bar.png'), bbox_inches='tight', dpi=300)