import cv2
import numpy as np
import os
import pandas as pd
from functions import write_to_gsheet
from statistics import mean

common_path = 'annotationData/'
batch_num = 25

images = os.listdir(common_path + '/image')
lenimg = len(images)
print('There are %d images' % lenimg)
nameList = []
frameList = []
Treat_C_F_stat = []
Check_C_F_stat = []
Merge_C_F_stat = []
Treat_C_N_stat = []
Check_C_N_stat = []
Merge_C_N_stat = []
Treat_C_G_stat = []
Check_C_G_stat = []
Merge_C_G_stat = []
Treat_C_J_stat = []
Check_C_J_stat = []
Merge_C_J_stat = []
Treat_C_Er_stat = []
Check_C_Er_stat = []
Merge_C_Er_stat = []
Treat_C_Eb_stat = []
Check_C_Eb_stat = []
Merge_C_Eb_stat = []

for i in range(lenimg):
    print(images[i])
    image_orig = cv2.imread(os.path.join(common_path, 'image', images[i]))
    maskH_N_array = cv2.imread(os.path.join(common_path, 'maskTreat_ni', images[i][:-4] + '.png'))
    maskS_N_array = cv2.imread(os.path.join(common_path, 'maskCheck_ni', images[i][:-4] + '.png'))
    maskH_J_array = cv2.imread(os.path.join(common_path, 'maskTreat_Je', images[i][:-4] + '.png'))
    maskS_J_array = cv2.imread(os.path.join(common_path, 'maskCheck_Je', images[i][:-4] + '.png'))
    maskH_G_array = cv2.imread(os.path.join(common_path, 'maskTreat_gi', images[i][:-4] + '.png'))
    maskS_G_array = cv2.imread(os.path.join(common_path, 'maskCheck_gi', images[i][:-4] + '.png'))
    maskH_F_array = cv2.imread(os.path.join(common_path, 'maskTreat_fi', images[i][:-4] + '.png'))
    maskS_F_array = cv2.imread(os.path.join(common_path, 'maskCheck_fi', images[i][:-4] + '.png'))
    maskH_Er_array = cv2.imread(os.path.join(common_path, 'maskTreat_Er', images[i][:-4] + '.png'))
    maskS_Er_array = cv2.imread(os.path.join(common_path, 'maskCheck_Er', images[i][:-4] + '.png'))
    maskH_Eb_array = cv2.imread(os.path.join(common_path, 'maskTreat_eb', images[i][:-4] + '.png'))
    maskS_Eb_array = cv2.imread(os.path.join(common_path, 'maskCheck_eb', images[i][:-4] + '.png'))
    maskH_C_array = cv2.imread(os.path.join(common_path, 'maskTreat_in', images[i][:-4] + '.png'))
    maskS_C_array = cv2.imread(os.path.join(common_path, 'maskCheck_in', images[i][:-4] + '.png'))

    merge_G = maskS_G_array | maskH_G_array
    merge_F = maskS_F_array | maskH_F_array
    merge_N = maskS_N_array | maskH_N_array
    merge_J = maskS_J_array | maskH_J_array
    merge_Er = maskS_Er_array | maskH_Er_array
    merge_Eb = maskS_Eb_array | maskH_Eb_array
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
    Treat_C_N = score_cal(maskH_C_array, maskH_N_array)
    Check_C_N = score_cal(maskS_C_array, maskS_N_array)
    Merge_C_N = score_cal(merge_C, merge_N)
    # score of Treat/Check/Merge zones with consensus & Jean
    Treat_C_J = score_cal(maskH_C_array, maskH_J_array)
    Check_C_J = score_cal(maskS_C_array, maskS_J_array)
    Merge_C_J = score_cal(merge_C, merge_J)
    # score of Treat/Check/Merge zones with consensus & Giuseppe
    Treat_C_G = score_cal(maskH_C_array, maskH_G_array)
    Check_C_G = score_cal(maskS_C_array, maskS_G_array)
    Merge_C_G = score_cal(merge_C, merge_G)
    # score of Treat/Check/Merge zones with consensus & Filippo
    Treat_C_F = score_cal(maskH_C_array, maskH_F_array)
    Check_C_F = score_cal(maskS_C_array, maskS_F_array)
    Merge_C_F = score_cal(merge_C, merge_F)
    # score of Treat/Check/Merge zones with consensus & Ervin
    Treat_C_Er = score_cal(maskH_C_array, maskH_Er_array)
    Check_C_Er = score_cal(maskS_C_array, maskS_Er_array)
    Merge_C_Er = score_cal(merge_C, merge_Er)
    # score of Treat/Check/Merge zones with consensus & Ebbe
    Treat_C_Eb = score_cal(maskH_C_array, maskH_Eb_array)
    Check_C_Eb = score_cal(maskS_C_array, maskS_Eb_array)
    Merge_C_Eb = score_cal(merge_C, merge_Eb)

    namevid, _, frnumber = images[i][:-4].rpartition('_')
    nameList.append(namevid[:-4])
    frameList.append(frnumber)


    Treat_C_F_stat.append(Treat_C_F)
    Check_C_F_stat.append(Check_C_F)
    Merge_C_F_stat.append(Merge_C_F)
    Treat_C_G_stat.append(Treat_C_G)
    Check_C_G_stat.append(Check_C_G)
    Merge_C_G_stat.append(Merge_C_G)
    Treat_C_N_stat.append(Treat_C_N)
    Check_C_N_stat.append(Check_C_N)
    Merge_C_N_stat.append(Merge_C_N)
    Treat_C_J_stat.append(Treat_C_J)
    Check_C_J_stat.append(Check_C_J)
    Merge_C_J_stat.append(Merge_C_J)
    Treat_C_Er_stat.append(Treat_C_Er)
    Check_C_Er_stat.append(Check_C_Er)
    Merge_C_Er_stat.append(Merge_C_Er)
    Treat_C_Eb_stat.append(Treat_C_Eb)
    Check_C_Eb_stat.append(Check_C_Eb)
    Merge_C_Eb_stat.append(Merge_C_Eb)

nameList.append('Average')
frameList.append('')
Treat_C_F_stat.append(mean(Treat_C_F_stat))
Check_C_F_stat.append(mean(Check_C_F_stat))
Merge_C_F_stat.append(mean(Merge_C_F_stat))
Treat_C_G_stat.append(mean(Treat_C_G_stat))
Check_C_G_stat.append(mean(Check_C_G_stat))
Merge_C_G_stat.append(mean(Merge_C_G_stat))
Treat_C_N_stat.append(mean(Treat_C_N_stat))
Check_C_N_stat.append(mean(Check_C_N_stat))
Merge_C_N_stat.append(mean(Merge_C_N_stat))
Treat_C_J_stat.append(mean(Treat_C_J_stat))
Check_C_J_stat.append(mean(Check_C_J_stat))
Merge_C_J_stat.append(mean(Merge_C_J_stat))
Treat_C_Er_stat.append(mean(Treat_C_Er_stat))
Check_C_Er_stat.append(mean(Check_C_Er_stat))
Merge_C_Er_stat.append(mean(Merge_C_Er_stat))
Treat_C_Eb_stat.append(mean(Treat_C_Eb_stat))
Check_C_Eb_stat.append(mean(Check_C_Eb_stat))
Merge_C_Eb_stat.append(mean(Merge_C_Eb_stat))

data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'NB Treat': Treat_C_N_stat, 'NB Check': Check_C_N_stat,
     'NB Merge': Merge_C_N_stat, 'GG Treat': Treat_C_G_stat, 'GG Check': Check_C_G_stat,
     'GG Merge': Merge_C_G_stat, 'FF Treat': Treat_C_F_stat, 'FF Check': Check_C_F_stat,
     'FF Merge': Merge_C_F_stat, 'JLP Treat': Treat_C_J_stat, 'JLP Check': Check_C_J_stat,
     'JLP Merge': Merge_C_J_stat, 'EK Treat': Treat_C_Er_stat, 'EK Check': Check_C_Er_stat,
     'EK Merge': Merge_C_Er_stat, 'ET Treat': Treat_C_Eb_stat, 'ET Check': Check_C_Eb_stat,
     'ET Merge': Merge_C_Eb_stat})
sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
data_df.to_pickle('c_batch' + str(batch_num) + '.pkl')
print('c_batch' + str(batch_num) + '.pkl saved')
sheetID = '1PeZuOl_tUKS_j6-5-DDoOd9b-iUVVEZC9Ff9cZ7jp-0'
write_to_gsheet(sfpath, sheetID, str(batch_num), data_df)
