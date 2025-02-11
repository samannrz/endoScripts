import os

path_train_image = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/train_images'
path_train_mask = '/data/projects/IncisionDeepLab/input/incision/orig_dataall/train_masks'

path_test = ('/data/projects/IncisionDeepLab/input/incision/orig_data4/test_images')

for file in os.listdir(path_train_image):
    if file in os.listdir(path_test):
        os.remove(os.path.join(path_train_image,file))
        os.remove(os.path.join(path_train_mask,file))