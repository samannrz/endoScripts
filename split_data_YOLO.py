import os
import random
import shutil
import pickle


label_path = '/data/projects/dataset/LesionLabelsYOLO'
dict_file = 'data_split.pkl'

# List all the JSON files in the directory
# json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]

file = open(dict_file, 'rb')
data_dict = pickle.load(file)
file.close()
print(data_dict)

# Move the JSON files and their corresponding JPEG files to the appropriate folders
# for png_file in test_files:
#     jpeg_file = json_file.replace('.json', '.jpg')
#     shutil.copy(os.path.join(dir_path, json_file), test_path)
#     shutil.copy(os.path.join(dir_path, jpeg_file), test_path)
#
# for json_file in valid_files:
#     jpeg_file = json_file.replace('.json', '.jpg')
#     shutil.copy(os.path.join(dir_path, json_file), valid_path)
#     shutil.copy(os.path.join(dir_path, jpeg_file), valid_path)
#
# for json_file in train_files:
#     jpeg_file = json_file.replace('.json', '.jpg')
#     shutil.copy(os.path.join(dir_path, json_file), train_path)
#     shutil.copy(os.path.join(dir_path, jpeg_file), train_path)
#
# with open(dict_file+'.pkl', 'wb') as fp:
#     pickle.dump(split_dict, fp)
#     print('dictionary saved successfully to %s', %dict_file)