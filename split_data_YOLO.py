import os
import shutil
import pickle
import datetime

label_path = '/data/projects/datasets/LesionLabelsYOLO'
image_path = '/data/projects/datasets/LesionDatasetImages'
test_image_path = '/data/projects/datasets/coco128/images/test'
train_image_path = '/data/projects/datasets/coco128/images/train2017'
valid_image_path = '/data/projects/datasets/coco128/images/valid'
train_label_path = '/data/projects/datasets/coco128/labels/train2017'
test_label_path = '/data/projects/datasets/coco128/labels/test'
valid_label_path = '/data/projects/datasets/coco128/labels/valid'
if os.path.exists(test_image_path):
    shutil.rmtree(test_image_path)
    shutil.rmtree(test_label_path)
    shutil.rmtree(train_image_path)
    shutil.rmtree(train_label_path)
    shutil.rmtree(valid_image_path)
    shutil.rmtree(valid_label_path)
os.makedirs(test_image_path)
os.makedirs(test_label_path)
os.makedirs(train_image_path)
os.makedirs(train_label_path)
os.makedirs(valid_image_path)
os.makedirs(valid_label_path)


dict_file = 'data_split_'+str(datetime.date.today())+'.pkl'

file = open(dict_file, 'rb')
data_dict = pickle.load(file)
file.close()

# Move the JSON files and their corresponding PNG files to the appropriate folders
for png_file in data_dict['train']:
    txt_file = png_file.replace('.png','.txt')
    shutil.copy(os.path.join(label_path, txt_file), train_label_path)
    shutil.copy(os.path.join(image_path, png_file), train_image_path)

for png_file in data_dict['test']:
    txt_file = png_file.replace('.png', '.txt')
    shutil.copy(os.path.join(label_path, txt_file), test_label_path)
    shutil.copy(os.path.join(image_path, png_file), test_image_path)

for png_file in data_dict['valid']:
    txt_file = png_file.replace('.png', '.txt')
    shutil.copy(os.path.join(label_path, txt_file), valid_label_path)
    shutil.copy(os.path.join(image_path, png_file), valid_image_path)

