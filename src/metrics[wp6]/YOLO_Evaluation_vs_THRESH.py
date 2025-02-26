import numpy as np
import matplotlib.pyplot as plt
from YOLO_Evaluation_V3 import evaluate_detections, class_names  # Import your function

# Define thresholds from 0.1 to 1 with 0.1 step
thresholds = np.arange(0.1, 1.1, 0.1)

# Storage for precision, recall, and F1-score averages
avg_precisions = []
avg_recalls = []
avg_f1_scores = []

folder_gt = "/data/projects/datasets/coco128-2023-06-28-2/labels/test"
folder_detect = "/data/projects/yolov5/runs/detect/exp/labels"

for thresh in thresholds:
    results, _ = evaluate_detections(folder_gt, folder_detect, iou_threshold=thresh)

    # Extract the average metrics[wp7] across all classes
    print(thresh)
    print(results)
    print('\n')
    avg_precision = np.mean([res["Precision"] for res in results.values()])
    avg_recall = np.mean([res["Recall"] for res in results.values()])
    avg_f1_score = np.mean([res["F1-score"] for res in results.values()])

    avg_precisions.append(avg_precision)
    avg_recalls.append(avg_recall)
    avg_f1_scores.append(avg_f1_score)

# Plot results
plt.figure(figsize=(8, 6))
plt.plot(thresholds, avg_precisions, label="Precision", marker="o")
plt.plot(thresholds, avg_recalls, label="Recall", marker="s")
plt.plot(thresholds, avg_f1_scores, label="F1-score", marker="^")

plt.xlabel("IoU Threshold")
plt.ylabel("Score")
plt.title("Precision, Recall, and F1-score vs IoU Threshold")
plt.legend()
plt.grid(True)

# Save plot
plt.savefig("metrics_vs_threshold.png", dpi=300, bbox_inches="tight")
plt.show()
