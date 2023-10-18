import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os
import matplotlib.pyplot as plt
import pandas as pd
from functions import write_to_gsheet, createDIR
import datetime
from overlay_mask import reColor
from statistics import mean

batch_num = 21
# from IncisionDataFolderCreation import batch_num

common_path = 'annotationData/'
# machine_path = '/data/projects/IncisionDeepLab/outputs_consensus_Batch3-7/inference_results'
# machine_path = '/data/projects/IncisionDeepLab/outputs_consensus_Batch3-7_mobilenet/inference_results'
machine_path = '/data/DATA/Incision_predictions/Batch11/all/final'
dest_folder = 'ImgOut2'
draw_machine_prediction = False


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


nb_ann = 6
images = os.listdir(common_path + '/image')
createDIR('', dest_folder)
lenimg = len(images)
Treat_rates = np.zeros((lenimg, nb_ann * nb_ann))
Check_rates = np.zeros((lenimg, nb_ann * nb_ann))
r = 0
print('There are %d images' % lenimg)
batch_size = 2
space_height = 150
ep = 1e-15
save_image = False


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
          calculate_score(maskH_G, maskH_F), calculate_score(maskH_G, maskH_F), calculate_score(maskH_G, maskH_ER),

          calculate_score(maskH_F, maskH_N), calculate_score(maskH_F, maskH_J), calculate_score(maskH_F, maskH_G),
          calculate_score(maskH_F, maskH_F), calculate_score(maskH_F, maskH_F), calculate_score(maskH_F, maskH_ER),

          calculate_score(maskH_ER, maskH_N), calculate_score(maskH_ER, maskH_J), calculate_score(maskH_ER, maskH_G),
          calculate_score(maskH_ER, maskH_F), calculate_score(maskH_ER, maskH_F), calculate_score(maskH_ER, maskH_ER),

          calculate_score(maskH_EB, maskH_N), calculate_score(maskH_EB, maskH_J), calculate_score(maskH_EB, maskH_G),
          calculate_score(maskH_EB, maskH_F), calculate_score(maskH_EB, maskH_F), calculate_score(maskH_EB, maskH_ER),
          ]
    C1 = [calculate_score(maskS_N, maskS_N), calculate_score(maskS_N, maskS_J), calculate_score(maskS_N, maskS_G),
          calculate_score(maskS_N, maskS_F), calculate_score(maskS_N, maskS_ER), calculate_score(maskS_N, maskS_EB),

          calculate_score(maskS_J, maskS_N), calculate_score(maskS_J, maskS_J), calculate_score(maskS_J, maskS_G),
          calculate_score(maskS_J, maskS_F), calculate_score(maskS_J, maskS_ER), calculate_score(maskS_J, maskS_EB),

          calculate_score(maskS_G, maskS_N), calculate_score(maskS_G, maskS_J), calculate_score(maskS_G, maskS_G),
          calculate_score(maskS_G, maskS_F), calculate_score(maskS_G, maskS_F), calculate_score(maskS_G, maskS_ER),

          calculate_score(maskS_F, maskS_N), calculate_score(maskS_F, maskS_J), calculate_score(maskS_F, maskS_G),
          calculate_score(maskS_F, maskS_F), calculate_score(maskS_F, maskS_F), calculate_score(maskS_F, maskS_ER),

          calculate_score(maskS_ER, maskS_N), calculate_score(maskS_ER, maskS_J), calculate_score(maskS_ER, maskS_G),
          calculate_score(maskS_ER, maskS_F), calculate_score(maskS_ER, maskS_F), calculate_score(maskS_ER, maskS_ER),

          calculate_score(maskS_EB, maskS_N), calculate_score(maskS_EB, maskS_J), calculate_score(maskS_EB, maskS_G),
          calculate_score(maskS_EB, maskS_F), calculate_score(maskS_EB, maskS_F), calculate_score(maskS_EB, maskS_ER),
          ]
    return T1, C1


for j in range(math.ceil(lenimg / batch_size)):
    counter = 1
    batchstart = True
    hh = 0
    print(j)

    for i in range(j * batch_size, (j + 1) * batch_size):
        if i > lenimg - 1:
            break
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
        maskH_F = Image.open(os.path.join(common_path, 'maskTreat_fi', images[i][:-4] + '.png'))
        maskS_F = Image.open(os.path.join(common_path, 'maskCheck_fi', images[i][:-4] + '.png'))
        maskH_ER = Image.open(os.path.join(common_path, 'maskTreat_Er', images[i][:-4] + '.png'))
        maskS_ER = Image.open(os.path.join(common_path, 'maskCheck_Er', images[i][:-4] + '.png'))
        maskH_EB = Image.open(os.path.join(common_path, 'maskTreat_eb', images[i][:-4] + '.png'))
        maskS_EB = Image.open(os.path.join(common_path, 'maskCheck_eb', images[i][:-4] + '.png'))

        #########################
        image_overlayed_N = overlayMasks_incision(image_orig, maskH_N, maskS_N)
        image_overlayed_J = overlayMasks_incision(image_orig, maskH_J, maskS_J)
        image_overlayed_G = overlayMasks_incision(image_orig, maskH_G, maskS_G)
        image_overlayed_F = overlayMasks_incision(image_orig, maskH_F, maskS_F)
        image_overlayed_ER = overlayMasks_incision(image_orig, maskH_ER, maskS_ER)
        image_overlayed_EB = overlayMasks_incision(image_orig, maskH_EB, maskS_EB)

        Treat_rates[r, :], Check_rates[r, :] = calculate_agreements(maskH_N, maskH_J, maskH_G, maskH_F, maskH_ER,
                                                                    maskH_EB, maskS_N, maskS_J, maskS_G,
                                                                    maskS_F, maskS_ER, maskS_EB)
        r += 1
        if not save_image:
            continue

        if batchstart:
            batchstart = False
            if j > math.floor(lenimg / batch_size) - 1:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    3 * (lenimg % batch_size) * 1080 + space_height * (lenimg % batch_size)),
                                (255, 255, 255))
            else:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    3 * batch_size * 1080 + space_height * (batch_size + 1)),
                                (255, 255, 255))

        if image_overlayed_N.width < 1920:
            newsize = (1920, 1080)
            image_overlayed_N = image_overlayed_N.resize(newsize)
            image_overlayed_J = image_overlayed_J.resize(newsize)
            image_overlayed_G = image_overlayed_G.resize(newsize)
            image_overlayed_F = image_overlayed_F.resize(newsize)
            image_overlayed_EB = image_overlayed_EB.resize(newsize)
            image_overlayed_ER = image_overlayed_ER.resize(newsize)
            image_orig = image_orig.resize(newsize)

        WIDTH = image_orig.width
        HEIGHT = image_orig.height
        # Paste the images onto the white background
        if draw_machine_prediction:
            im3.paste(image_orig, (int(0.5 * WIDTH), hh + space_height))
        else:
            im3.paste(image_orig, (int(1 * WIDTH), hh + space_height))

        im3.paste(image_overlayed_N, (0, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_J, (WIDTH + 10, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_G, (2 * WIDTH + 20, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_F, (0, hh + 3 * space_height + 2 * HEIGHT - 200))
        im3.paste(image_overlayed_ER, (WIDTH + 10, hh + 3 * space_height + 2 * HEIGHT - 200))
        im3.paste(image_overlayed_EB, (2 * WIDTH + 20, hh + 3 * space_height + 2 * HEIGHT - 200))

        if draw_machine_prediction:
            image_machine = Image.open(os.path.join(machine_path, images[i]))
            im3.paste(image_machine.resize((1920, 1080)), (1.5 * WIDTH, hh + space_height))

        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("arial.ttf", 50)

        draw.text((1 / 2 * WIDTH, hh + space_height + HEIGHT), 'N', fill=(240, 60, 240), font=font)
        draw.text((3 / 2 * WIDTH + 10, hh + space_height + HEIGHT), 'J', fill=(240, 60, 240), font=font)
        draw.text((5 / 2 * WIDTH + 20, hh + space_height + HEIGHT), 'G', fill=(240, 60, 240), font=font)
        draw.text((1 / 2 * WIDTH, hh + space_height + 2 * HEIGHT + 50), 'F', fill=(240, 60, 240), font=font)
        draw.text((3 / 2 * WIDTH + 10, hh + space_height + 2 * HEIGHT + 50), 'Er', fill=(240, 60, 240), font=font)
        draw.text((5 / 2 * WIDTH + 20, hh + space_height + 2 * HEIGHT + 50), 'Eb', fill=(240, 60, 240), font=font)

        # Draw the text on the image
        imagename = images[i][:-4]

        namevid, _, frnumber = imagename.rpartition('_')
        draw.text((0 / 2 * WIDTH, hh + int(0.5 * HEIGHT)), namevid + '_' + frnumber, fill=(0, 0, 0), font=font)
        hh = hh + 3 * HEIGHT + space_height + 30

        counter += 1

        imagename = images[i][:-4]
        namevid, _, frnumber = imagename.rpartition('_')
    if save_image:
        cv2.imwrite(dest_folder + '/Batch' + str(batch_num) + '-Comparison' + str(j + 1) + ".jpg",
                    cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))

Treat_matrix_flat = np.mean(Treat_rates, axis=0)
Treat_matrix = Treat_matrix_flat.reshape(6,6)
Check_matrix_flat = np.mean(Check_rates, axis=0)
Check_matrix = Check_matrix_flat.reshape(6,6)
plt.imshow(Treat_matrix,cmap = 'viridis')
plt.colorbar()
plt.show
#  im3.save(dest_folder +'/Batch' + str(batch_num) + '-Comparison' + str(j + 1) + ".jpg")

# im3.close()

# data_df = pd.DataFrame(
#     {'Vid. Name': nameList, '# frame': frameList, 'FF-NB Treat': HFNstat, 'FF-NB Check': SFNstat,
#      'FF-NB Merge': MFNstat, 'GG-NB Treat': HGNstat, 'GG-NB Check': SGNstat,
#      'GG-NB Merge': MGNstat, 'FF-JLP Treat': HFJstat, 'FF-JLP Check': SFJstat,
#      'FF-JLP Merge': MFJstat, 'GG-JLP Treat': HGJstat, 'GG-JLP Check': SGJstat,
#      'GG-JLP Merge': MGJstat, 'NB-JLP Treat': HNJstat, 'NB-JLP Check': SNJstat,
#      'NB-JLP Merge': MNJstat})
# # sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
# # sheetID = '1HiWuZGv5_Y_BjxnV2gIgDN2VA7WVawuvUd545Wr5FlY'
# # sheetName = str(datetime.date.today()) + '-Batch' + str(batch_num)
# # write_to_gsheet(sfpath, sheetID, sheetName, data_df)
# data_df.to_pickle('batch' + str(batch_num) + '.pkl')
# print('batch' + str(batch_num) + '.pkl saved')
