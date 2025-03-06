import argparse

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os
from functions import createDIR, reColor

parser = argparse.ArgumentParser()
parser.add_argument('--batch', help = 'batch number')
parser.add_argument('--input',help = 'path of dest. folder')
args = parser.parse_args()
batch_num = args.batch
common_path = args.input
### Parameters to be defined ###
nb_ann = 6
N_ROWS = 3 # number of rows for visualization of annotations

machine_path = '/data/DATA/Incision_predictions/Batch211-FasterViT/final'
path_mask_STAPLE = '/data/DATA/STAPLE/Batch' + str(batch_num)+'/mask/'
# final_consensus_path = '/Users/saman/Documents/data/DATA/incision/4/Batch24/final'

dest_folder = 'ImgOut2'

heatmap_creation=False
draw_machine_prediction = False
final_consensus = False
save_image = True
draw_STAPLE = False
###
vidname=[]

def get_STAPLE_vote(SHEET_ID):
    import pygsheets

    # Authenticate using the credentials.json file
    gc = pygsheets.authorize(service_file='../../../data/keycode/my-gpysheets-3d8d13442005.json')

    # Open the Google Sheet
    spreadsheet = gc.open_by_key(SHEET_ID)  # Replace with your spreadsheet ID
    worksheet = spreadsheet.sheet1  # Open the first sheet

    # Get data from row 1 (names) and row 7 (numbers)
    names = worksheet.get_row(1)  # Get data from row 1
    numbers = worksheet.get_row(6)  # Get data from row 7

    # Create a dictionary from the two rows
    dictionary = {name: int(number) for name, number in zip(names, numbers) if name and number}

    # Print the resulting dictionary
    return dictionary

if draw_STAPLE:
    dict_STAPLE = get_STAPLE_vote('1EExamxHJh5Sg3pIWagfLk1Da6xe-TT43F3V-G5dqHuU')
    print(dict_STAPLE)

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
createDIR('', dest_folder)
lenimg = len(images)
Treat_rates = np.zeros((lenimg, nb_ann * nb_ann))
Check_rates = np.zeros((lenimg, nb_ann * nb_ann))
Merge_rates = np.zeros((lenimg, nb_ann * nb_ann))

r = 0
print('There are %d images' % lenimg)
batch_size = 2
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


def calculate_agreements(maskH_N, maskH_J, maskH_G, maskH_F, maskH_ER, maskH_EB, maskS_N, maskS_J, maskS_G, maskS_F,
                         maskS_ER, maskS_EB):
    T1 = [calculate_score(maskH_N, maskH_N), calculate_score(maskH_N, maskH_J), calculate_score(maskH_N, maskH_G),
          calculate_score(maskH_N, maskH_F), calculate_score(maskH_N, maskH_ER), calculate_score(maskH_N, maskH_EB),

          calculate_score(maskH_J, maskH_N), calculate_score(maskH_J, maskH_J), calculate_score(maskH_J, maskH_G),
          calculate_score(maskH_J, maskH_F), calculate_score(maskH_J, maskH_ER), calculate_score(maskH_J, maskH_EB),

          calculate_score(maskH_G, maskH_N), calculate_score(maskH_G, maskH_J), calculate_score(maskH_G, maskH_G),
          calculate_score(maskH_G, maskH_F), calculate_score(maskH_G, maskH_ER), calculate_score(maskH_G, maskH_EB),

          calculate_score(maskH_F, maskH_N), calculate_score(maskH_F, maskH_J), calculate_score(maskH_F, maskH_G),
          calculate_score(maskH_F, maskH_F), calculate_score(maskH_F, maskH_ER), calculate_score(maskH_F, maskH_EB),

          calculate_score(maskH_ER, maskH_N), calculate_score(maskH_ER, maskH_J), calculate_score(maskH_ER, maskH_G),
          calculate_score(maskH_ER, maskH_F), calculate_score(maskH_ER, maskH_ER), calculate_score(maskH_ER, maskH_EB),

          calculate_score(maskH_EB, maskH_N), calculate_score(maskH_EB, maskH_J), calculate_score(maskH_EB, maskH_G),
          calculate_score(maskH_EB, maskH_F), calculate_score(maskH_EB, maskH_ER), calculate_score(maskH_EB, maskH_EB),
          ]
    C1 = [calculate_score(maskS_N, maskS_N), calculate_score(maskS_N, maskS_J), calculate_score(maskS_N, maskS_G),
          calculate_score(maskS_N, maskS_F), calculate_score(maskS_N, maskS_ER), calculate_score(maskS_N, maskS_EB),

          calculate_score(maskS_J, maskS_N), calculate_score(maskS_J, maskS_J), calculate_score(maskS_J, maskS_G),
          calculate_score(maskS_J, maskS_F), calculate_score(maskS_J, maskS_ER), calculate_score(maskS_J, maskS_EB),

          calculate_score(maskS_G, maskS_N), calculate_score(maskS_G, maskS_J), calculate_score(maskS_G, maskS_G),
          calculate_score(maskS_G, maskS_F), calculate_score(maskS_G, maskS_ER), calculate_score(maskS_G, maskS_EB),

          calculate_score(maskS_F, maskS_N), calculate_score(maskS_F, maskS_J), calculate_score(maskS_F, maskS_G),
          calculate_score(maskS_F, maskS_F), calculate_score(maskS_F, maskS_ER), calculate_score(maskS_F, maskS_EB),

          calculate_score(maskS_ER, maskS_N), calculate_score(maskS_ER, maskS_J), calculate_score(maskS_ER, maskS_G),
          calculate_score(maskS_ER, maskS_F), calculate_score(maskS_ER, maskS_ER), calculate_score(maskS_ER, maskS_EB),

          calculate_score(maskS_EB, maskS_N), calculate_score(maskS_EB, maskS_J), calculate_score(maskS_EB, maskS_G),
          calculate_score(maskS_EB, maskS_F), calculate_score(maskS_EB, maskS_ER), calculate_score(maskS_EB, maskS_EB),
          ]
    return T1, C1

def calculate_agreements2(*args):
    agreements = []
    for mask1 in args:
        for mask2 in args:
            agreement_score = calculate_score(mask1, mask2)
            agreements.append(agreement_score)
    return agreements
def create_heatmap(mask1, mask2, mask3, mask4, mask5, mask6, color_theme='red'):
    num_masks = 0
    heatmap = np.ones((mask1.shape[0], mask1.shape[1], 3))
    if color_theme == 'red':
        colors = [[255, 255, 255], [210, 241, 250], [222, 250, 205], [253, 231, 118], [245, 182, 94],
                  [237, 133, 69], [164, 14, 76]]
    else:
        colors = [[255, 255, 255], [247, 242, 198], [218, 243, 251], [229, 220, 249], [216, 246, 228], [184, 206, 169],
                  [90, 101, 83], ]
    for i in range(mask1.shape[0]):
        for j in range(mask1.shape[1]):
            num_masks = sum([mask1[i, j], mask2[i, j], mask3[i, j], mask4[i, j], mask5[i, j], mask6[i, j]])
            if num_masks == 0:
                # print(i,j)
                heatmap[i, j] = colors[0]  # White color for unmasked pixels
            elif num_masks == nb_ann-5:
                heatmap[i, j] = colors[1]  # Blue color for pixels masked in one image
            elif num_masks == nb_ann - 4:
                heatmap[i, j] = colors[2]  # green color for pixels masked in two images
            elif num_masks == nb_ann - 3:
                heatmap[i, j] = colors[3]  # Orange color for pixels masked in all three images
            elif num_masks == nb_ann - 2:
                heatmap[i, j] = colors[4]  # Yellow color for pixels masked in all three images
            elif num_masks == nb_ann - 1:
                heatmap[i, j] = colors[5]  # Red color for pixels masked in all three images
            elif num_masks == nb_ann:
                heatmap[i, j] = colors[6]  # Red color for pixels masked in all three images
    return heatmap


def ref_score(*args):
    co = 0
    score = []
    for maskk in args:
        maskk = maskk.astype(float)
        if co == 0:
            ref = maskk
            co += 1
        else:
            ref = ref + maskk

    for maskk in args:
        maskk = maskk.astype(float)
        ref_one_out = ref - maskk
        maskk = cv2.normalize(maskk, None, 0, 1, cv2.NORM_MINMAX)
        maskk = maskk.flatten() / np.linalg.norm(maskk.flatten())

        ref_norm = cv2.normalize(ref_one_out, None, 0, 1, cv2.NORM_MINMAX)
        ref_norm = ref_norm.flatten() / np.linalg.norm(ref_norm.flatten())
        score.append(round(np.dot(ref_norm.flatten(), maskk.flatten()), 2))
        # print(np.dot(ref.flatten(), mask.flatten()))
    return score


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
        maskH_N = initializeMask(image_orig.size)
        maskS_N = initializeMask(image_orig.size)
        maskH_F = initializeMask(image_orig.size)
        maskS_F = initializeMask(image_orig.size)
        maskH_G = initializeMask(image_orig.size)
        maskS_G = initializeMask(image_orig.size)
        maskH_J = initializeMask(image_orig.size)
        maskS_J = initializeMask(image_orig.size)
        maskH_ER = initializeMask(image_orig.size)
        maskS_ER = initializeMask(image_orig.size)
        maskH_EB = initializeMask(image_orig.size)
        maskS_EB = initializeMask(image_orig.size)

        maskH_N = Image.open(os.path.join(common_path, 'maskTreat_ni', images[i][:-4] + '.png'))
        maskS_N = Image.open(os.path.join(common_path, 'maskCheck_ni', images[i][:-4] + '.png'))
        maskH_J = Image.open(os.path.join(common_path, 'maskTreat_Je', images[i][:-4] + '.png'))
        maskS_J = Image.open(os.path.join(common_path, 'maskCheck_Je', images[i][:-4] + '.png'))
        maskH_G = Image.open(os.path.join(common_path, 'maskTreat_gi', images[i][:-4] + '.png'))
        maskS_G = Image.open(os.path.join(common_path, 'maskCheck_gi', images[i][:-4] + '.png'))
        #maskH_F = Image.open(os.path.join(common_path, 'maskTreat_fi', images[i][:-4] + '.png'))
        #maskS_F = Image.open(os.path.join(common_path, 'maskCheck_fi', images[i][:-4] + '.png'))
        maskH_ER = Image.open(os.path.join(common_path, 'maskTreat_Er', images[i][:-4] + '.png'))
        maskS_ER = Image.open(os.path.join(common_path, 'maskCheck_Er', images[i][:-4] + '.png'))
        maskH_EB = Image.open(os.path.join(common_path, 'maskTreat_eb', images[i][:-4] + '.png'))
        maskS_EB = Image.open(os.path.join(common_path, 'maskCheck_eb', images[i][:-4] + '.png'))
        if draw_STAPLE:
            maskH_STAPLE = Image.open(os.path.join(path_mask_STAPLE,'Treat', images[i][:]))
            maskS_STAPLE = Image.open(os.path.join(path_mask_STAPLE,'Check', images[i][:]))
        #########################
        image_overlayed_N = overlayMasks_incision(image_orig, maskH_N, maskS_N)
        image_overlayed_J = overlayMasks_incision(image_orig, maskH_J, maskS_J)
        image_overlayed_G = overlayMasks_incision(image_orig, maskH_G, maskS_G)
        image_overlayed_F = overlayMasks_incision(image_orig, maskH_F, maskS_F)
        image_overlayed_ER = overlayMasks_incision(image_orig, maskH_ER, maskS_ER)
        image_overlayed_EB = overlayMasks_incision(image_orig, maskH_EB, maskS_EB)
        if draw_STAPLE:
            image_overlayed_STAPLE = overlayMasks_incision(image_orig, maskH_STAPLE, maskS_STAPLE)


        ## Calculation of agreement images ##########

        maskH_N_array = np.array(maskH_N.convert('1'))
        maskH_J_array = np.array(maskH_J.convert('1'))
        maskH_G_array = np.array(maskH_G.convert('1'))
        maskH_F_array = np.array(maskH_F.convert('1'))
        maskH_ER_array = np.array(maskH_ER.convert('1'))
        maskH_EB_array = np.array(maskH_EB.convert('1'))

        maskS_N_array = np.array(maskS_N.convert('1'))
        maskS_J_array = np.array(maskS_J.convert('1'))
        maskS_G_array = np.array(maskS_G.convert('1'))
        maskS_F_array = np.array(maskS_F.convert('1'))
        maskS_ER_array = np.array(maskS_ER.convert('1'))
        maskS_EB_array = np.array(maskS_EB.convert('1'))

        maskmerge_N_array = np.maximum(maskS_N_array,maskH_N_array)
        maskmerge_J_array = np.maximum(maskS_J_array,maskH_J_array)
        maskmerge_G_array = np.maximum(maskS_G_array,maskH_G_array)
        maskmerge_F_array = np.maximum(maskS_F_array,maskH_F_array)
        maskmerge_ER_array = np.maximum(maskS_ER_array,maskH_ER_array)
        maskmerge_EB_array = np.maximum(maskS_EB_array,maskH_EB_array)
        #############################
        # Treat_rates[r, :] = calculate_agreements2(maskH_N, maskH_J, maskH_G, maskH_F,maskH_ER, maskH_EB)
        # Check_rates[r, :] = calculate_agreements2(maskS_N, maskS_J, maskS_G, maskS_F,maskS_ER, maskS_EB)
        # Merge_rates[r, :] = calculate_agreements2(Image.fromarray(maskmerge_N_array), Image.fromarray(maskmerge_J_array),
        #                                           Image.fromarray(maskmerge_G_array), Image.fromarray(maskmerge_F_array),
        #                                           Image.fromarray(maskmerge_ER_array), Image.fromarray(maskmerge_EB_array))

        r += 1
        if not save_image:
            continue

        if batchstart:
            batchstart = False
            if j > math.floor(lenimg / batch_size) - 1:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    N_ROWS * (lenimg % batch_size) * 1080 + space_height * (lenimg % batch_size)),
                                (255, 255, 255))
            else:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    N_ROWS * batch_size * 1080 + space_height * (batch_size + 1)),
                                (255, 255, 255))

        if image_overlayed_N.width < 1920:
            newsize = (1920, 1080)
            image_overlayed_N = image_overlayed_N.resize(newsize)
            image_overlayed_J = image_overlayed_J.resize(newsize)
            image_overlayed_G = image_overlayed_G.resize(newsize)
            image_overlayed_F = image_overlayed_F.resize(newsize)
            image_overlayed_EB = image_overlayed_EB.resize(newsize)
            image_overlayed_ER = image_overlayed_ER.resize(newsize)
            if draw_STAPLE:
                image_overlayed_STAPLE = image_overlayed_STAPLE.resize(newsize)

            image_orig = image_orig.resize(newsize)

        WIDTH = image_orig.width
        HEIGHT = image_orig.height
        # Paste the images onto the white background
        if draw_machine_prediction:
            im3.paste(image_orig, (int(0.49 * WIDTH), hh + space_height))
        else:
            im3.paste(image_orig, (int(1 * WIDTH), hh + space_height))
        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("../../arial.ttf", 50)

        im3.paste(image_overlayed_N, (0, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_J, (WIDTH + 10, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_G, (2 * WIDTH + 20, hh + 2 * space_height + HEIGHT - 100))
        #im3.paste(image_overlayed_F, (0, hh + 3 * space_height + 2 * HEIGHT - 200))
        im3.paste(image_overlayed_ER, (0, hh + 3 * space_height + 2 * HEIGHT - 200))
        im3.paste(image_overlayed_EB, (WIDTH + 10, hh + 3 * space_height + 2 * HEIGHT - 200))
        draw.text((1 / 2 * WIDTH, hh + space_height + HEIGHT),
                  'Nicolas: ', fill=(240, 60, 240), font=font)
        draw.text((3 / 2 * WIDTH + 10, hh + space_height + HEIGHT),
                  'Jean: ', fill=(240, 60, 240), font=font)
        draw.text((5 / 2 * WIDTH + 20, hh + space_height + HEIGHT),
                  'Guiseppe: ', fill=(240, 60, 240), font=font)
        #draw.text((1 / 2 * WIDTH, hh + space_height + 2 * HEIGHT + 50), 'Filippo', fill=(240, 60, 240), font=font)
        draw.text((1 / 2 * WIDTH, hh + space_height + 2 * HEIGHT + 50),
                  'Ervin: ' , fill=(240, 60, 240), font=font)
        draw.text((3 / 2 * WIDTH + 10, hh + space_height + 2 * HEIGHT + 50),
                  'Ebbe: ' , fill=(240, 60, 240), font=font)

        if draw_STAPLE:
            draw.text((5 / 2 * WIDTH + 20, hh + space_height + 2 * HEIGHT + 50), 'Suggestion by STAPLE',
                      fill=(240, 60, 240),font=font)
        if draw_STAPLE:
            im3.paste(image_overlayed_STAPLE, (2*WIDTH + 20, hh + 3 * space_height + 2 * HEIGHT - 200))
            image_width, image_height = image_overlayed_STAPLE.size
            paste_position = (2 * WIDTH + 20, hh + 3 * space_height + 2 * HEIGHT - 200)
            box_coords = (
                paste_position[0],  # Left
                paste_position[1],  # Top
                paste_position[0] + image_width,  # Right
                paste_position[1] + image_height  # Bottom
            )

            # Draw the green rectangle around the pasted image
            draw = ImageDraw.Draw(im3)
            draw.rectangle(box_coords, outline="green", width=30)

        if final_consensus:
            image_cons = Image.open(os.path.join(final_consensus_path, images[i]))
            im3.paste(image_cons.resize((1920, 1080)), (2 * WIDTH + 20, hh + 4 * space_height + 3 * HEIGHT - 300))

        if draw_machine_prediction:
            image_machine = Image.open(os.path.join(machine_path, images[i]))
            image_machine = image_machine.resize((1920, 1080))
            im3.paste(image_machine, (round(1.51 * WIDTH), hh + space_height))
            image_width, image_height = image_overlayed_STAPLE.size
            paste_position = (round(1.51 * WIDTH), hh + space_height)
            box_coords = (
                paste_position[0],  # Left
                paste_position[1],  # Top
                paste_position[0] + image_width,  # Right
                paste_position[1] + image_height  # Bottom
            )

            # Draw the green rectangle around the pasted image
            draw = ImageDraw.Draw(im3)
            draw.rectangle(box_coords, outline="blue", width=30)

        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("../../arial.ttf", 50)

        if final_consensus:
            draw.text((5 / 2 * WIDTH + 20, hh + space_height + 3 * HEIGHT + 100), 'FINAL Consensus',
                      fill=(240, 60, 240), font=font)

        # Draw the text on the image
        imagename = images[i][:-4]

        namevid, _, frnumber = imagename.rpartition('_')
        draw.text((0 / 2 * WIDTH, hh + 100 + int(0 * HEIGHT)), namevid + '_' + frnumber, fill=(0, 0, 0), font=font)
        if draw_STAPLE:
            font = ImageFont.truetype("arial.ttf", 200)
            draw.text((0 / 2 * WIDTH+50, hh + 400 + int(0 * HEIGHT)), str(dict_STAPLE[namevid + '_' + frnumber+'.png'])
, fill=(0, 0, 0), font=font)
        space_height = 150

        hh = hh + N_ROWS * HEIGHT + space_height + 30

        counter += 1

        imagename = images[i][:-4]
        namevid, _, frnumber = imagename.rpartition('_')

    if save_image:

        cv2.imwrite(dest_folder + '/Batch' + str(batch_num) + '-Comparison' + str(j + 1) + ".jpg",
                    cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))
np.save('../../../data/Rates_agreement/Check_rates'+str(batch_num)+'.npy', Check_rates)
np.save('../../../data/Rates_agreement/Treat_rates'+str(batch_num)+'.npy', Treat_rates)
np.save('../../../data/Rates_agreement/Merge_rates'+str(batch_num)+'.npy', Treat_rates)

np.save('../../../data/Rates_agreement/videos'+str(batch_num)+'.npy', vidname)


