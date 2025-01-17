import argparse

import cv2
import numpy as np
import os
import pandas as pd
from functions import write_to_gsheet
from statistics import mean


parser = argparse.ArgumentParser()
parser.add_argument('--batch', help = 'batch number')
parser.add_argument('--input',help = 'path of dest. folder')
args = parser.parse_args()
batch_num = args.batch
common_path = args.input

images = os.listdir(os.path.join(common_path, 'image'))
lenimg = len(images)
print('There are %d images' % lenimg)
nameList = []
frameList = []
Treat_C_O_stat = []
Check_C_O_stat = []
Merge_C_O_stat = []
Treat_C_A_stat = []
Check_C_A_stat = []
Merge_C_A_stat = []
Treat_C_G_stat = []
Check_C_G_stat = []
Merge_C_G_stat = []

for i in range(lenimg):
    print(images[i])
    image_orig = cv2.imread(os.path.join(common_path, 'image', images[i]))
    maskH_O_array = cv2.imread(os.path.join(common_path, 'maskTreat_os', images[i][:-4] + '.png'))
    maskS_O_array = cv2.imread(os.path.join(common_path, 'maskCheck_os', images[i][:-4] + '.png'))
    maskH_A_array = cv2.imread(os.path.join(common_path, 'maskTreat_an', images[i][:-4] + '.png'))
    maskS_A_array = cv2.imread(os.path.join(common_path, 'maskCheck_an', images[i][:-4] + '.png'))
    maskH_G_array = cv2.imread(os.path.join(common_path, 'maskTreat_gr', images[i][:-4] + '.png'))
    maskS_G_array = cv2.imread(os.path.join(common_path, 'maskCheck_gr', images[i][:-4] + '.png'))

    maskH_C_array = cv2.imread(os.path.join(common_path, 'maskTreat_j.', images[i][:-4] + '.png'))
    maskS_C_array = cv2.imread(os.path.join(common_path, 'maskCheck_j.', images[i][:-4] + '.png'))

    merge_G = maskS_G_array | maskH_G_array
    merge_O = maskS_O_array | maskH_O_array
    merge_A = maskS_A_array | maskH_A_array

    merge_C = maskS_C_array | maskH_C_array

    ####### CONSENSUS SCORES #########
    def score_cal(mask1, mask2):
        epsilon = 1e-15
        intersection = np.logical_and(mask1, mask2)
        union = np.logical_or(mask1, mask2)
        iou = np.sum(intersection) / (np.sum(union) + epsilon)
        if np.sum(intersection) == 0 and np.sum(union) == 0:
            iou = 1
        return iou


    # score of Treat/Check/Merge zones with consensus & Nicolas
    Treat_C_O = score_cal(maskH_C_array, maskH_O_array)
    Check_C_O = score_cal(maskS_C_array, maskS_O_array)
    Merge_C_O = score_cal(merge_C, merge_O)
    # score of Treat/Check/Merge zones with consensus & Jean
    Treat_C_A = score_cal(maskH_C_array, maskH_A_array)
    Check_C_A = score_cal(maskS_C_array, maskS_A_array)
    Merge_C_A = score_cal(merge_C, merge_A)
    # score of Treat/Check/Merge zones with consensus & Giuseppe
    Treat_C_G = score_cal(maskH_C_array, maskH_G_array)
    Check_C_G = score_cal(maskS_C_array, maskS_G_array)
    Merge_C_G = score_cal(merge_C, merge_G)
    # score of Treat/Check/Merge zones with consensus & Filippo
    namevid, _, frnumber = images[i][:-4].rpartition('_')
    nameList.append(namevid[:-4])
    frameList.append(frnumber)

    Treat_C_G_stat.append(Treat_C_G)
    Check_C_G_stat.append(Check_C_G)
    Merge_C_G_stat.append(Merge_C_G)
    Treat_C_O_stat.append(Treat_C_O)
    Check_C_O_stat.append(Check_C_O)
    Merge_C_O_stat.append(Merge_C_O)
    Treat_C_A_stat.append(Treat_C_A)
    Check_C_A_stat.append(Check_C_A)
    Merge_C_A_stat.append(Merge_C_A)

nameList.append('Average')
frameList.append('')
Treat_C_G_stat.append(mean(Treat_C_G_stat))
Check_C_G_stat.append(mean(Check_C_G_stat))
Merge_C_G_stat.append(mean(Merge_C_G_stat))
Treat_C_O_stat.append(mean(Treat_C_O_stat))
Check_C_O_stat.append(mean(Check_C_O_stat))
Merge_C_O_stat.append(mean(Merge_C_O_stat))
Treat_C_A_stat.append(mean(Treat_C_A_stat))
Check_C_A_stat.append(mean(Check_C_A_stat))
Merge_C_A_stat.append(mean(Merge_C_A_stat))

data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'OP Treat': Treat_C_O_stat, 'OP Check': Check_C_O_stat,
     'OP Merge': Merge_C_O_stat, 'ASP Treat': Treat_C_A_stat, 'ASP Check': Check_C_A_stat,
     'ASP Merge': Merge_C_A_stat, 'GO Treat': Treat_C_G_stat, 'GO Check': Check_C_G_stat,
     'GO Merge': Merge_C_G_stat})

sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
data_df.to_pickle('pkl_files/c_batch' + str(batch_num) + '.pkl')
print('pkl_files/c_batchj' +  str(batch_num) + '.pkl saved')
sheetID = '171H6ZgzfzZVD-Zz8LFpry-3rVC_ORq59-xy2OIBHqyA'
write_to_gsheet(sfpath, sheetID, str(batch_num)+'j', data_df)
