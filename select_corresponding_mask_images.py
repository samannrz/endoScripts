import os
import shutil
def move_matching_files(imgDir, maskDir, destDir):
    os.makedirs(destDir, exist_ok=True)
    # Get the set of filenames in folder2 (without paths)
    files_in_images = set(os.listdir(imgDir))
    # List to keep track of moved files
    moved_files = []
    # Iterate through files in masks
    for filename in os.listdir(maskDir):
        # Check if the file name exists in images
        if filename in files_in_images:
            source_path = os.path.join(maskDir, filename)
            destination_path = os.path.join(destDir, filename)

            # Move the file to mask
            shutil.move(source_path, destination_path)
            moved_files.append(filename)

    return moved_files

moved_files = move_matching_files("/data/projects/IncisionDeepLab/input/incision/orig_data4/valid_images",
'/data/projects/IncisionDeepLab/input/incision/orig_data4/train_masks',
                                  '/data/projects/IncisionDeepLab/input/incision/orig_data4/valid_masks')
