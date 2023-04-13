import os
import random
import shutil
import pickle
import numpy as np


def remove_redundant_data(files, sample_rate):
    files.sort()
    file_names = [p[:-10] for p in png_files]
    frame_num = [p[-9:-4] for p in png_files]
    select_file = [file_names[0]]
    select_frame = [frame_num[0]]
    for ind in range(1, len(file_names)):
        if select_file[-1] != file_names[ind]:
            select_file.append(file_names[ind])
            select_frame.append(frame_num[ind])
        else:
            if file_names[ind].startswith('2019-11-19_122223_VID013'):
                aug = 10
            else:
                aug = 0
            if int(frame_num[ind]) - int(select_frame[-1]) > sample_rate + aug - 1:
                select_file.append(file_names[ind])
                select_frame.append(frame_num[ind])
    return select_file, select_frame


dir_path = '/data/projects/dataset/LesionDatasetImages'
dict_file = 'data_split'
split_dict = {'train': [], 'test': [], 'valid': []}

# List all the png files in the directory
png_files = [f for f in os.listdir(dir_path) if f.endswith('.png')]
print('Total files: %s' % len(png_files))

file_names, frame_number = remove_redundant_data(png_files, 5)
print('Total files (after sampling redundants): %s' % len(file_names))

with open('surgeries.txt', 'w') as ff:
    for i in range(len(file_names)):
        ff.write(file_names[i] + '  ' + frame_number[i] + '\n')

surgeries = []
for file in file_names:
    if file.startswith('P') or file.startswith('MCLO'):
        surgeries.append(file[:7])
    elif file.startswith('FCF1'):
        surgeries.append(file[:20])
    elif file.startswith('Surgery') or file.startswith('surgery'):
        surgeries.append(file[:9])
    else:  # file.startswith('2022') or '2021' or '2020'or '2019':
        surgeries.append(file[:17])

unique_surgeries = list(set(surgeries))
# with open('surgeries_unique.txt', 'w') as ff:
#     for i in range(len(unique_surgeries)):
#         ff.write(unique_surgeries[i]+ '\n')
num_surgeries = len(unique_surgeries)
print('Num of surgeries: %s' % num_surgeries)

# Shuffle the list of surgery files
random.shuffle(unique_surgeries)
# Split the list of surgery files into three parts
train_surg, valid_surg, test_surg = np.split(unique_surgeries, [int(num_surgeries * 0.87), int(num_surgeries * 0.95)])
print('Num of Train surgeries: %d' %len(train_surg))
print('Num of Test surgeries: %d' %len(test_surg))
print('Num of Valid surgeries: %d' %len(valid_surg))
final_files= [file_names[i]+'_'+frame_number[i]+'.png' for i in range(len(file_names))]
for f in train_surg:
    train_files = [string for string in final_files if any(string.startswith(prefix) for prefix in train_surg)]
for f in test_surg:
    test_files = [string for string in final_files if any(string.startswith(prefix) for prefix in test_surg)]
for f in valid_surg:
    valid_files = [string for string in final_files if any(string.startswith(prefix) for prefix in valid_surg)]
split_dict['train']=train_files
split_dict['test'] =test_files
split_dict['valid']=valid_files

#### Finalyzing ######
print('Num of Train files: %d' %len(train_files))
print('Num of Test files: %d' %len(test_files))
print('Num of Valid files: %d' %len(valid_files))
print('Total files sum: %d' % (len(valid_files)+len(train_files)+len(test_files)))
with open(dict_file + '.pkl', 'wb') as fp:
    pickle.dump(split_dict, fp)
    print('dictionary saved successfully to %s' % dict_file + '.pkl')
