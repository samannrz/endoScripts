import os
import shutil
import pickle


label_path = '/data/projects/datasets/LesionLabelsFRCNN'
image_path = '/data/projects/datasets/LesionDatasetImages'
test_image_path = '/data/projects/datasets/dataFasterRCNN/test'
train_image_path = '/data/projects/datasets/dataFasterRCNN/train'
valid_image_path = '/data/projects/datasets/dataFasterRCNN/valid'
train_label_path = train_image_path
test_label_path = test_image_path
valid_label_path = valid_image_path
if os.path.exists(test_image_path):
    shutil.rmtree(test_image_path)
    shutil.rmtree(train_image_path)
    shutil.rmtree(valid_image_path)
os.makedirs(test_image_path)
os.makedirs(train_image_path)
os.makedirs(valid_image_path)


dict_file = 'pkl_files/data_split.pkl'

file = open(dict_file, 'rb')
data_dict = pickle.load(file)
file.close()

# Move the JSON files and their corresponding PNG files to the appropriate folders
for png_file in data_dict['train']:
    json_file = png_file.replace('.png','.json')
    shutil.copy(os.path.join(label_path, json_file), train_label_path)
    shutil.copy(os.path.join(image_path, png_file), train_image_path)

for png_file in data_dict['test']:
    json_file = png_file.replace('.png', '.json')
    shutil.copy(os.path.join(label_path, json_file), test_label_path)
    shutil.copy(os.path.join(image_path, png_file), test_image_path)

for png_file in data_dict['valid']:
    json_file = png_file.replace('.png', '.json')
    shutil.copy(os.path.join(label_path, json_file), valid_label_path)
    shutil.copy(os.path.join(image_path, png_file), valid_image_path)

