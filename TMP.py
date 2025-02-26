# The images in folder1, if are also existing in folder 2, are copied to a new folder
import os
import shutil

def check_and_move_files(folder1, folder2):
    for file in os.listdir(folder1):
        if file not in os.listdir(folder2):
            # Move the file to the 2
            # shutil.copy(os.path.join(folder1, file), os.path.join(folder2, file))
            print(os.path.join(folder2[:-6],'mask/Treat', file))
            # shutil.copy(os.path.join(folder1[:-6],'mask/Treat', file1), os.path.join(folder2[:-6],'mask/Treat', file1))
            # shutil.copy(os.path.join(folder1[:-6], 'mask/Check', file1),
            #             os.path.join(folder2[:-6], 'mask/Check', file1))


# Paths to the folders
folder2 = "/data/projects/IncisionDeepLab/input/incision/orig_data_expert_consensus/mask/Treat"
folder1 = "/data/projects/IncisionDeepLab/input/incision/orig_data4/train_images"

# Call the function
check_and_move_files(folder1, folder2)