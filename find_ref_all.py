import os.path

import cv2
from overlay_mask import *
import numpy as np
import matplotlib.pyplot as plt
ni_score=[]
je_score=[]
gi_score=[]
fi_score=[]
co_score=[]
ma_score=[]
er_score=[]
eb_score=[]

for which_class in ['Treat','Check']:
    # Load the three black and white masks
    image_name = 'bsp1_GY_20230601_054_VID001_trim1.mp4_00189.png'

    print(image_name)

    image_dir = 'annotationData26/image'
    mask1_dir = 'annotationData26/mask'+which_class+'_ni'
    mask2_dir = 'annotationData26/mask'+which_class+'_Je'
    mask3_dir = 'annotationData26/mask'+which_class+'_gi'
    mask4_dir = 'annotationData26/mask'+which_class+'_fi'
    mask5_dir = 'annotationData26/mask'+which_class+'_er'
    mask6_dir = 'annotationData26/mask' + which_class + '_eb'
    mask_consensus_dir = 'annotationData26/mask' + which_class + '_in'
    # mask_machine_dir = '/data/DATA/Incision_predictions/Batch8-9/all_data/mask/'+which_class
    # mask_machine_dir = '/Users/saman/Documents/data/DATA/incision/Batch22-model1-21/mask/'+which_class

    # image_name = 'FCF1_GY_20230127_059_VID001_trim1.mp4_00083.png'
    dest_folder = 'heatmap2/'
    mask1 = plt.imread(os.path.join(mask1_dir, image_name))
    mask1 = cv2.imread(os.path.join(mask1_dir, image_name), 0) / 255
    print(type(mask1))
    print(mask1.dtype)

    mask2 = cv2.imread(os.path.join(mask2_dir, image_name), 0) / 255
    mask3 = cv2.imread(os.path.join(mask3_dir, image_name), 0) / 255
    mask4 = cv2.imread(os.path.join(mask4_dir, image_name), 0) / 255
    mask5 = cv2.imread(os.path.join(mask5_dir, image_name), 0) / 255
    mask6 = cv2.imread(os.path.join(mask6_dir, image_name), 0) / 255
    mask_consensus = cv2.imread(os.path.join(mask_consensus_dir, image_name), 0) / 255
    # mask_machine = cv2.imread(os.path.join(mask_machine_dir, image_name), 0) / 255


    # Create a new numpy array to represent the heatmap
    heatmap = np.ones((mask1.shape[0], mask1.shape[1], 3))

    # Loop over the pixels in the heatmap and assign a color based on the number of masks that have that pixel masked
    for i in range(mask1.shape[0]):
        for j in range(mask1.shape[1]):

            num_masks = mask1[i, j] + mask2[i, j] + mask3[i, j] + mask4[i, j]
            if num_masks == 0:
                heatmap[i, j] = [255, 255, 255]  # White color for unmasked pixels
            elif num_masks == 1:
                heatmap[i, j] = [0, 0, 255]  # Yellow color for pixels masked in one image
            elif num_masks == 2:
                heatmap[i, j] = [0, 255, 0]  # Orange color for pixels masked in two images
            elif num_masks == 3:
                heatmap[i, j] = [255, 255, 0]  # Red color for pixels masked in all three images
            else:
                heatmap[i, j] = [255, 0, 0]  # Red color for pixels masked in all three images

    image_orig = Image.open(os.path.join(image_dir, image_name))
    bg = image_orig.convert('RGB')
    overlay = Image.fromarray(heatmap.astype('uint8'), 'RGB')

    mask = overlay.convert('L')
    mask = mask.point(lambda p: 80 if p < 250 else 0)  # if the point is white it is become transparent
    bg.paste(overlay, None, mask)  # paste the overlay to image when a mask exists
    # bg.save(dest_folder + image_name)
    #####################################
    ref = mask1 + mask2 + mask4+ mask5 + mask6
    ref = cv2.normalize(ref, None, 0, 1, cv2.NORM_MINMAX)
    mask1 = cv2.normalize(mask1, None, 0, 1, cv2.NORM_MINMAX)
    mask2 = cv2.normalize(mask2, None, 0, 1, cv2.NORM_MINMAX)
    mask3 = cv2.normalize(mask3, None, 0, 1, cv2.NORM_MINMAX)
    mask4 = cv2.normalize(mask4, None, 0, 1, cv2.NORM_MINMAX)
    mask5 = cv2.normalize(mask5, None, 0, 1, cv2.NORM_MINMAX)
    mask6 = cv2.normalize(mask6, None, 0, 1, cv2.NORM_MINMAX)
    mask_consensus = cv2.normalize(mask_consensus, None, 0, 1, cv2.NORM_MINMAX)
    # mask_machine = cv2.normalize(mask_machine, None, 0, 1, cv2.NORM_MINMAX)

    ref = ref.flatten()/np.linalg.norm(ref.flatten())
    mask1 = mask1.flatten()/np.linalg.norm(mask1.flatten())
    mask2 = mask2.flatten()/np.linalg.norm(mask2.flatten())
    mask3 = mask3.flatten()/np.linalg.norm(mask3.flatten())
    mask4 = mask4.flatten()/np.linalg.norm(mask4.flatten())
    mask5 = mask5.flatten()/np.linalg.norm(mask5.flatten())
    mask6 = mask6.flatten()/np.linalg.norm(mask6.flatten())
    mask_consensus = mask_consensus.flatten()/np.linalg.norm(mask_consensus.flatten())
    # mask_machine = mask_machine.flatten()/np.linalg.norm(mask_machine.flatten())



    # ref = (ref - np.mean(ref.flatten())) / np.linalg.norm(ref.flatten())
    # mask2 = (mask2 - np.mean(mask2.flatten())) / np.linalg.norm(mask2.flatten())
    # mask3 = (mask3 - np.mean(mask3.flatten())) / np.linalg.norm(mask3.flatten())
    # mask4 = (mask4 - np.mean(mask4.flatten())) / np.linalg.norm(mask4.flatten())
    # mask5 = (mask5 - np.mean(mask5.flatten())) / np.linalg.norm(mask5.flatten())

    ni_score.append(np.dot(ref.flatten(), mask1.flatten()))
    je_score.append(np.dot(ref.flatten(), mask2.flatten()))
    gi_score.append(np.dot(ref.flatten(), mask3.flatten()))
    fi_score.append(np.dot(ref.flatten(), mask4.flatten()))
    er_score.append(np.dot(ref.flatten(), mask5.flatten()))
    eb_score.append(np.dot(ref.flatten(), mask6.flatten()))
    co_score.append(np.dot(ref.flatten(), mask_consensus.flatten()))
    # ma_score.append(np.dot(ref.flatten(), mask_machine.flatten()))


#####################################vvv
########################################
image_orig = Image.open(os.path.join(image_dir, image_name))
def overlayMasks_incision(image_orig, mask1, mask2):
    # This function takes the two masks and overlay them to the image_orig
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, color2=(255, 0, 0))

    overlay2 = mask2.convert('RGB')
    overlay2 = reColor(overlay2, color2=(0, 255, 0))

    # Replace (255,255,0) with (255,0,0)
    data1 = np.array(overlay)  # "data" is a height x width x 4 numpy array
    data2 = np.array(overlay2)  # "data" is a height x width x 4 numpy array
    data = data1 + data2
    red, green, blue = data.T  # Temporarily unpack the bands for readability
    two_colored_areas = (red == 255) & (blue == 0) & (green == 255)
    data[two_colored_areas.T] = (255, 0, 0)  # Transpose back neede
    overlay_final = Image.fromarray(data)
    mask_final = overlay_final.convert('L')
    mask_final = mask_final.point(lambda p: 60 if p > 5 else 0)

    bg.paste(overlay_final, None, mask_final)
    return bg


def initializeMask(size):
    a = Image.new(mode="RGBA", size=(size[0], size[1]), color="black")
    return a
from PIL import Image, ImageDraw, ImageFont

hh = 20
space_height = 150

maskH_N = initializeMask(image_orig.size)
maskS_N = initializeMask(image_orig.size)
maskH_F = initializeMask(image_orig.size)
maskS_F = initializeMask(image_orig.size)
maskH_G = initializeMask(image_orig.size)
maskS_G = initializeMask(image_orig.size)
maskH_J = initializeMask(image_orig.size)
maskS_J = initializeMask(image_orig.size)
maskH_C = initializeMask(image_orig.size)
maskS_C = initializeMask(image_orig.size)

maskH_N = Image.open(os.path.join('annotationData26', 'maskTreat_ni', image_name[:-4] + '.png'))
maskS_N = Image.open(os.path.join('annotationData26', 'maskCheck_ni', image_name[:-4] + '.png'))
maskH_J = Image.open(os.path.join('annotationData26', 'maskTreat_Je', image_name[:-4] + '.png'))
maskS_J = Image.open(os.path.join('annotationData26', 'maskCheck_Je', image_name[:-4] + '.png'))
maskH_G = Image.open(os.path.join('annotationData26', 'maskTreat_gi', image_name[:-4] + '.png'))
maskS_G = Image.open(os.path.join('annotationData26', 'maskCheck_gi', image_name[:-4] + '.png'))
maskH_F = Image.open(os.path.join('annotationData26', 'maskTreat_fi', image_name[:-4] + '.png'))
maskS_F = Image.open(os.path.join('annotationData26', 'maskCheck_fi', image_name[:-4] + '.png'))
maskH_C = Image.open(os.path.join('annotationData26', 'maskTreat_in', image_name[:-4] + '.png'))
maskS_C = Image.open(os.path.join('annotationData26', 'maskCheck_in', image_name[:-4] + '.png'))
maskH_ER = Image.open(os.path.join('annotationData26', 'maskTreat_er', image_name[:-4] + '.png'))
maskS_ER = Image.open(os.path.join('annotationData26', 'maskCheck_er', image_name[:-4] + '.png'))
maskH_EB = Image.open(os.path.join('annotationData26', 'maskTreat_eb', image_name[:-4] + '.png'))
maskS_EB = Image.open(os.path.join('annotationData26', 'maskCheck_eb', image_name[:-4] + '.png'))

#########################
image_overlayed_N = overlayMasks_incision(image_orig, maskH_N, maskS_N)
image_overlayed_J = overlayMasks_incision(image_orig, maskH_J, maskS_J)
image_overlayed_G = overlayMasks_incision(image_orig, maskH_G, maskS_G)
image_overlayed_F = overlayMasks_incision(image_orig, maskH_F, maskS_F)
image_overlayed_C = overlayMasks_incision(image_orig, maskH_C, maskS_C)
image_overlayed_ER = overlayMasks_incision(image_orig, maskH_ER, maskS_ER)
image_overlayed_EB = overlayMasks_incision(image_orig, maskH_EB, maskS_EB)
# image_overlayed_M = Image.open(os.path.join(mask_machine_dir[:-10]+'final/', image_name))
im3 = Image.new("RGB", (
    3 * 1920,
    4 * 1080+400),
                (255, 255, 255))
if image_overlayed_N.width < 1920:
    newsize = (1920, 1080)
    image_overlayed_N = image_overlayed_N.resize(newsize)
    image_overlayed_J = image_overlayed_J.resize(newsize)
    image_overlayed_G = image_overlayed_G.resize(newsize)
    image_overlayed_F = image_overlayed_F.resize(newsize)
    image_overlayed_C = image_overlayed_C.resize(newsize)
    image_overlayed_ER = image_overlayed_ER.resize(newsize)
    image_overlayed_EB = image_overlayed_EB.resize(newsize)
    # image_overlayed_M = image_overlayed_M.resize(newsize)
    image_orig = image_orig.resize(newsize)

WIDTH = image_orig.width
HEIGHT = image_orig.height
# Paste the images onto the white background

im3.paste(image_orig, (int(1 * WIDTH), hh + 0))
im3.paste(image_overlayed_N, (0, hh + 1 * space_height + HEIGHT - 50))
im3.paste(image_overlayed_J, (WIDTH + 10, hh + 1 * space_height + HEIGHT - 50))
im3.paste(image_overlayed_G, (2 * WIDTH + 20, hh + 1 * space_height + HEIGHT - 50))
im3.paste(image_overlayed_F, (0, hh + 2 * space_height + 2 * HEIGHT - 50))
im3.paste(image_overlayed_ER, (WIDTH + 10, hh + 2 * space_height + 2 * HEIGHT - 50))
im3.paste(image_overlayed_EB, (2 * WIDTH + 20, hh + 2 * space_height + 2 * HEIGHT - 50))
im3.paste(image_overlayed_C, (0, hh + 3 * space_height + 3 * HEIGHT - 50))
im3.paste(image_overlayed_M, (WIDTH + 10, hh + 3 * space_height + 3 * HEIGHT - 50))

draw = ImageDraw.Draw(im3)
font = ImageFont.truetype("arial.ttf", 100)

draw.text((1 / 3 * WIDTH, hh + 0 + HEIGHT), 'Nicolas : '+str(round(ni_score[0],2))+' , '+str(round(ni_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((4 / 3 * WIDTH, hh + 0 + HEIGHT), 'Jean : '+str(round(je_score[0],2))+' , '+str(round(je_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((7 / 3 * WIDTH, hh + 0 + HEIGHT), 'Guiseppe : '+str(round(gi_score[0],2))+' , '+str(round(gi_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((1 / 3 * WIDTH, hh + 0 + 2 * HEIGHT + 130), 'Filippo : '+str(round(fi_score[0],2))+' , '+str(round(fi_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((4 / 3 * WIDTH, hh + 0 + 2 * HEIGHT + 130), 'Ervin : '+str(round(er_score[0],2))+' , '+str(round(er_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((7 / 3 * WIDTH, hh + 0 + 2 * HEIGHT + 130), 'Ebbe : '+str(round(eb_score[0],2))+' , '+str(round(eb_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((1 / 3 * WIDTH, hh + 0 + 3 * HEIGHT + 290), 'Consensus : '+str(round(co_score[0],2))+' , '+str(round(co_score[1],2)), fill=(0, 0, 0), font=font)
draw.text((4 / 3 * WIDTH, hh + 0 + 3 * HEIGHT + 290), 'Machine : '+str(round(ma_score[0],2))+' , '+str(round(ma_score[1],2)), fill=(0, 0, 0), font=font)


# Draw the text on the image
imagename = image_name[:-4]

namevid, _, frnumber = imagename.rpartition('_')
font = ImageFont.truetype("arial.ttf", 70)

draw.text((0 / 2 * WIDTH, hh + int(0 * HEIGHT)), namevid + '_' + frnumber, fill=(0, 0, 0), font=font)
space_height = 150

hh = hh + 3 * HEIGHT + space_height + 30

imagename = image_name[:-4]
namevid, _, frnumber = imagename.rpartition('_')

cv2.imwrite(dest_folder + image_name + ".jpg",
            cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))
