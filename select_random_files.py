import os
import random
import shutil

source_folder = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/train_images'
source_label = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/train_masks'
destination_path = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/valid_images'
destination_label = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/valid_masks'

# Get a list of all files in the source folder
all_files = os.listdir(source_folder)

# Randomly select x images
selected_images = random.sample(all_files, 140)

# Move the selected images to the destination folder
for image in selected_images:
    # print(os.path.join(source_label,image[:-3]+'txt'))
    shutil.move(os.path.join(source_folder, image), destination_path)
    # shutil.move(os.path.join(source_label,image[:-3]+'txt'), destination_label)
    shutil.move(os.path.join(source_label, image), destination_label)
    print(os.path.join(source_folder, image), ' TO ', destination_path)
    print(os.path.join(source_label, image), ' TO ', destination_label)
