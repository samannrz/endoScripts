# in this version the consensensus of annottaors are also plot as heatmaps
import argparse

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math, os, cv2
from src.functions import createDIR,reColor

parser = argparse.ArgumentParser()
parser.add_argument('--batch', help = 'batch number')
parser.add_argument('--input',help = 'path of dest. folder')
args = parser.parse_args()
batch_num = args.batch
# from IncisionDataFolderCreation import batch_num
nb_ann = 2
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
        maskH_ju = initializeMask(image_orig.size)
        maskS_ju = initializeMask(image_orig.size)
        maskH_in = initializeMask(image_orig.size)
        maskS_in = initializeMask(image_orig.size)

        maskH_ju = Image.open(os.path.join(common_path, 'maskTreat_j.', images[i][:-4] + '.png'))
        maskS_ju = Image.open(os.path.join(common_path, 'maskCheck_j.', images[i][:-4] + '.png'))
        maskH_in = Image.open(os.path.join(common_path, 'maskTreat_in', images[i][:-4] + '.png'))
        maskS_in = Image.open(os.path.join(common_path, 'maskCheck_in', images[i][:-4] + '.png'))


        if draw_STAPLE:
            maskH_STAPLE = Image.open(os.path.join('/data/DATA/STAPLE/Batch210/mask/Treat', images[i][:]))
            maskS_STAPLE = Image.open(os.path.join('/data/DATA/STAPLE/Batch210/mask/Check', images[i][:]))
        #########################
        image_overlayed_ju = overlayMasks_incision(image_orig, maskH_ju, maskS_ju)
        image_overlayed_in = overlayMasks_incision(image_orig, maskH_in, maskS_in)

        if draw_STAPLE:
            image_overlayed_STAPLE = overlayMasks_incision(image_orig, maskH_STAPLE, maskS_STAPLE)


        ## Calculation of agreement images ##########

        maskH_ju_array = np.array(maskH_ju.convert('1'))
        maskH_in_array = np.array(maskH_in.convert('1'))


        maskS_ju_array = np.array(maskS_ju.convert('1'))
        maskS_in_array = np.array(maskS_in.convert('1'))

        Treat_rates[r, :] = calculate_agreements2(maskH_in, maskH_ju)
        Check_rates[r, :] = calculate_agreements2(maskS_in, maskS_ju)

        r += 1
        if not save_image:
            continue

        if batchstart:
            batchstart = False
            if j > math.floor(lenimg / batch_size) - 1:
                im3 = Image.new("RGB", (
                    2 * 1920 + 20,
                    2 * (lenimg % batch_size) * 1080 + space_height * (lenimg % batch_size)),
                                (255, 255, 255))
            else:
                im3 = Image.new("RGB", (
                    2 * 1920 + 20,
                    2 * batch_size * 1080 + space_height * (batch_size + 1)),
                                (255, 255, 255))

        if image_overlayed_ju.width < 1920:
            newsize = (1920, 1080)
            image_overlayed_ju = image_overlayed_ju.resize(newsize)
            image_overlayed_in = image_overlayed_in.resize(newsize)
            image_orig = image_orig.resize(newsize)

        WIDTH = image_orig.width
        HEIGHT = image_orig.height
        # Paste the images onto the white background
        if draw_machine_prediction:
            im3.paste(image_orig, (int(0.49 * WIDTH), hh + space_height))
        else:
            im3.paste(image_orig, (int(1 * WIDTH), hh + space_height))

        im3.paste(image_overlayed_ju, (0, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_in, (WIDTH + 10, hh + 2 * space_height + HEIGHT - 100))


        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("../../arial.ttf", 70)

        draw.text((1 / 2 * WIDTH, hh + space_height + HEIGHT),'Juniors: ', fill=(240, 60, 240), font=font)
        draw.text((3 / 2 * WIDTH + 10, hh + space_height + HEIGHT),'Experts: ', fill=(240, 60, 240), font=font)
        rr = 15

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
        cv2.imwrite(dest_folder + '/J_Batch' + str(int(batch_num)-2) + '-Comparison_consensus_juniors_seniors' + str(j + 1) + ".jpg",
                    cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))
batch_num = str(int(batch_num) -2)
print(Check_rates)
np.save('Rates_agreement/Check_rates_juniors_seniors'+str(batch_num)+'.npy', Check_rates)
np.save('Rates_agreement/Treat_rates_juniors_seniors'+str(batch_num)+'.npy', Treat_rates)

