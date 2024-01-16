import os
import shutil

def find_missing_images(folder1, folder2):
    # Get the list of images in folder1 and folder2
    images_folder1 = set(os.listdir(folder1))
    images_folder2 = set(os.listdir(folder2))

    # Find the missing images
    missing_images = images_folder1 - images_folder2

    # Copy missing images from folder1 to folder2
    for image in missing_images:
        source_path = os.path.join(folder1, image)
        destination_path = os.path.join(folder2, image)
        shutil.copy2(source_path, destination_path)
        print(f"Copying {image} from {folder1} to {folder2}")

