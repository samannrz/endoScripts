# The images in folder1, if are also existing in folder 2, are copied to a new folder
import os
import shutil

def check_and_move_files(folder1, folder2, new_folder):
    # Create the new folder if it doesn't exist
    if not os.path.exists(new_folder):
        os.makedirs(new_folder)

    folder2_files = os.listdir(folder2)
    count = 1
    for file1 in os.listdir(folder1):
        if file1 in folder2_files:
            if not file1 in os.listdir(new_folder):
                # Move the file to the new folder
                shutil.copy(os.path.join(folder1, file1), os.path.join(new_folder, file1))
                print(os.path.join(new_folder[:-6],'mask/Treat', file1))
                shutil.copy(os.path.join(folder1[:-6],'mask/Treat', file1), os.path.join(new_folder[:-6],'mask/Treat', file1))
                shutil.copy(os.path.join(folder1[:-6], 'mask/Check', file1),
                            os.path.join(new_folder[:-6], 'mask/Check', file1))
                print(count)
                count +=1


# Paths to the folders
folder1 = "/data/DATA/orig_data_expert_consensus/image"
folder2 = "/data/projects/IncisionDeepLab/input/incision/orig_data4/train_images"
new_folder = "/data/DATA/orig_data_junior_consensus/image"

# Call the function
check_and_move_files(folder1, folder2, new_folder)