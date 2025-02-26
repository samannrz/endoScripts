import os
import random
import shutil

source_folder = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/train_images'
source_label = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/train_masks'
destination_path = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/valid_images'
destination_label = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/valid_masks'

# Get a list of all files in the source folder
all_files = os.listdir(source_folder)

try:
    # Create directories if they don't exist
    os.makedirs(destination_path)
    print(f"Directories created at: {destination_path}")
except FileExistsError:
    print(f"Directories already exist at: {destination_path}")

try:
    # Create directories if they don't exist
    os.makedirs(destination_label)
    print(f"Directories created at: {destination_label}")
except FileExistsError:
    print(f"Directories already exist at: {destination_label}")


# Randomly select x images
selected_images = random.sample(all_files, 170)

# Move the selected images to the destination folder
for image in selected_images:
    # print(os.path.join(source_label,image[:-3]+'txt'))
    shutil.move(os.path.join(source_folder, image), destination_path)
    # shutil.move(os.path.join(source_label,image[:-3]+'txt'), destination_label)
    shutil.move(os.path.join(source_label, image), destination_label)
    print(os.path.join(source_folder, image), ' TO ', destination_path)
    print(os.path.join(source_label, image), ' TO ', destination_label)
