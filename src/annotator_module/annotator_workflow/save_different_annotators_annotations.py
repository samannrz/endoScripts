'''
it takes the path of the saved annotationData (in the format given as the output pf incisiondataFolderCreation.py),
and saves in the destination folder all the annotations of hte annotators in this format:
IMAGE_NAME_i.png, where i is specific to one annotator

Args:
    common_path: the path of the folder where annotations are located
    dest_folder: The path in which you want to save the annotations
'''
import os
import shutil
from PIL import Image
from src.functions import overlayMasks_incision

common_path = 'annotationDatas/annotationData7'
dest_folder = '/data/DATA/TEST_save_diff_annot'

annotators = {
    "Nicolas": ("maskTreat_ni", "maskCheck_ni"),
    "Jean Luc": ("maskTreat_Je", "maskCheck_Je"),
    "Giuseppe": ("maskTreat_gi", "maskCheck_gi"),
    "Filippo": ("maskTreat_fi", "maskCheck_fi"),
    "Consensus": ("maskTreat_in", "maskCheck_in")
}
def save_different_annotations(common_path,dest_folder):
    # Function to create an empty mask
    def initialize_mask(size):
        return Image.new(mode="RGBA", size=size, color="black")

    # Function to safely load masks
    def load_image(image_path, zone_type, annotator, image_name):
        try:
            return Image.open(image_path)
        except FileNotFoundError:
            print(f"There is no {zone_type} Zone on {annotator}'s annot on {image_name}")
            return initialize_mask((0, 0))  # Return an empty mask to avoid None errors

    # Ensure destination folder exists
    os.makedirs(dest_folder, exist_ok=True)

    # Get all images
    images = os.listdir(os.path.join(common_path, 'image'))
    print(f'There are {len(images)} images')

    for image_name in images:
        base_name = image_name[:-4] + ".png"
        image_orig = Image.open(os.path.join(common_path, 'image', image_name))
        print(base_name)
        # Initialize masks for all annotators
        masks_hard = {}
        masks_security = {}

        for annotator, (hard_zone_folder, security_zone_folder) in annotators.items():
            masks_hard[annotator] = load_image(os.path.join(common_path, hard_zone_folder, base_name), "Treat", annotator, image_name)
            masks_security[annotator] = load_image(os.path.join(common_path, security_zone_folder, base_name), "Check", annotator, image_name)
        # Create overlayed images
        overlayed_images = [
            overlayMasks_incision(image_orig, masks_hard["Nicolas"], masks_security["Nicolas"]),
            overlayMasks_incision(image_orig, masks_hard["Jean Luc"], masks_security["Jean Luc"]),
            overlayMasks_incision(image_orig, masks_hard["Giuseppe"], masks_security["Giuseppe"]),
            overlayMasks_incision(image_orig, masks_hard["Filippo"], masks_security["Filippo"]),
            overlayMasks_incision(image_orig, masks_hard["Consensus"], masks_security["Consensus"])
        ]

        # Construct new image names
        namevid, _, frnumber = image_name.rpartition('_')
        print(f'Writing images to {dest_folder}/{namevid}_{frnumber}_i.png')

        # Save overlayed images with a loop
        for idx, img in enumerate(overlayed_images, start=1):
            img.save(os.path.join(dest_folder, f'{namevid}_{frnumber}_{idx}.png'))

        # Copy original image as reference
        shutil.copy(os.path.join(common_path, 'image', image_name), os.path.join(dest_folder, f'{namevid}_{frnumber}_0.png'))

if __name__ == '__main__':
    save_different_annotations(common_path,dest_folder)