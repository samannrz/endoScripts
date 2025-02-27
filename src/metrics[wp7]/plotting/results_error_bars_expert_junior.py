import os

import matplotlib.pyplot as plt
import json
from statistics import mean as mean
from statistics import stdev as std
plt.subplots(figsize=(3, 4))

Version = 'V2'
metric = 'NSD' # DICE
train_data = 'expert_consensus_junior_consensus'
plt.subplots(figsize=(4, 3))

x_Treat = [1, 2, 3]
x_Check = [1.2, 2.2, 3.2]
path_results = '../json_results/V2'

if metric == 'DICE':
    with open(os.path.join(path_results,'DICE_models_' + train_data + '_' + 'Treat'), 'r') as f:
        NSDs_Treat = json.load(f)
    with open(os.path.join(path_results,'DICE_models_' + train_data + '_' + 'Check'), 'r') as f:
        NSDs_Check = json.load(f)
    with open(os.path.join(path_results,'DICE_models_' + 'consensus' + '_' + 'Treat'), 'r') as f:
        NSDs_Treat_consensus = json.load(f)
    with open(os.path.join(path_results,'DICE_models_' + 'consensus' + '_' + 'Check'), 'r') as f:
        NSDs_Check_consensus = json.load(f)
if metric == 'NSD':
    with open(os.path.join(path_results,'NSD_models_' + train_data + '_' + 'Treat'), 'r') as f:
        NSDs_Treat = json.load(f)
    with open(os.path.join(path_results,'NSD_models_' + train_data + '_' + 'Check'), 'r') as f:
        NSDs_Check = json.load(f)
    with open(os.path.join(path_results, 'NSD_models_' + 'consensus' + '_' + 'Treat'), 'r') as f:
        NSDs_Treat_consensus = json.load(f)
    with open(os.path.join(path_results, 'NSD_models_' + 'consensus' + '_' + 'Check'), 'r') as f:
        NSDs_Check_consensus = json.load(f)

NSD_deeplab_Treat = NSDs_Treat_consensus[0]
NSD_deeplab_Check = NSDs_Check_consensus[0]
NSD_deeplab_expert_Treat = NSDs_Treat[0]
NSD_deeplab_expert_Check = NSDs_Check[0]
NSD_deeplab_junior_Treat = NSDs_Treat[1]
NSD_deeplab_junior_Check = NSDs_Check[1]

y_Treat = [mean(NSD_deeplab_Treat),mean(NSD_deeplab_expert_Treat), mean(NSD_deeplab_junior_Treat)]
y_Check = [mean(NSD_deeplab_Check),mean(NSD_deeplab_expert_Check), mean(NSD_deeplab_junior_Check)]

y_error_Treat = [std(NSD_deeplab_Treat) ** 2,std(NSD_deeplab_expert_Treat) ** 2, std(NSD_deeplab_junior_Treat) ** 2]
y_error_Check = [std(NSD_deeplab_Check) ** 2, std(NSD_deeplab_expert_Check) ** 2, std(NSD_deeplab_junior_Check) ** 2]

colors = ['black', 'red', 'blue']
colors2 = ['gray', 'pink', 'cyan']

plt.errorbar([], [], yerr=[], fmt='o', markerfacecolor='red', markeredgecolor='red',
             ecolor='red', elinewidth=3, capsize=6, label='Treat')
plt.errorbar([], [], yerr=[], fmt='o', markerfacecolor='green', markeredgecolor='green',
             ecolor='green', elinewidth=3, capsize=6, label='Check')

# Add legend
plt.legend()
for i in range(3):
    print(i)
    plt.errorbar(x_Treat[i], y_Treat[i], yerr=y_error_Treat[i], fmt='o', ecolor='red',
                 markerfacecolor='red', markeredgecolor='red' , elinewidth=3, barsabove=True,
                 capsize=6, capthick=2,label='Treat')

    plt.errorbar(x_Check[i], y_Check[i], yerr=y_error_Check[i], fmt='o', ecolor='green',
                 markerfacecolor = 'green',markeredgecolor='green' , elinewidth=3, barsabove=True,
                 capsize=6, capthick=2,label='Check')
    if i==0:
        plt.scatter([x_Treat[i]] * len(NSD_deeplab_Treat), NSD_deeplab_Treat, color='pink', marker='x')
        plt.scatter([x_Check[i]] * len(NSD_deeplab_Check), NSD_deeplab_Check, color='lightgreen', marker='x')
    elif i==1:
        plt.scatter([x_Treat[i]] * len(NSD_deeplab_expert_Treat), NSD_deeplab_expert_Treat, color='pink', marker='x')
        plt.scatter([x_Check[i]] * len(NSD_deeplab_expert_Check), NSD_deeplab_expert_Check, color='lightgreen', marker='x')
    else:
        plt.scatter([x_Treat[i]] * len(NSD_deeplab_junior_Treat), NSD_deeplab_junior_Treat, color='pink', marker='x')
        plt.scatter([x_Check[i]] * len(NSD_deeplab_junior_Check), NSD_deeplab_junior_Check, color='lightgreen',
                    marker='x')


# plt.xticks(x_Treat, ['Consensus', 'Experts', 'Juniors'])
# plt.ylabel(metric)
# plt.grid(axis='y', linestyle='--')

plt.xticks(x_Check, ['Consensus', 'Experts', 'Juniors'])
plt.ylabel(metric)
plt.grid(axis = 'y',linestyle = '--')

# Show plot
# plt.savefig('metrics[wp7]/figures/'+Version+ '/' + metric+ '_' + train_data + '_' + class_label,orientation='portrait',bbox_inches = 'tight')
# Show plot
plt.savefig('../figures/'+Version+ '/' + metric + '_' + train_data , orientation='portrait',
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
