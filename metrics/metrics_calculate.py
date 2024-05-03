
import os

from metrics import *
import cv2


def calculate_metrics(mask_pred_path,mask_gt_path):
    NSD=[]
    IOU=[]
    DICE=[]
    for filename in os.listdir(mask_pred_path):
        mask_pred_path1 = os.path.join(mask_pred_path, filename)
        mask_gt_path1 = os.path.join(mask_gt_path, filename)

        print(filename)
        mask_gt = cv2.imread(mask_gt_path1, cv2.IMREAD_GRAYSCALE).astype(bool)
        mask_pred = cv2.imread(mask_pred_path1, cv2.IMREAD_GRAYSCALE).astype(bool)

        a = compute_surface_distances(mask_gt, mask_pred, (1, 1))
        # NSD = compute_surface_dice_at_tolerance(a, tolerance_mm=100)
        NSD.append(compute_NSD(mask_gt, mask_pred, 20, 100))
        DICE.append(compute_dice_coefficient(mask_gt, mask_pred))
        IOU.append(calculate_iou(mask_gt, mask_pred))
    return NSD,DICE,IOU
