import os
import shutil
import random

def move_images_with_single_file_groups(src_folder, dest_folder, num_to_move):
    """
    Moves N% of image files from src_folder to dest_folder, considering groups
    Args:
        src_folder (str): Path to the source folder containing image files.
        dest_folder (str): Path to the destination folder for selected images.
        percentage (float): Percentage of eligible single-file groups to move (0-100).

    Returns:
        None
    """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    # List all files in the source folder
    files = [f for f in os.listdir(src_folder) if os.path.isfile(os.path.join(src_folder, f))]

    # Group files by their "trimmed" filenames (minus the last 10 characters)
    trimmed_to_files = {}
    for file in files:
        trimmed_name = file[:-10]
        if trimmed_name not in trimmed_to_files:
            trimmed_to_files[trimmed_name] = []
        trimmed_to_files[trimmed_name].append(file)

    # Filter groups to keep only those with a single file
    single_file_groups = {k: v for k, v in trimmed_to_files.items() if len(v) == 1}

    # Calculate the number of single-file groups to move
    unique_trimmed_names = list(single_file_groups.keys())

    # Randomly select single-file groups to move
    selected_trimmed_names = random.sample(unique_trimmed_names, num_to_move)

    # Move files corresponding to the selected trimmed names
    for trimmed_name in selected_trimmed_names:
        file = single_file_groups[trimmed_name][0]  # There's only one file in these groups
        src_path = os.path.join(src_folder, file)
        dest_path = os.path.join(dest_folder, file)
        shutil.move(src_path, dest_path)

    print(f"Moved {num_to_move} single-file groups to {dest_folder}.")

move_images_with_single_file_groups('/data/projects/IncisionDeepLab/input/incision/orig_data4/train_images',
                                    "/data/projects/IncisionDeepLab/input/incision/orig_data4/test_images", 30)
##########################
##########################
##########################
