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
            shutil.copy(os.path.join(folder1, file1), os.path.join(new_folder, file1))
            print(os.path.join(new_folder[:-6],'mask/Treat', file1))
            shutil.copy(os.path.join(folder1[:-6],'mask/Treat', file1), os.path.join(new_folder[:-6],'mask/Treat', file1))
            shutil.copy(os.path.join(folder1[:-6], 'mask/Check', file1),
                        os.path.join(new_folder[:-6], 'mask/Check', file1))


# Paths to the folders
folder1 = "/data/DATA/incision/4/image"
folder2 = "/data/DATA/incision/10/image"
new_folder = "/data/DATA/incision/4of10/image"

# Call the function
check_and_move_files(folder1, folder2, new_folder)