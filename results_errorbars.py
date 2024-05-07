import os

import matplotlib.pyplot as plt
import json
from statistics import mean as mean
from statistics import stdev as std
class_label = 'Check'
metric = 'DICE'
train_data = 'consensus'
plt.subplots(figsize=(3, 4))

x = [1, 1.5, 2]
if metric == 'NSD':
    with open('metrics/json_results/NSD_models_'+ train_data + '_' + class_label, 'r') as f:
        NSDs = json.load(f)
if metric == 'DICE':
    with open('metrics/json_results/DICE_models_'+ train_data + '_' + class_label, 'r') as f:
        NSDs = json.load(f)

NSD_deeplab = NSDs[0]
NSD_fasterViT = NSDs[1]
NSD_maskFormer = NSDs[2]

y = [mean(NSD_deeplab), mean(NSD_fasterViT), mean(NSD_maskFormer)]
y_error = [std(NSD_deeplab) ** 2, std(NSD_fasterViT) ** 2, std(NSD_maskFormer) ** 2]

colors = ['black', 'red', 'blue']
colors2 = ['gray', 'pink', 'cyan']

for i in range(3):
    plt.errorbar(x[i], y[i], yerr=y_error[i], fmt='o', ecolor=colors[i], elinewidth=3, barsabove=True, capsize=6,
                 capthick=2)

for i, y in enumerate(NSDs):
    plt.scatter([x[i]] * len(y), y, color=colors2[i], marker='x')

plt.xticks(x, ['DeeplabV3', 'FasterViT', 'Mask2Former'])
plt.ylabel(metric)
plt.grid(axis = 'y',linestyle = '--')

# Show plot
plt.savefig('metrics/figures/'+metric+ '_' +train_data + '_' + class_label,orientation='portrait',bbox_inches = 'tight')
