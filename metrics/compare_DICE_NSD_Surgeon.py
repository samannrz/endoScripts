import os.path

import pygsheets
from metrics_calculate import *


##### EXTRACT THE RESULTS OF THE SURGEON FROM THE RESPONDERS LINK IN GSHEET #####
gc = pygsheets.authorize(service_account_file="../keycode/my-gpysheets-3d8d13442005.json")
sh = gc.open("Clinical Evaluation of Machine detections (Responses)")
wks = sh[0]

IMAGE_NAMES = wks.get_values(start="B1", end="AO1")[0]
SURGEON = wks.get_values(start="B2", end="AO2")[0]
SURGEON = [int(value) for value in SURGEON]

print("Row 1:", IMAGE_NAMES)
print("Row 2:", SURGEON)
###################################
train_data = 'all'
class_label = 'Treat'
common_path = '/data/DATA/Incision_predictions/test-1-213'
mask_gt_path = '/data/DATA/incision/4/mask/' + class_label
mask_pred_path_fasterViT = os.path.join(common_path , 'FasterViT' , train_data, 'mask', class_label)

for image in IMAGE_NAMES:
    fasterViT_image = os.path.join(mask_pred_path_fasterViT,image)
    gt_image = os.path.join(mask_gt_path,image)
    NSD_fasterViT, DICE_fasterViT, IOU_fasterViT = calculate_metrics(mask_pred_path_fasterViT, mask_gt_path)
