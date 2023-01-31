from PIL import Image
import numpy as np
def overlayMask(image_orig,mask1):
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, (255, 0, 0)) #I change the mask to red
    mask1 = overlay.convert('L')
    mask1 = mask1.point(lambda p: 80 if p < 225 else 0) #if the point is white it is become transparent

    bg.paste(overlay, None, mask1) #paste the overlay to image when a mask exists
    return bg
def reColor(mask,color):
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    data[black_areas.T] = color  # Transpose back needed
    mask2 = Image.fromarray(data)
    return mask2

# Main:
image_orig = Image.open('/media/saman/data/PycharmProjects/endoDetection/Dataset/image/2021-12-06_004908_VID001_Trim.mp4_59.jpg')
maskH_N = Image.open('/media/saman/data/PycharmProjects/endoDetection/Dataset/maskHardF/2021-12-06_004908_VID001_Trim.mp4_59.png')
o = overlayMask(image_orig, maskH_N)
o.show()
