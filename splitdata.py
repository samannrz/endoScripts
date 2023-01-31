import os
import random
import shutil

dir_path = '/LesionDataset/LesionDataset'
test_path = '/media/saman/data/PycharmProjects/endoDetection/data/test'
train_path = '/media/saman/data/PycharmProjects/endoDetection/data/train'
valid_path = '/media/saman/data/PycharmProjects/endoDetection/data/valid'

# List all the JSON files in the directory
json_files = [f for f in os.listdir(dir_path) if f.endswith('.json')]
# Shuffle the list of JSON files
random.shuffle(json_files)

# Split the list of JSON files into three parts
test_files = json_files[:700]
valid_files = json_files[700:2000]
train_files = json_files[2000:]

# Move the JSON files and their corresponding JPEG files to the appropriate folders
for json_file in test_files:
    jpeg_file = json_file.replace('.json', '.jpg')
    shutil.copy(os.path.join(dir_path, json_file), test_path)
    shutil.copy(os.path.join(dir_path, jpeg_file), test_path)

for json_file in valid_files:
    jpeg_file = json_file.replace('.json', '.jpg')
    shutil.copy(os.path.join(dir_path, json_file), valid_path)
    shutil.copy(os.path.join(dir_path, jpeg_file), valid_path)

for json_file in train_files:
    jpeg_file = json_file.replace('.json', '.jpg')
    shutil.copy(os.path.join(dir_path, json_file), train_path)
    shutil.copy(os.path.join(dir_path, jpeg_file), train_path)