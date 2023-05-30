from PIL import Image
import numpy as np


def overlayMask(image_orig, mask1, mask_color=(255, 0, 0)):
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, mask_color)  # change the mask color
    mask1 = overlay.convert('L')
    mask1 = mask1.point(lambda p: 80 if p < 250 else 0)  # if the point is white it is become transparent

    bg.paste(overlay, None, mask1)  # paste the overlay to image when a mask exists
    return bg


def reColor(mask, color1=(255, 255, 255), color2=(255, 0, 0)):  # this function replaces color1 with color2 in mask
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == color1[0]) & (blue == color1[2]) & (green == color1[1])
    data[black_areas.T] = color2  # Transpose back needed
    mask2 = Image.fromarray(data)
    return mask2


def main(original_image_path, mask_path):
    # Main:
    image_orig = Image.open(original_image_path)
    mask = Image.open(mask_path)
    # You can change the mask color by setting the mask_color parameter to a defined (r,g,b)
    o = overlayMask(image_orig, mask)
    o.show()
