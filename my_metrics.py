import datetime
import os

def calculate_iou(box1, box2):
    x1, y1, w1, h1 = box1
    x2, y2, w2, h2 = box2

    # Convert normalized coordinates to absolute coordinates
    x1, y1 = x1 - w1/2, y1 - h1/2
    x2, y2 = x2 - w2/2, y2 - h2/2

    # Calculate coordinates of intersection rectangle
    x_left = max(x1, x2)
    y_top = max(y1, y2)
    x_right = min(x1 + w1, x2 + w2)
    y_bottom = min(y1 + h1, y2 + h2)

    if x_right < x_left or y_bottom < y_top:
        return 0.0  # No intersection

    # Calculate area of intersection rectangle
    intersection_area = (x_right - x_left) * (y_bottom - y_top)

    # Calculate area of both detection and ground truth rectangles
    box1_area = w1 * h1
    box2_area = w2 * h2

    # Calculate IoU
    iou = intersection_area / float(box1_area + box2_area - intersection_area)
    return iou

def evaluate_detections(det_folder, gt_folder, num_classes, iou_threshold=0.5):
    true_positives = [0] * num_classes
    false_positives = [0] * num_classes
    false_negatives = [0] * num_classes

    det_files = os.listdir(det_folder)
    gt_files = os.listdir(gt_folder)

    for det_file, gt_file in zip(det_files, gt_files):
        with open(os.path.join(det_folder, det_file), 'r') as det_f, \
             open(os.path.join(gt_folder, gt_file), 'r') as gt_f:
            det_boxes = [list(map(float, line.strip().split())) for line in det_f.readlines()]
            gt_boxes = [list(map(float, line.strip().split())) for line in gt_f.readlines()]

            for gt_box in gt_boxes:
                gt_class = int(gt_box[0])
                gt_box = gt_box[1:]

                found_match = False

                for det_box in det_boxes:
                    det_class = int(det_box[0])
                    if det_class != gt_class:
                        continue

                    iou = calculate_iou(det_box[1:], gt_box)
                    if iou >= iou_threshold:
                        true_positives[gt_class] += 1
                        found_match = True
                        det_boxes.remove(det_box)
                        break

                if not found_match:
                    false_negatives[gt_class] += 1

            false_positives_per_class = [0] * num_classes

            for det_box in det_boxes:
                det_class = int(det_box[0])
                false_positives_per_class[det_class] += 1

            for idx, fp_count in enumerate(false_positives_per_class):
                false_positives[idx] += fp_count

    return true_positives, false_positives, false_negatives
def count_boxes_by_class(folder, num_classes):
    total_boxes_by_class = [0] * num_classes

    files = os.listdir(folder)

    for file in files:
        with open(os.path.join(folder, file), 'r') as f:
            boxes = [list(map(float, line.strip().split())) for line in f.readlines()]
            for box in boxes:
                class_id = int(box[0])
                total_boxes_by_class[class_id] += 1

    return total_boxes_by_class


def calculate_metrics(TP, FP, FN):
    precision = [TP[i] / (TP[i] + FP[i]) if (TP[i] + FP[i]) > 0 else 0 for i in range(len(TP))]
    sensitivity = [TP[i] / (TP[i] + FN[i]) if (TP[i] + FN[i]) > 0 else 0 for i in range(len(TP))]
    accuracy = [(TP[i] + 0) / (TP[i] + 0 + FP[i] + FN[i]) if (TP[i] + 0 + FP[i] + FN[i]) > 0 else 0 for i in
                range(len(TP))]  # Assuming TN is not available
    specificity = [(0) / (0 + FP[i]) if (0 + FP[i]) > 0 else 0 for i in range(len(TP))]  # Assuming TN is not available
    f1_score = [2 * (precision[i] * sensitivity[i]) / (precision[i] + sensitivity[i]) if (precision[i] + sensitivity[
        i]) > 0 else 0 for i in range(len(TP))]

    return precision, sensitivity, accuracy, specificity, f1_score


det_folder = '/data/TESTwithAntoine/video2/detect/exp1/labels'
gt_folder = '/data/TESTwithAntoine/video2/YOLOLabel'

det_folder = '/data/projects/yolov5/runs/detect/exp251/labels'
gt_folder = '/data/projects/datasets/coco128-2023-06-28-2/labels/test'

num_classes = 9

TP, FP, FN = evaluate_detections(det_folder, gt_folder, num_classes,iou_threshold=0.05)
precision, sensitivity, accuracy, specificity, f1_score = calculate_metrics(TP, FP, FN)

total_gt_boxes = count_boxes_by_class(gt_folder, num_classes)
total_detected_boxes = count_boxes_by_class(det_folder, num_classes)
class_names = {
    0: "Adh Dense",
    1: "Adh Filmy",
    2: "Sup Black",
    3: "Sup White",
    4: "Sup Red",
    5: "Sup Subtle",
    6: "Ov. Endometrioma",
    7: "Ov. Chocolate Fluid",
    8: "Deep Endometriosis"
}
for i in range(num_classes):
    class_name = class_names[i]
    print(f"Class '{class_name}':")
    print("  True Positives:", TP[i])
    print("  False Positives:", FP[i])
    print("  False Negatives:", FN[i])
    print("  total detected:", total_detected_boxes[i])
    print("  total GT:", total_gt_boxes[i])

import pandas as pd
from write_func import write_to_gsheet

data = {
    'Class': [class_names[i] for i in range(len(TP))],
    'True Positives': TP,
    'False Positives': FP,
    'False Negatives': FN,
    'Detected' : total_detected_boxes,
    'Annotated' : total_gt_boxes,
    'precision': precision,
    'sensitivity': sensitivity,
    'accuracy': accuracy,
    'specificity': specificity,
    'F_scor': f1_score
}

data_df = pd.DataFrame(data,index = [class_names[i] for i in range(len(TP))])


sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1PbPw7fjmEQ1oxkJUGaGMgjEeLeD_62_q3XdSnzBnmkU'
sheetName = str(datetime.date.today())
write_to_gsheet(sfpath, sheetID, sheetName, data_df)