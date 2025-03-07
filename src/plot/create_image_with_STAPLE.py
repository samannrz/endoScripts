import os
from PIL import Image

def combine_images(path1, path2, output_path):
    """
    Combines images from two directories side by side and saves them in another directory.

    :param path1: Path to the first directory containing images.
    :param path2: Path to the second directory containing images.
    :param output_path: Path to save the combined images.
    """
    # Ensure the output directory exists
    os.makedirs(output_path, exist_ok=True)

    # Get list of image names (common in both directories)
    images1 = set(os.listdir(path1))
    images2 = set(os.listdir(path2))
    common_images = images1.intersection(images2)

    if not common_images:
        print("No matching images found in the directories.")
        return

    for image_name in common_images:
        try:
            # Open images from both directories
            img1 = Image.open(os.path.join(path1, image_name))
            img2 = Image.open(os.path.join(path2, image_name))

            # Ensure both images have the same height
            if img1.size[1] != img2.size[1]:
                new_height = min(img1.size[1], img2.size[1])
                img1 = img1.resize((int(img1.size[0] * new_height / img1.size[1]), new_height))
                img2 = img2.resize((int(img2.size[0] * new_height / img2.size[1]), new_height))

            # Create a new image with combined width
            combined_width = img1.size[0] + img2.size[0] + 20
            combined_image = Image.new("RGB", (combined_width, img1.size[1]))

            # Paste the images side by side
            combined_image.paste(img1, (0, 0))
            combined_image.paste(img2, (img1.size[0], 0))

            # Save the combined image to the output directory
            combined_image.save(os.path.join(output_path, image_name))

            print(f"Combined image saved: {image_name}")

        except Exception as e:
            print(f"Error processing {image_name}: {e}")

# Example usage
path1 = 'annotationDatas/annotationData214/image'
path2 = '/data/DATA/STAPLE/Batch214/final'
output_path = "/data/DATA/temp-staple-image"

combine_images(path1, path2, output_path)
