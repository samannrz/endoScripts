import os

import matplotlib.pyplot as plt
import json
from statistics import mean as mean
from statistics import stdev as std

metric = 'NSD'
train_data = 'all'
plt.subplots(figsize=(3, 4))

common_path = '/data/DATA/Incision_predictions/test-1-28_'
j = 0
color = ['red', 'green']
color_point = ['pink', 'lightgreen']

for class_label in ['Treat', 'Check']:
    with open('metrics/json_results/' + metric + '_annotator_' + train_data + '_' + class_label, 'r') as f:
        NSDs_model = json.load(f)
    with open('metrics/json_results/' + metric + '_annotator_' + train_data + '_' + class_label, 'r') as f:
        NSDs_annotator = json.load(f)
    print(len(NSDs_annotator))
    NSD_e1, NSD_e2, NSD_e3, NSD_e4, NSD_j1, NSD_j2 = NSDs_annotator[0:6]
    NSD_fasterViT = NSDs_model[1]

    y = [mean(NSD_e1), mean(NSD_e2), mean(NSD_e3), mean(NSD_e4), mean(NSD_j1), mean(NSD_j2), mean(NSD_fasterViT)]

    y_error = [std(NSD_e1) ** 2, std(NSD_e2) ** 2, std(NSD_e3) ** 2, std(NSD_e4) ** 2, std(NSD_j1) ** 2,
               std(NSD_j2) ** 2, std(NSD_fasterViT)]

    for i in range(7):
        plt.errorbar(i + j, y[i], yerr=y_error[i], fmt='o', ecolor=color[j * 10], elinewidth=3, barsabove=True,
                     capsize=6, capthick=2)

    for i, y in enumerate(NSDs):
        plt.scatter([i + j] * len(y), y, color=color_point[j * 10], marker='x')

    plt.xticks(list(range(0, 7)), ['Expert1', 'Expert2', 'Expert3', 'Expert4', 'Junior1', 'Junior2'])
    plt.ylabel(metric)
    plt.grid(axis='y', linestyle='--')

    # Show plot
    plt.savefig('metrics/figures/human_machine_' + metric + '_' + train_data, orientation='portrait',
                bbox_inches='tight')
    j += 0.1
