
import os

from metrics import *
import cv2


def calculate_metrics(mask_pred_path,mask_gt_path):
    NSD=[]
    IOU=[]
    DICE=[]
    if os.path.isdir(mask_pred_path):  # If it's a directory, process all files
        filenames = os.listdir(mask_pred_path)

    elif os.path.isfile(mask_pred_path):  # If it's a single file, process only that file
        filenames = [os.path.basename(mask_pred_path)]
        mask_gt_path = mask_gt_path  # Ensure mask_gt_path corresponds to the correct file
    else:
        raise ValueError("Invalid path: mask_pred_path must be a valid file or directory.")
    for filename in filenames:
        mask_pred_path1 = os.path.join(mask_pred_path, filename) if os.path.isdir(mask_pred_path) else mask_pred_path
        mask_gt_path1 = os.path.join(mask_gt_path, filename) if os.path.isdir(mask_pred_path) else mask_gt_path

        mask_gt = cv2.imread(mask_gt_path1, cv2.IMREAD_GRAYSCALE).astype(bool)
        mask_pred = cv2.imread(mask_pred_path1, cv2.IMREAD_GRAYSCALE).astype(bool)

        a = compute_surface_distances(mask_gt, mask_pred, (1, 1))
        # NSD = compute_surface_dice_at_tolerance(a, tolerance_mm=100)
        if mask_gt.shape[1] == 854 or mask_gt.shape[1] == 418:
            mask_gt = mask_gt[:, :-1]
        if mask_pred.shape[1] == 854 or mask_pred.shape[1] == 418:
            mask_pred = mask_pred[:, :-1]
        NSD.append(compute_NSD(mask_gt, mask_pred, 20, 100))
        DICE.append(compute_dice_coefficient(mask_gt, mask_pred))
        IOU.append(calculate_iou(mask_gt, mask_pred))
    return NSD,DICE,IOU
