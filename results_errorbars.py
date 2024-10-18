import os

import matplotlib.pyplot as plt
import json
from statistics import mean as mean
from statistics import stdev as std
<<<<<<< HEAD
class_label = 'Check'
metric = 'DICE'
train_data = 'consensus'
plt.subplots(figsize=(3, 4))
=======

class_label = 'Treat'
metric = 'DICE'
train_data = 'consensus'
plt.subplots(figsize=(3, 4))

x_Treat = [1, 2, 3]
x_Check = [1.2, 2.2, 3.2]
>>>>>>> 50694583d2ed8aec19ff33c4735999824f28aa5a

if metric == 'NSD':
<<<<<<< HEAD
    with open('metrics/json_results/NSD_models_'+ train_data + '_' + class_label, 'r') as f:
        NSDs = json.load(f)
if metric == 'DICE':
    with open('metrics/json_results/DICE_models_'+ train_data + '_' + class_label, 'r') as f:
        NSDs = json.load(f)
=======
    with open('metrics/json_results/NSD_models_' + train_data + '_' + 'Treat', 'r') as f:
        NSDs_Treat = json.load(f)
    with open('metrics/json_results/NSD_models_' + train_data + '_' + 'Check', 'r') as f:
        NSDs_Check = json.load(f)
if metric == 'DICE':
    with open('metrics/json_results/DICE_models_' + train_data + '_' + 'Treat', 'r') as f:
        NSDs_Treat = json.load(f)
    with open('metrics/json_results/DICE_models_' + train_data + '_' + 'Check', 'r') as f:
        NSDs_Check = json.load(f)

NSD_deeplab_Treat = NSDs_Treat[0]
NSD_fasterViT_Treat = NSDs_Treat[1]
NSD_maskFormer_Treat = NSDs_Treat[2]
NSD_deeplab_Check = NSDs_Check[0]
NSD_fasterViT_Check = NSDs_Check[1]
NSD_maskFormer_Check = NSDs_Check[2]
>>>>>>> 50694583d2ed8aec19ff33c4735999824f28aa5a

y_Treat = [mean(NSD_deeplab_Treat), mean(NSD_fasterViT_Treat), mean(NSD_maskFormer_Treat)]
y_Check = [mean(NSD_deeplab_Check), mean(NSD_fasterViT_Check), mean(NSD_maskFormer_Check)]

y_error_Treat = [std(NSD_deeplab_Treat) ** 2, std(NSD_fasterViT_Treat) ** 2, std(NSD_maskFormer_Treat) ** 2]
y_error_Check = [std(NSD_deeplab_Check) ** 2, std(NSD_fasterViT_Check) ** 2, std(NSD_maskFormer_Check) ** 2]

colors = ['black', 'red', 'blue']
colors2 = ['gray', 'pink', 'cyan']

for i in range(3):
    plt.errorbar(x_Treat[i], y_Treat[i], yerr=y_error_Treat[i], fmt='o', ecolor='red', elinewidth=3, barsabove=True,
                 capsize=6, capthick=2)
    plt.errorbar(x_Check[i], y_Check[i], yerr=y_error_Check[i], fmt='o', ecolor='green', elinewidth=3, barsabove=True,
                 capsize=6, capthick=2)

for i, y in enumerate(NSDs_Treat):
    plt.scatter([x_Treat[i]] * len(y), y, color='pink', marker='x')
for i, y in enumerate(NSDs_Check):
    plt.scatter([x_Check[i]] * len(y), y, color='lightgreen', marker='x')
    print(i)

plt.xticks(x_Treat, ['DeeplabV3', 'FasterViT', 'Mask2Former'])
plt.ylabel(metric)
plt.grid(axis='y', linestyle='--')

<<<<<<< HEAD
plt.xticks(x, ['DeeplabV3', 'FasterViT', 'Mask2Former'])
plt.ylabel(metric)
plt.grid(axis = 'y',linestyle = '--')

# Show plot
plt.savefig('metrics/figures/'+metric+ '_' +train_data + '_' + class_label,orientation='portrait',bbox_inches = 'tight')
=======
# Show plot
plt.savefig('metrics/figures/' + metric + '_' + train_data , orientation='portrait',
            bbox_inches='tight')
>>>>>>> 50694583d2ed8aec19ff33c4735999824f28aa5a
