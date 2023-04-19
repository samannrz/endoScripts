import datetime
import os.path
import pickle
import argparse

import pandas as pd
from functions import write_to_gsheet

CLASSES = [
    'Adhesions.Dense', 'Adhesions.Filmy', 'Superficial.Black', 'Superficial.White',
    'Superficial.Red', 'Superficial.Subtle', 'Ovarian.Endometrioma[B]', 'Ovarian.Chocolate Fluid', 'Deep Endometriosis'
]
# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('--dict_name', type=str, required=True, help='name of the data_split dict')
# file_name = parser.parse_args().dict_name
file_name = 'data_split_'+str(datetime.date.today())+'.pkl'

def class_stats(labels):
    instances = [0] * len(CLASSES)
    frame_num = [0] * len(CLASSES)
    for label in labels:
        with open(os.path.join(labels_path, label)) as label_file:
            already_counted = [False] * len(CLASSES)
            for line in label_file:
                cl = int(line[0])
                instances[cl] += 1
                if not already_counted[cl]:
                    frame_num[cl] = frame_num[cl] + 1
                    already_counted[cl] = True
    return instances, frame_num



file = open(file_name, 'rb')
data_dict = pickle.load(file)
file.close()

labels_path = '/data/projects/datasets/LesionLabelsYOLO'

train_label_files = [f[:-3] + 'txt' for f in data_dict['train']]
train_instances, train_frame_num = class_stats(train_label_files)

valid_label_files = [f[:-3] + 'txt' for f in data_dict['valid']]
valid_instances, valid_frame_num = class_stats(valid_label_files)

test_label_files = [f[:-3] + 'txt' for f in data_dict['test']]
test_instances, test_frame_num = class_stats(test_label_files)
###############################################################
stat = [train_instances, train_frame_num, valid_instances, valid_frame_num, test_instances, test_frame_num]
statsum = [sum(row) for row in stat]

stat_df = pd.DataFrame(stat, columns=CLASSES,
                       index=['train instances', 'train frames', 'validation instances', 'validation frames',
                              'test instances', 'test frames'])
stat_df['Total'] = statsum
stat_df['Surgeries'] = [len(data_dict['train_surg']), '', len(data_dict['valid_surg']),'',len(data_dict['test_surg']), '']
stat_df['Frames'] = [len(data_dict['train']), '', len(data_dict['valid']),'',len(data_dict['test']), '']

print(stat_df)
write_to_gsheet('keycode/my-gpysheets-3d8d13442005.json', '1zc_KLrf11ipLkpvaf0eYjb4l1vK8vyUfYp2mKY8ubAE',
                'split_' + str(datetime.date.today()), stat_df)
