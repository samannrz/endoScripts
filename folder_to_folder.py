import os
import shutil

def check_and_move_files(folder1, folder2):
    # Create the new folder if it doesn't exist

    # Get the list of files in folder2
    folder2_files = os.listdir(folder2)

    # Iterate through files in folder1
    for file1 in os.listdir(folder1):
        # Check if the file exists in folder2
        if file1 not in folder2_files:
            # Move the file to the new folder
            # os.remove(os.path.join(folder1, file1))
            print('action')

# Paths to the folders
folder2 = "/data/projects/IncisionDeepLab/input/inference_data_1-28/test_with_consensus/test_images"
folder1 = "/data/DATA/annotator-consensus/0/mask/Check"

# Call the function
check_and_move_files(folder1, folder2)