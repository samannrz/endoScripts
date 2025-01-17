import json
Version = 'V2'
############ EXport expert models ##########
for class_label in ['Treat', 'Check']:
    mask_e1_path = '/data/DATA/annotator-consensus/0/mask/' + class_label
    mask_e2_path = '/data/DATA/annotator-consensus/1/mask/' + class_label
    mask_e3_path = '/data/DATA/annotator-consensus/5/mask/' + class_label
    mask_e4_path = '/data/DATA/annotator-consensus/6/mask/' + class_label
    mask_j1_path = '/data/DATA/annotator-consensus/2/mask/' + class_label
    mask_j2_path = '/data/DATA/annotator-consensus/3/mask/' + class_label

    mask_gt_path = '/data/DATA/incision/4/mask/' + class_label

    from metrics_calculate import *

    NSD_e1, DICE_e1, IOU_e1 = calculate_metrics(mask_e1_path, mask_gt_path)
    NSD_e2, DICE_e2, IOU_e2 = calculate_metrics(mask_e2_path, mask_gt_path)
    NSD_e3, DICE_e3, IOU_e3 = calculate_metrics(mask_e3_path, mask_gt_path)
    NSD_e4, DICE_e4, IOU_e4 = calculate_metrics(mask_e4_path, mask_gt_path)
    NSD_j1, DICE_j1, IOU_j1 = calculate_metrics(mask_j1_path, mask_gt_path)
    NSD_j2, DICE_j2, IOU_j2 = calculate_metrics(mask_j2_path, mask_gt_path)

    with open('json_results/'+Version+'/NSD_annotator' + '_' + class_label, 'w') as f1:
        json.dump((NSD_e1, NSD_e2, NSD_e3, NSD_e4, NSD_j1, NSD_j2), f1)

    with open('json_results/'+Version+'/DICE_annotator' + '_' + class_label, 'w') as f2:
        json.dump((DICE_e1, DICE_e2, DICE_e3, DICE_e4, DICE_j1, DICE_j2), f2)
