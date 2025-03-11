import os

import matplotlib.pyplot as plt
import json
from statistics import mean as mean
from statistics import stdev as std


metric = 'NSD'
train_data = 'all'
plt.subplots(figsize=(3, 4))
Version='V2'
j = 0
color = ['red', 'green']
color_point = ['pink', 'lightgreen']
plt.subplots(figsize=(4, 3))

x_Treat = [1, 2, 3,4,5,6,7]
x_Check = [1.2, 2.2, 3.2,4.2,5.2,6.2,7.2]


for class_label in ['Treat', 'Check']:
    if class_label == 'Treat':
        j=0
    with open('../json_results/'+Version+'/' + metric + '_annotator_' + class_label, 'r') as f:
        NSDs_annotator = json.load(f)
    with open('../json_results/'+Version+'/' + metric + '_models_'+train_data+'_'+ class_label, 'r') as f:
        NSDs_model = json.load(f)
    NSD_e1, NSD_e2, NSD_e3, NSD_e4, NSD_j1, NSD_j2 = NSDs_annotator[0:6]
    NSD_fasterViT = NSDs_model[0]

    y = [mean(NSD_e1), mean(NSD_e2), mean(NSD_e4), mean(NSD_e3), mean(NSD_j1), mean(NSD_j2), mean(NSD_fasterViT)]

    y_error = [std(NSD_e1) ** 2, std(NSD_e2) ** 2, std(NSD_e4) ** 2,std(NSD_e3) ** 2, std(NSD_j1) ** 2,
               std(NSD_j2) ** 2, std(NSD_fasterViT) ** 2]

    for i in range(7):
        plt.errorbar(i + j, y[i], yerr=y_error[i], fmt='o', ecolor=color[int(j/2 * 10)], elinewidth=3, barsabove=True,
                     capsize=6, capthick=2, markerfacecolor=color[int(j/2 * 10)], markeredgecolor=color[int(j/2 * 10)])
    NSDs_annotator.append(NSD_fasterViT)
    for i, y in enumerate(NSDs_annotator):
        plt.scatter([i + j] * len(y), y, color=color_point[int(j/2 * 10)], marker='x')

    plt.xticks(list(range(0, 7)), ['Expert1', 'Expert2', 'Expert3', 'Expert4', 'Junior1', 'Junior2','FasterViT'])
    plt.ylabel(metric)
    plt.grid(axis='y', linestyle='--')

    # Show plot
    j += 0.2
plt.errorbar([], [], yerr=[], fmt='o', markerfacecolor='red', markeredgecolor='red',
                 ecolor='red', elinewidth=3, capsize=6, label='Treat')
plt.errorbar([], [], yerr=[], fmt='o', markerfacecolor='green', markeredgecolor='green',
                 ecolor='green', elinewidth=3, capsize=6, label='Check')

    # Add legend
plt.legend(loc = 'lower center')
plt.tight_layout()  # This ensures the labels fit well inside the plot
plt.xticks(list(range(0, 7)), ['Expert1', 'Expert2', 'Expert3', 'Senior1', 'Junior1', 'Junior2', 'DeeplabV3'], rotation=45)
print('../figures/'+Version+'/human_machine_' + metric + '_' + train_data)
plt.savefig('../figures/'+Version+'/human_machine_' + metric + '_' + train_data, orientation='portrait',
            bbox_inches='tight')

