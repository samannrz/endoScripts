import os
import shutil

def check_and_move_files(folder1, folder2, new_folder):
    # Create the new folder if it doesn't exist
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    # Get the list of files in folder2
    folder2_files = os.listdir(folder2)

    # Iterate through files in folder1
    for file1 in os.listdir(folder1):
        # Check if the file exists in folder2
        if file1 in folder2_files:
            # Move the file to the new folder
            shutil.move(os.path.join(folder1, file1), os.path.join(new_folder, file1))

# Paths to the folders
folder1 = "folder1"
folder2 = "folder2"
new_folder = "new"

# Call the function
check_and_move_files(folder1, folder2, new_folder)