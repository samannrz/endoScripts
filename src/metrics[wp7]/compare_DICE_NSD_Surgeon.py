import os.path
from itertools import count

import pygsheets
from metrics_calculate import *


##### EXTRACT THE RESULTS OF THE SURGEON FROM THE RESPONDERS LINK IN GSHEET #####
gc = pygsheets.authorize(service_account_file="../../data/keycode/my-gpysheets-3d8d13442005.json")
sh = gc.open_by_key("1LZMVcWstjOJrGDJMl5j5c93Bwh1wpn1kCSgSopSZIkc")
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
NSD_treat = []
DICE_treat = []
for image in IMAGE_NAMES:
    fasterViT_image = os.path.join(mask_pred_path_fasterViT,image)
    gt_image = os.path.join(mask_gt_path,image)
    NSD_fasterViT, DICE_fasterViT, IOU_fasterViT = calculate_metrics(fasterViT_image, gt_image)
    NSD_treat.append (NSD_fasterViT[0])
    DICE_treat.append (DICE_fasterViT[0])
print(DICE_treat)
##### CHECK
class_label = 'Check'
mask_gt_path = '/data/DATA/incision/4/mask/' + class_label
mask_pred_path_fasterViT = os.path.join(common_path , 'FasterViT' , train_data, 'mask', class_label)
NSD_check = []
DICE_check = []
for image in IMAGE_NAMES:
    fasterViT_image = os.path.join(mask_pred_path_fasterViT,image)
    gt_image = os.path.join(mask_gt_path,image)
    NSD_fasterViT, DICE_fasterViT, IOU_fasterViT = calculate_metrics(fasterViT_image, gt_image)
    NSD_check.append (NSD_fasterViT[0])
    DICE_check.append (DICE_fasterViT[0])
print(DICE_check)
DICE = [(a + b) / 2 for a, b in zip(DICE_check, DICE_treat)]
NSD = [(a + b) / 2 for a, b in zip(NSD_check, NSD_treat)]

wks.update_values('B3:AO3',[DICE])
wks.update_values('B4:AO4',[NSD])
################################
########## ANALYSIS  ##############
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# Convert to numpy arrays for calculations
SURGEON = np.array(SURGEON)
SURGEON = SURGEON /100
DICE = np.array(DICE)
NSD = np.array(NSD)

# Compute Pearson and Spearman correlations
pearson_corr_dice, _ = stats.pearsonr(SURGEON, DICE)
spearman_corr_dice, _ = stats.spearmanr(SURGEON, DICE)

pearson_corr_nsd, _ = stats.pearsonr(SURGEON, NSD)
spearman_corr_nsd, _ = stats.spearmanr(SURGEON, NSD)

# Print the correlation results
print(f"Pearson correlation (SURGEON vs DICE): {pearson_corr_dice:.3f}")
print(f"Spearman correlation (SURGEON vs DICE): {spearman_corr_dice:.3f}")
print(f"Pearson correlation (SURGEON vs NSD): {pearson_corr_nsd:.3f}")
print(f"Spearman correlation (SURGEON vs NSD): {spearman_corr_nsd:.3f}")
error_surgeon_dice = np.mean(np.abs(np.array(SURGEON) - np.array(DICE)))
error_surgeon_nsd = np.mean(np.abs(np.array(SURGEON) - np.array(NSD)))

print(f"Average Error between SURGEON and DICE: {error_surgeon_dice}")
print(f"Average Error between SURGEON and NSD: {error_surgeon_nsd}")
##################################
####################################
# Plot scatter plots
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
plt.scatter(SURGEON, DICE, alpha=0.7)
plt.xlabel("SURGEON Scores")
plt.ylabel("DICE")
plt.title("SURGEON vs DICE")

plt.subplot(1, 2, 2)
plt.scatter(SURGEON, NSD, alpha=0.7)
plt.xlabel("SURGEON Scores")
plt.ylabel("NSD")
plt.title("SURGEON vs NSD")

plt.tight_layout()
plt.savefig("figures/METRICS_CORRELATION.png", dpi=300, bbox_inches='tight')

############
import matplotlib.pyplot as plt

x_values = list(range(1, 41))

plt.figure(figsize=(10, 6))
plt.plot(x_values, SURGEON, color='blue', marker='o', linestyle='-', label="SURGEON")
plt.plot(x_values, DICE, color='red', marker='s', linestyle='-', label="DICE")
plt.plot(x_values, NSD, color='green', marker='^', linestyle='-', label="NSD")

# Labels and legend
plt.xlabel("Index (1 to 40)")
plt.ylabel("Values")
plt.title("Comparison of METRICS")
plt.legend()
plt.grid(True)

plt.savefig("figures/METRICS_vs_IMAGE.png", dpi=300, bbox_inches='tight')

