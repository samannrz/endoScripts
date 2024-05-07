import json
import os

class_label = 'Treat'
common_path = '/data/DATA/Incision_predictions/test-1-28_'
train_data = 'all'
mask_pred_path_deeplab = os.path.join(common_path + 'Deeplab_' + train_data, 'mask', class_label)
mask_pred_path_fasterViT = os.path.join(common_path + 'FasterViT_' + train_data, 'mask', class_label)
mask_pred_path_mask2Former = os.path.join(common_path + 'Mask2Former_' + train_data, 'mask', class_label)

mask_gt_path = '/data/DATA/incision/4/mask/' + class_label

from metrics_calculate import *

NSD_deeplab, DICE_deeplab, IOU_deeplab = calculate_metrics(mask_pred_path_deeplab, mask_gt_path)
print('Deeplab Done')
NSD_fasterViT, DICE_fasterViT, IOU_fasterViT = calculate_metrics(mask_pred_path_fasterViT, mask_gt_path)
print('fasterViT Done')
NSD_mask2Former, DICE_mask2Former, IOU_mask2Former = calculate_metrics(mask_pred_path_mask2Former, mask_gt_path)
print('Mask2Former Done')

with open('json_results/NSD_models_' + train_data + '_' + class_label, 'w') as f1:
    json.dump((NSD_deeplab, NSD_fasterViT, NSD_mask2Former), f1)

with open('json_results/DICE_models_' + train_data + '_' + class_label, 'w') as f2:
    json.dump((DICE_deeplab, DICE_fasterViT, DICE_mask2Former), f2)
