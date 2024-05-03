import json

class_label = 'Treat'
mask_pred_path_deeplab = '/data/DATA/Incision_predictions/test1-28_Deeplab_consensus_1-28_scheduler/mask/' + class_label
mask_pred_path_fasterViT = '/data/DATA/Incision_predictions/test1-28_FasterVit/mask/' + class_label
mask_pred_path_mask2Former = '/data/DATA/Incision_predictions/test1-28_mask2Former/mask/' + class_label

mask_gt_path = '/data/DATA/incision/4/mask/'+class_label

from metrics_calculate import *

NSD_deeplab, DICE_deeplab, IOU_deeplab = calculate_metrics(mask_pred_path_deeplab, mask_gt_path)
print('Deeplab Done')
NSD_fasterViT, DICE_fasterViT, IOU_fasterViT = calculate_metrics(mask_pred_path_fasterViT, mask_gt_path)
print('fasterViT Done')
NSD_mask2Former, DICE_mask2Former, IOU_mask2Former = calculate_metrics(mask_pred_path_mask2Former, mask_gt_path)

with open('NSD_models_'+class_label, 'w') as f1:
    json.dump((NSD_deeplab, NSD_fasterViT, NSD_mask2Former), f1)

with open('DICE_models_'+class_label, 'w') as f2:
    json.dump((DICE_deeplab, DICE_fasterViT, DICE_mask2Former), f2)
