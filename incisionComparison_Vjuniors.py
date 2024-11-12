# in this version the consensensus of annottaors are also plot as heatmaps
import argparse

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os

from functions import write_to_gsheet, createDIR
from overlay_mask import reColor

parser = argparse.ArgumentParser()
parser.add_argument('--batch', help = 'batch number')
parser.add_argument('--input',help = 'path of dest. folder')
args = parser.parse_args()
batch_num = args.batch
# from IncisionDataFolderCreation import batch_num
nb_ann = 3
common_path = args.input
dest_folder = 'ImgOut'

heatmap_creation=False
draw_machine_prediction = False
final_consensus = False
save_image = True
draw_STAPLE = False


print('YO')
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


images = os.listdir(common_path + '/image')
print(common_path + '/image')
createDIR('', dest_folder)
lenimg = len(images)
Treat_rates = np.zeros((lenimg, nb_ann * nb_ann))
Check_rates = np.zeros((lenimg, nb_ann * nb_ann))
r = 0
print('There are %d images' % lenimg)
batch_size = 4
space_height = 150
ep = 1e-15


def calculate_score(mask1, mask2):
    mask1_array = np.array(mask1.convert('1'))
    mask2_array = np.array(mask2.convert('1'))
    try:
        # score of Hard zones
        score = round((np.count_nonzero(mask2_array & mask1_array) / np.count_nonzero(
            mask2_array | mask1_array)) * 100, 2)
    except ZeroDivisionError:
        score = 100
    return score


def calculate_agreements(maskH_O, maskH_A, maskH_G, maskS_O, maskS_A, maskS_G):
    T1 = [calculate_score(maskH_O, maskH_O), calculate_score(maskH_O, maskH_A), calculate_score(maskH_O, maskH_G),

          calculate_score(maskH_A, maskH_O), calculate_score(maskH_A, maskH_A), calculate_score(maskH_A, maskH_G),

          calculate_score(maskH_G, maskH_O), calculate_score(maskH_G, maskH_A), calculate_score(maskH_G, maskH_G),
          ]
    C1 = [calculate_score(maskS_O, maskH_O), calculate_score(maskS_O, maskS_A), calculate_score(maskS_O, maskS_G),

          calculate_score(maskS_A, maskH_O), calculate_score(maskS_A, maskS_A), calculate_score(maskS_A, maskS_G),

          calculate_score(maskS_G, maskH_O), calculate_score(maskS_G, maskS_A), calculate_score(maskS_G, maskS_G),
          ]
    return T1, C1

def calculate_agreements2(*args):
    agreements = []
    for mask1 in args:
        for mask2 in args:
            agreement_score = calculate_score(mask1, mask2)
            agreements.append(agreement_score)
    return agreements



for j in range(math.ceil(lenimg / batch_size)):
    counter = 1
    batchstart = True
    hh = 0
    print('File: '+str(j))

    for i in range(j * batch_size, (j + 1) * batch_size):
        if i > lenimg - 1:
            break
        print(os.path.join(common_path, 'image', images[i]))
        image_orig = Image.open(os.path.join(common_path, 'image', images[i]))
        maskH_O = initializeMask(image_orig.size)
        maskS_O = initializeMask(image_orig.size)
        maskH_G = initializeMask(image_orig.size)
        maskS_G = initializeMask(image_orig.size)
        maskH_A = initializeMask(image_orig.size)
        maskS_A = initializeMask(image_orig.size)


        maskH_O = Image.open(os.path.join(common_path, 'maskTreat_os', images[i][:-4] + '.png'))
        maskS_O = Image.open(os.path.join(common_path, 'maskCheck_os', images[i][:-4] + '.png'))
        maskH_A = Image.open(os.path.join(common_path, 'maskTreat_an', images[i][:-4] + '.png'))
        maskS_A = Image.open(os.path.join(common_path, 'maskCheck_an', images[i][:-4] + '.png'))
        maskH_G = Image.open(os.path.join(common_path, 'maskTreat_gr', images[i][:-4] + '.png'))
        maskS_G = Image.open(os.path.join(common_path, 'maskCheck_gr', images[i][:-4] + '.png'))

        if draw_STAPLE:
            maskH_STAPLE = Image.open(os.path.join('/data/DATA/STAPLE/Batch210/mask/Treat', images[i][:]))
            maskS_STAPLE = Image.open(os.path.join('/data/DATA/STAPLE/Batch210/mask/Check', images[i][:]))
        #########################
        image_overlayed_O = overlayMasks_incision(image_orig, maskH_O, maskS_O)
        image_overlayed_A = overlayMasks_incision(image_orig, maskH_A, maskS_A)
        image_overlayed_G = overlayMasks_incision(image_orig, maskH_G, maskS_G)

        if draw_STAPLE:
            image_overlayed_STAPLE = overlayMasks_incision(image_orig, maskH_STAPLE, maskS_STAPLE)


        ## Calculation of agreement images ##########

        maskH_O_array = np.array(maskH_O.convert('1'))
        maskH_A_array = np.array(maskH_A.convert('1'))
        maskH_G_array = np.array(maskH_G.convert('1'))


        maskS_O_array = np.array(maskS_O.convert('1'))
        maskS_A_array = np.array(maskS_A.convert('1'))
        maskS_G_array = np.array(maskS_G.convert('1'))

        if heatmap_creation:
            heatmap_Treat = create_heatmap(maskH_O_array, maskH_A_array, maskH_G_array, 'red')
            heatmap_Check = create_heatmap(
                maskS_O_array, maskS_A_array, maskS_G_array, 'red')

            dst = cv2.cvtColor(np.uint8(heatmap_Treat), cv2.COLOR_BGR2RGB)
            cv2.imwrite('ahmap.png', dst)

            overlay = Image.fromarray(heatmap_Treat.astype('uint8'), 'RGB')
            bg_treat = image_orig.convert('RGB')
            mask = overlay.convert('L')
            mask = mask.point(lambda p: 200 if p < 250 else 0)  # if the point is white it is become transparent
            bg_treat.paste(overlay, None, mask)  # paste the overlay to image when a mask exists

            overlay = Image.fromarray(heatmap_Check.astype('uint8'), 'RGB')
            bg_check = image_orig.convert('RGB')
            mask = overlay.convert('L')
            mask = mask.point(lambda p: 200 if p < 250 else 0)  # if the point is white it is become transparent
            bg_check.paste(overlay, None, mask)  # paste the overlay to image when a mask exists
            bg_treat.save('ztreat.png')
            bg_check.save('zcheck.png')

        # score_Treat = ref_score(maskH_O_array, maskH_A_array, maskH_G_array, maskH_F_array, maskH_ER_array,
        #                         maskH_EB_array)
        # score_Check = ref_score(maskS_O_array, maskS_A_array, maskS_G_array, maskS_F_array, maskS_ER_array,
        #                         maskS_EB_array)

        # print(score_Treat)
        # print(score_Check)
        #############################

        #Treat_rates[r, :] = calculate_agreements2(maskH_O, maskH_A, maskH_G)
        #Check_rates[r, :] = calculate_agreements2(maskS_O, maskS_A, maskS_G)
        r += 1
        if not save_image:
            continue

        if batchstart:
            batchstart = False
            if j > math.floor(lenimg / batch_size) - 1:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    2 * (lenimg % batch_size) * 1080 + space_height * (lenimg % batch_size)),
                                (255, 255, 255))
            else:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    2 * batch_size * 1080 + space_height * (batch_size + 1)),
                                (255, 255, 255))

        if image_overlayed_O.width < 1920:
            newsize = (1920, 1080)
            image_overlayed_O = image_overlayed_O.resize(newsize)
            image_overlayed_A = image_overlayed_A.resize(newsize)
            image_overlayed_G = image_overlayed_G.resize(newsize)

            if draw_STAPLE:
                image_overlayed_STAPLE = image_overlayed_O.resize(newsize)



            image_orig = image_orig.resize(newsize)

        WIDTH = image_orig.width
        HEIGHT = image_orig.height
        # Paste the images onto the white background
        if draw_machine_prediction:
            im3.paste(image_orig, (int(0.49 * WIDTH), hh + space_height))
        else:
            im3.paste(image_orig, (int(1 * WIDTH), hh + space_height))

        im3.paste(image_overlayed_O, (0, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_A, (WIDTH + 10, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_G, (2 * WIDTH + 20, hh + 2 * space_height + HEIGHT - 100))

        if draw_STAPLE:
            im3.paste(image_overlayed_STAPLE, (2*WIDTH + 20, hh + 4 * space_height + 3 * HEIGHT - 300))
        if final_consensus:
            image_cons = Image.open(os.path.join(final_consensus_path, images[i]))
            im3.paste(image_cons.resize((1920, 1080)), (2 * WIDTH + 20, hh + 4 * space_height + 3 * HEIGHT - 300))

        if draw_machine_prediction:
            image_machine = Image.open(os.path.join(machine_path, images[i]))
            im3.paste(image_machine.resize((1920, 1080)), (round(1.51 * WIDTH), hh + space_height))

        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("arial.ttf", 70)

        draw.text((1 / 2 * WIDTH, hh + space_height + HEIGHT),'Oscar: ', fill=(240, 60, 240), font=font)
        draw.text((3 / 2 * WIDTH + 10, hh + space_height + HEIGHT),'Anne-sofie: ', fill=(240, 60, 240), font=font)
        draw.text((5 / 2 * WIDTH + 20, hh + space_height + HEIGHT),'Gry: ' , fill=(240, 60, 240), font=font)
        #draw.text((1 / 2 * WIDTH, hh + space_height + 2 * HEIGHT + 50), 'Filippo: '+str(score_Treat[3])+', '+str(score_Check[3]), fill=(240, 60, 240), font=font)

        if draw_STAPLE:
            draw.text((5 / 2 * WIDTH + 20, hh + space_height + 3 * HEIGHT + 100), 'Suggestion by STAPLE',
                      fill=(240, 60, 240),
                      font=font)
        rr = 15

        if final_consensus:
            draw.text((5 / 2 * WIDTH + 20, hh + space_height + 3 * HEIGHT + 100), 'FINAL Consensus',
                      fill=(240, 60, 240), font=font)

        # Draw the text on the image
        imagename = images[i][:-4]

        namevid, _, frnumber = imagename.rpartition('_')
        draw.text((0 / 2 * WIDTH, hh + 100 + int(0 * HEIGHT)), namevid + '_' + frnumber, fill=(0, 0, 0), font=font)
        space_height = 150

        hh = hh + 2 * HEIGHT + space_height + 30

        counter += 1

        imagename = images[i][:-4]
        namevid, _, frnumber = imagename.rpartition('_')

    if save_image:
        cv2.imwrite(dest_folder + '/J_Batch' + str(int(batch_num)-2) + '-Comparison' + str(j + 1) + ".jpg",
                    cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))
np.save('Rates_agreement/Check_rates_j'+str(batch_num)+'.npy', Check_rates)
np.save('Rates_agreement/Treat_rates_j'+str(batch_num)+'.npy', Treat_rates)

