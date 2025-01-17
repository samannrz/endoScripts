import os

import matplotlib.pyplot as plt
import json
from statistics import mean as mean
from statistics import stdev as std
Version = 'V2'
class_label = 'Check'
metric = 'DICE'
train_data = 'consensus'
plt.subplots(figsize=(3, 4))

class_label = 'Treat'
metric = 'NSD'
train_data = 'all'
plt.subplots(figsize=(4, 3))

x_Treat = [1, 2, 3]
x_Check = [1.2, 2.2, 3.2]
path_results = '../json_results/V2'
if metric == 'NSD':
    with open(os.path.join(path_results,'NSD_models_'+ train_data + '_' + class_label), 'r') as f:
        NSDs = json.load(f)
if metric == 'DICE':
    with open(os.path.join(path_results,'DICE_models_'+ train_data + '_' + class_label), 'r') as f:
        NSDs = json.load(f)
        print('hello?')
    with open(os.path.join(path_results,'NSD_models_' + train_data + '_' + 'Treat'), 'r') as f:
        NSDs_Treat = json.load(f)
    with open(os.path.join(path_results,'NSD_models_' + train_data + '_' + 'Check'), 'r') as f:
        NSDs_Check = json.load(f)
if metric == 'DICE':
    with open(os.path.join(path_results,'DICE_models_' + train_data + '_' + 'Treat'), 'r') as f:
        NSDs_Treat = json.load(f)
    with open(os.path.join(path_results,'DICE_models_' + train_data + '_' + 'Check'), 'r') as f:
        NSDs_Check = json.load(f)
if metric == 'NSD':
    with open(os.path.join(path_results,'NSD_models_' + train_data + '_' + 'Treat'), 'r') as f:
        NSDs_Treat = json.load(f)
    with open(os.path.join(path_results,'NSD_models_' + train_data + '_' + 'Check'), 'r') as f:
        NSDs_Check = json.load(f)

NSD_deeplab_Treat = NSDs_Treat[0]
NSD_fasterViT_Treat = NSDs_Treat[1]
NSD_maskFormer_Treat = NSDs_Treat[2]
NSD_deeplab_Check = NSDs_Check[0]
NSD_fasterViT_Check = NSDs_Check[1]
NSD_maskFormer_Check = NSDs_Check[2]

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

plt.xticks(x_Check, ['DeeplabV3', 'FasterViT', 'Mask2Former'])
plt.ylabel(metric)
plt.grid(axis = 'y',linestyle = '--')

# Show plot
# plt.savefig('metrics/figures/'+Version+ '/' + metric+ '_' + train_data + '_' + class_label,orientation='portrait',bbox_inches = 'tight')
# Show plot
plt.savefig('metrics/figures/'+Version+ '/' + metric + '_' + train_data , orientation='portrait',
            bbox_inches='tight')
############
###### Simple Bar Plots #####
# plt.clf

# # Bar widths and offsets for Treat and Check bars
# bar_width = 0.4
# x_Treat = [1, 2, 3]  # Base x positions for Treat bars
# x_Check = [x + bar_width for x in x_Treat]  # Offset x positions for Check bars
#
# # Create bar plots for Treat and Check
# plt.bar(x_Treat, y_Treat, yerr=y_error_Treat, width=bar_width, color='red', label='Treat', capsize=5, alpha=0.7)
# plt.bar(x_Check, y_Check, yerr=y_error_Check, width=bar_width, color='green', label='Check', capsize=5, alpha=0.7)
#
# # Add labels and legend
# plt.xticks([x + bar_width / 2 for x in x_Treat], ['DeeplabV3', 'FasterViT', 'Mask2Former'])  # Center x-ticks
# plt.ylabel(metric)
# plt.legend()
# plt.grid(axis='y', linestyle='--')
#
# # Show the plot
# plt.savefig(os.path.join('../figures/',Version,'/BAR_' + metric + '_' + train_data) , orientation='portrait',
#              bbox_inches='tight')
# plt.tight_layout()
# plt.show()
