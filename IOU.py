import os

import cv2
import numpy as np


def calculate_iou(mask1, mask2):
    epsilon = 1e-15
    intersection = np.logical_and(mask1, mask2)
    union = np.logical_or(mask1, mask2)
    iou = np.sum(intersection) / (np.sum(union) + epsilon)
    if np.sum(intersection) == 0 and np.sum(union) == 0:
        iou = 1
    return iou


path_ref = '/data/DATA/incision/4/mask'
path_inf = '/data/projects/IncisionDeepLab/outputs/outputs_all_Batch1-25/test_consensus_inference/detected/mask'

iou_treat = []
iou_check = []
path_Treat = os.path.join(path_inf, 'Treat')
for mask_name in os.listdir(path_Treat):
    mask_ref_Treat = cv2.imread(os.path.join(path_ref, 'Treat', mask_name))
    mask_ref_Check = cv2.imread(os.path.join(path_ref, 'Check', mask_name))
    mask_inf_Treat = cv2.imread(os.path.join(path_inf, 'Treat', mask_name))
    mask_inf_Check = cv2.imread(os.path.join(path_inf, 'Check', mask_name))

    if mask_ref_Check.shape[1] == 854 or mask_ref_Check.shape[1] == 418:
        mask_ref_Check = mask_ref_Check[:, :-1, :]
        mask_ref_Treat = mask_ref_Treat[:, :-1, :]

    iou_treat.append(calculate_iou(mask_ref_Treat, mask_inf_Treat))
    iou_check.append(calculate_iou(mask_ref_Check, mask_inf_Check))
    print(mask_name)
print(np.mean(iou_treat))
print(np.mean(iou_check))
