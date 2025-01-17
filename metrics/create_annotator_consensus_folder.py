import os
import shutil


def copy_files(base_source, base_dest, test_images_folder):

    test_images = {os.path.basename(f) for f in os.listdir(test_images_folder) if
                   os.path.isfile(os.path.join(test_images_folder, f))}

    # Define source and destination paths
    source_image_folder = os.path.join(base_source, "image")
    source_mask_treat_folder = os.path.join(base_source, "mask", "Treat")
    source_mask_check_folder = os.path.join(base_source, "mask", "Check")

    dest_image_folder = os.path.join(base_dest, "image")
    dest_mask_treat_folder = os.path.join(base_dest, "mask", "Treat")
    dest_mask_check_folder = os.path.join(base_dest, "mask", "Check")

    # Ensure destination directories exist
    os.makedirs(dest_image_folder, exist_ok=True)
    os.makedirs(dest_mask_treat_folder, exist_ok=True)
    os.makedirs(dest_mask_check_folder, exist_ok=True)

    # Helper function to copy matching files
    def copy_matching_files(source_folder, dest_folder):
        for filename in os.listdir(source_folder):
            if filename in test_images:
                shutil.copy(os.path.join(source_folder, filename), os.path.join(dest_folder, filename))

    # Copy matching files
    print("Copying images...")
    copy_matching_files(source_image_folder, dest_image_folder)

    print("Copying Treat masks...")
    copy_matching_files(source_mask_treat_folder, dest_mask_treat_folder)

    print("Copying Check masks...")
    copy_matching_files(source_mask_check_folder, dest_mask_check_folder)

    print("Done copying files.")


# Example usage
annotator = 0
base_source = os.path.join('/data/DATA/incision/',str(annotator))  # the path to the annotator (all data) folder
base_dest =os.path.join('/data/DATA/annotator-consensus/',str(annotator))  #the path to the 'annotator-consensus' folder
test_images_folder = '/data/projects/IncisionDeepLab/input/incision/orig_data4/test_images'  #the path to the 'test_images' folder

copy_files(base_source, base_dest, test_images_folder)
