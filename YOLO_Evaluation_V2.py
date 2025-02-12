import datetime
import os
import time

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from write_yolo_results_to_gsheet import write_results_to_google_sheet

def calculate_iou(box1, box2):
    """
    Calculate Intersection over Union (IoU) between two boxes.
    Each box is represented as [x_center, y_center, width, height].
    """
    # Convert boxes to (x1, y1, x2, y2) format
    box1_x1 = box1[0] - box1[2] / 2
    box1_y1 = box1[1] - box1[3] / 2
    box1_x2 = box1[0] + box1[2] / 2
    box1_y2 = box1[1] + box1[3] / 2

    box2_x1 = box2[0] - box2[2] / 2
    box2_y1 = box2[1] - box2[3] / 2
    box2_x2 = box2[0] + box2[2] / 2
    box2_y2 = box2[1] + box2[3] / 2

    # Calculate intersection area
    x1 = max(box1_x1, box2_x1)
    y1 = max(box1_y1, box2_y1)
    x2 = min(box1_x2, box2_x2)
    y2 = min(box1_y2, box2_y2)
    intersection = max(0, x2 - x1) * max(0, y2 - y1)

    # Calculate union area
    box1_area = box1[2] * box1[3]
    box2_area = box2[2] * box2[3]
    union = box1_area + box2_area - intersection

    # Avoid division by zero
    if union == 0:
        return 0
    return intersection / union

############################################
################################################
import os
import numpy as np

# Define class names including "Background" for false positives
class_names = {
    0: "Adh Dense",
    1: "Adh Filmy",
    2: "Sup Black",
    3: "Sup White",
    4: "Sup Red",
    5: "Sup Subtle",
    6: "Ov. Endometrioma",
    7: "Ov. Chocolate Fluid",
    8: "Deep Endometriosis",
}
############################
#############################
def evaluate_detections(folder_gt, folder_detect, iou_threshold=0.2):
    """
    Evaluate object detection results by comparing detected boxes to ground truth boxes.

    Args:
        folder_gt (str): Path to the folder containing ground truth annotation files.
        folder_detect (str): Path to the folder containing detection result files.
        iou_threshold (float): IoU threshold to consider a detection as a true positive.

    Returns:
        results (dict): A dictionary containing precision, recall, and F1-score for each class.
        confusion_matrix (np.array): A confusion matrix of shape (num_classes + 1, num_classes + 1).
    """
    # Add an extra class for background (last index)
    num_classes = len(class_names)
    background_class_id = num_classes  # Background class
    confusion_matrix = np.zeros((num_classes + 1, num_classes + 1), dtype=int)

    # Initialize class counts for TP, FP, FN
    class_counts = {class_id: {"TP": 0, "FP": 0, "FN": 0} for class_id in class_names.keys()}
    class_counts[background_class_id] = {"TP": 0, "FP": 0, "FN": 0}  # Track background

    # Iterate over all ground truth files
    for filename in os.listdir(folder_gt):
        if not filename.endswith(".txt"):
            continue

        gt_path = os.path.join(folder_gt, filename)
        detect_path = os.path.join(folder_detect, filename)

        # Load ground truth boxes
        gt_boxes = []
        with open(gt_path, "r") as f:
            for line in f:
                class_id, x_center, y_center, width, height = map(float, line.strip().split())
                gt_boxes.append([int(class_id), x_center, y_center, width, height])

        # Load detected boxes if file exists
        detect_boxes = []
        if os.path.exists(detect_path):
            with open(detect_path, "r") as f:
                for line in f:
                    class_id, x_center, y_center, width, height = map(float, line.strip().split())
                    detect_boxes.append([int(class_id), x_center, y_center, width, height])

        # Track matched ground truth and detected boxes
        matched_gt = set()
        matched_detect = set()

        # Match detected boxes to ground truth boxes
        for i, detect_box in enumerate(detect_boxes):
            best_iou = 0
            best_gt_idx = -1

            # Find best matching ground truth box
            for j, gt_box in enumerate(gt_boxes):
                if j in matched_gt:
                    continue  # Skip already matched ground truths

                iou = calculate_iou(detect_box[1:], gt_box[1:])
                if filename == 'P-0072_Video001_trim_2.mp4_01158.txt':
                    print(gt_box)
                    print(iou)
                if iou > best_iou:
                    best_iou = iou
                    best_gt_idx = j

            # If IoU is above threshold, we have a valid match
            if best_iou > iou_threshold:
                matched_gt.add(best_gt_idx)  # Mark ground truth as matched
                matched_detect.add(i)  # Mark detection as matched
                gt_class = gt_boxes[best_gt_idx][0]
                pred_class = detect_box[0]

                if gt_class == pred_class:
                    # True Positive (correct detection)
                    confusion_matrix[gt_class, gt_class] += 1
                    class_counts[gt_class]["TP"] += 1
                else:
                    # Misclassification (Class B detected as Class A)
                    confusion_matrix[gt_class, pred_class] += 1
                    class_counts[gt_class]["FN"] += 1  # Ground truth missed
                    class_counts[pred_class]["FP"] += 1  # Predicted class incorrect
            else:
                # False positive - detection does not match any ground truth
                pred_class = detect_box[0]
                confusion_matrix[background_class_id, pred_class] += 1  # FP against background
                class_counts[pred_class]["FP"] += 1

        # Unmatched ground truth boxes (False Negatives)
        for j, gt_box in enumerate(gt_boxes):
            if j not in matched_gt:
                gt_class = gt_box[0]
                confusion_matrix[gt_class, background_class_id] += 1  # False Negative
                class_counts[gt_class]["FN"] += 1

        # Handle background (False Positives on background)
        if len(detect_boxes) == 0 and len(gt_boxes) == 0:
            confusion_matrix[background_class_id, background_class_id] += 1  # True Negative (background correctly detected)
        elif len(detect_boxes) > 0 and len(gt_boxes) == 0:
            for detect_box in detect_boxes:
                pred_class = detect_box[0]
                confusion_matrix[background_class_id, pred_class] += 1  # FP on background
                class_counts[background_class_id]["FP"] += 1

    # Calculate Precision, Recall, and F1-score for each class
    results = {}
    for class_id, counts in class_counts.items():
        TP = counts["TP"]
        FP = counts["FP"]
        FN = counts["FN"]

        precision = TP / (TP + FP) if (TP + FP) > 0 else 0
        recall = TP / (TP + FN) if (TP + FN) > 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

        results[class_id] = {
            "Precision": precision,
            "Recall": recall,
            "F1-score": f1_score,
        }

    return results, confusion_matrix
############################
# MAIN
THRESH = .2
folder_gt = "/data/projects/datasets/coco128-2023-06-28-2/labels/test"
folder_detect = "/data/projects/yolov5/runs/detect/exp/labels"
results, confusion_matrix = evaluate_detections(folder_gt, folder_detect,iou_threshold=THRESH)

###################################
#####################################
print()
# Define class names, including background
class_names = {
    0: "Adh Dense",
    1: "Adh Filmy",
    2: "Sup Black",
    3: "Sup White",
    4: "Sup Red",
    5: "Sup Subtle",
    6: "Ov. Endometrioma",
    7: "Ov. Chocolate Fluid",
    8: "Deep Endometriosis",
}
class_names[len(class_names)] = "Background"  # Adding background class

# Convert confusion matrix to DataFrame
confusion_matrix_df = pd.DataFrame(confusion_matrix, index=class_names.values(), columns=class_names.values())

# Plot confusion matrix
plt.figure(figsize=(10, 8))
sns.heatmap(confusion_matrix_df, annot=True, fmt="d", cmap="Blues", cbar=False)

plt.title("Confusion Matrix")
plt.xlabel("Predicted")
plt.ylabel("Actual")
# Save the plot to a file
plt.savefig("confusion_matrix_plot.png", dpi=300, bbox_inches="tight")  # bbox_inches="tight" ensures no parts are cut off

plt.close()
##############################
##############################


json_keyfile = 'keycode/my-gpysheets-3d8d13442005.json'  # Replace with your JSON key file path
sheet_name = "Evaluation Results"+ str(THRESH)+'-'+str(datetime.date.today()) # Replace with your Google Sheet name
sheet_id = '1PbPw7fjmEQ1oxkJUGaGMgjEeLeD_62_q3XdSnzBnmkU'
write_results_to_google_sheet(results, sheet_id,sheet_name, json_keyfile)