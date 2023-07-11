import os
import random
import shutil

source_folder = '/data/projects/datasets/coco128-2023-06-28-2/images/train2017'
source_label = '/data/projects/datasets/coco128-2023-06-28-2/labels/train2017'
destination_path = '/data/projects/datasets/coco128-2023-06-28-2/images/valid'
destination_label = '/data/projects/datasets/coco128-2023-06-28-2/labels/valid'

# Get a list of all files in the source folder
all_files = os.listdir(source_folder)

# Randomly select 166 images
selected_images = random.sample(all_files, 340)

# Move the selected images to the destination folder
for image in selected_images:
    # print(os.path.join(source_label,image[:-3]+'txt'))
    shutil.move(os.path.join(source_folder,image), destination_path)
    shutil.move(os.path.join(source_label,image[:-3]+'txt'), destination_label)
    print(os.path.join(source_folder,image), ' TO ' , destination_path)
    print(os.path.join(source_label,image[:-3]+'txt'), ' TO ',destination_label)