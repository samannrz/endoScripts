import json
import os

class_label = 'Treat'
common_path = '/data/DATA/Incision_predictions/test-1-213'
#train_data = 'consensus'
train_data1 = 'expert_consensus'
train_data2 = 'junior_consensus'

Version = 'V2'
mask_pred_path_deeplab_expert = os.path.join(common_path , 'Deeplab' , train_data1, 'mask', class_label)
mask_pred_path_deeplab_junior = os.path.join(common_path , 'Deeplab' , train_data2, 'mask', class_label)

mask_gt_path = '/data/DATA/incision/4/mask/' + class_label

from metrics_calculate import *

NSD_deeplab_expert, DICE_deeplab_expert, IOU_deeplab_expert = calculate_metrics(mask_pred_path_deeplab_expert, mask_gt_path)
print('Deeplab experts Done')
NSD_deeplab_junior, DICE_deeplab_junior, IOU_deeplab_junior = calculate_metrics(mask_pred_path_deeplab_junior, mask_gt_path)
print('Deeplab juniors Done')

with open('json_results/'+Version+'/NSD_models_' + train_data1 + '_' +train_data2+'_'+ class_label, 'w') as f1:
    json.dump((NSD_deeplab_expert, NSD_deeplab_junior), f1)
with open('json_results/'+Version+'/DICE_models_' + train_data1 + '_' +train_data2+'_'+ class_label, 'w') as f2:
    json.dump((DICE_deeplab_expert, DICE_deeplab_junior), f2)