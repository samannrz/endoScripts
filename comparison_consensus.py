import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os
import pandas as pd
from functions import write_to_gsheet, createDIR
import datetime
from overlay_mask import reColor
from statistics import mean


common_path = 'annotationData26/'
# machine_path = '/data/projects/IncisionDeepLab/outputs_consensus_Batch3-7/inference_results'
# machine_path = '/data/projects/IncisionDeepLab/outputs_consensus_Batch3-7_mobilenet/inference_results'
machine_path = '/data/DATA/Incision_predictions/Batch11/all/final'
dest_folder = 'ImgOut'
draw_machine_prediction = False
batch_num =22

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
print('There are %d images' % lenimg)
batch_size = 4
space_height = 120
ep = 1e-15
nameList = []
frameList = []

HCFstat = []
SCFstat = []
MCFstat = []
HCNstat = []
SCNstat = []
MCNstat = []
HCGstat = []
SCGstat = []
MCGstat = []
HCJstat = []
SCJstat = []
MCJstat = []
HCErstat = []
SCErstat = []
MCErstat = []
HCEbstat = []
SCEbstat = []
MCEbstat = []


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

        try:
            maskH_N = Image.open(os.path.join(common_path, 'maskTreatN', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Nicolas\'s annot on ' + images[i][:-4])
        try:
            maskS_N = Image.open(os.path.join(common_path, 'maskCheckN', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Nicolas\'s annot on ' + images[i][:-4])
        #### Jean Luc ####
        try:
            maskH_J = Image.open(os.path.join(common_path, 'maskTreatJ', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Jean Luc\'s annot on ' + images[i][:-4])
        try:
            maskS_J = Image.open(os.path.join(common_path, 'maskCheckJ', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Jean Luc\'s annot on ' + images[i][:-4])
        #### Giuseppe ####
        try:
            maskH_G = Image.open(os.path.join(common_path, 'maskTreatG', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Giuseppe\'s annot on ' + images[i][:-4])
        try:
            maskS_G = Image.open(os.path.join(common_path, 'maskCheckG', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Giuseppe\'s annot on ' + images[i][:-4])
        #### Filippo ####
        try:
            maskH_F = Image.open(os.path.join(common_path, 'maskTreatF', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Filippo\'s annot on ' + images[i][:-4])
        try:
            maskS_F = Image.open(os.path.join(common_path, 'maskCheckF', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Filippo\'s annot on ' + images[i][:-4])
        try:
            maskH_C = Image.open(os.path.join(common_path, 'maskTreatI', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Consensus\'s annot on ' + images[i][:-4])
        try:
            maskS_C = Image.open(os.path.join(common_path, 'maskCheckI', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Consensus\'s annot on ' + images[i][:-4])

        maskH_N_array = np.array(maskH_N.convert('1'))
        maskS_N_array = np.array(maskS_N.convert('1'))
        maskH_J_array = np.array(maskH_J.convert('1'))
        maskS_J_array = np.array(maskS_J.convert('1'))
        maskH_1_array = np.array(maskH_G.convert('1'))
        maskS_1_array = np.array(maskS_G.convert('1'))
        maskH_2_array = np.array(maskH_F.convert('1'))
        maskS_2_array = np.array(maskS_F.convert('1'))
        maskH_C_array = np.array(maskH_C.convert('1'))
        maskS_C_array = np.array(maskS_C.convert('1'))

        merge1 = maskS_1_array | maskH_1_array
        merge2 = maskS_2_array | maskH_2_array
        mergeN = maskS_N_array | maskH_N_array
        mergeJ = maskS_J_array | maskH_J_array
        mergeC = maskS_C_array | maskH_C_array


####### CONSENSUS SCORES #########
        def score_cal(mask1, mask2):
            epsilon = 1e-15
            intersection = np.logical_and(mask1, mask2)
            union = np.logical_or(mask1, mask2)
            iou = np.sum(intersection) / (np.sum(union) + epsilon)
            if np.sum(intersection) == 0 and np.sum(union) == 0:
                iou = 1
            return iou


        # score of Treat zones with consensus & Nicolas
        HCN = score_cal(maskH_C_array, maskH_N_array)
        SCN = score_cal(maskS_C_array, maskS_N_array)
        MCN = score_cal(mergeC, mergeN)

        HCJ = score_cal(maskH_C_array, maskH_J_array)
        SCJ = score_cal(maskS_C_array, maskS_J_array)
        MCJ = score_cal(mergeC, mergeJ)

        HC1 = score_cal(maskH_C_array, maskH_1_array)
        SC1 = score_cal(maskS_C_array, maskS_1_array)
        MC1 = score_cal(mergeC, merge1)

        HC2 = score_cal(maskH_C_array, maskH_2_array)
        SC2 = score_cal(maskS_C_array, maskS_2_array)
        MC2 = score_cal(mergeC, merge2)

        imagename = images[i][:-4]
        namevid, _, frnumber = imagename.rpartition('_')
        nameList.append(namevid[:-4])
        frameList.append(frnumber)

        HCFstat.append(HC2)
        SCFstat.append(SC2)
        MCFstat.append(MC2)
        HCGstat.append(HC1)
        SCGstat.append(SC1)
        MCGstat.append(MC1)
        HCNstat.append(HCN)
        SCNstat.append(SCN)
        MCNstat.append(MCN)
        HCJstat.append(HCJ)
        SCJstat.append(SCJ)
        MCJstat.append(MCJ)

nameList.append('Average')
frameList.append('')
HCFstat.append(mean(HCFstat))
SCFstat.append(mean(SCFstat))
MCFstat.append(mean(MCFstat))
HCGstat.append(mean(HCGstat))
SCGstat.append(mean(SCGstat))
MCGstat.append(mean(MCGstat))
HCNstat.append(mean(HCNstat))
SCNstat.append(mean(SCNstat))
MCNstat.append(mean(MCNstat))
HCJstat.append(mean(HCJstat))
SCJstat.append(mean(SCJstat))
MCJstat.append(mean(MCJstat))

data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'NB Treat': HCNstat, 'NB Check': SCNstat,
     'NB Merge': MCNstat, 'GG Treat': HCGstat, 'GG Check': SCGstat,
     'GG Merge': MCGstat, 'FF Treat': HCFstat, 'FF Check': SCFstat,
     'FF Merge': MCFstat, 'JLP Treat': HCJstat, 'JLP Check': SCJstat,
     'JLP Merge': MCJstat})
sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
# sheetID = '1HiWuZGv5_Y_BjxnV2gIgDN2VA7WVawuvUd545Wr5FlY'
# sheetName = str(datetime.date.today()) + '-Batch' + str(batch_num)
# write_to_gsheet(sfpath, sheetID, sheetName, data_df)
data_df.to_pickle('c_batch' + str(batch_num) + '.pkl')
print('c_batch' + str(batch_num) + '.pkl saved')

# sheetID = '1PeZuOl_tUKS_j6-5-DDoOd9b-iUVVEZC9Ff9cZ7jp-0'
# write_to_gsheet(sfpath, sheetID, str(batch_num), data_df)
