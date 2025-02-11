import os
import shutil


def copy_folders(starting_With, path_src, path_dest):
    # Make sure the destination path exists
    if not os.path.exists(path_dest):
        os.makedirs(path_dest)

    # Loop through all directories in the source path
    for folder_name in os.listdir(path_src):
        folder_path = os.path.join(path_src, folder_name)

        # Check if it's a directory and starts with the given string
        if os.path.isdir(folder_path) and folder_name.startswith(starting_With):
            # Copy the folder to the destination path
            dest_folder = os.path.join(path_dest, folder_name)
            shutil.copytree(folder_path, dest_folder)
            print(f"Copied: {folder_name}")


# Example usage:
CLASS = 'Treat'
batch_num = 14
starting_With = 'mask'+CLASS  # Replace with your prefix
path_src = "annotationDatas/annotationData"+ '2'+str(batch_num)  # Replace with your source directory
path_dest = '/data/projects/STAPLE-develop/staple/gt_vols/'+CLASS  # Replace with your destination directory

copy_folders(starting_With, path_src, path_dest)