import os

from functions import find_missing_images
# Call the function to find and copy missing images
base_path = '/data/DATA/incision/'
orig_path1 = os.path.join(base_path, str(2))
orig_path2 = os.path.join(base_path, str(3))
savepath = os.path.join(base_path,'23')

orig_path_image1 = os.path.join(orig_path1, 'image')
orig_path_image2 = os.path.join(orig_path2, 'image')
path_mask_check1 = os.path.join(orig_path1, 'mask/Check/')
path_mask_check2 = os.path.join(orig_path2, 'mask/Check/')
path_mask_treat1 = os.path.join(orig_path1, 'mask/Treat/')
path_mask_treat2 = os.path.join(orig_path2, 'mask/Treat/')

images1 = os.listdir(os.path.join(orig_path1, 'image/'))
images2 = os.listdir(os.path.join(orig_path2, 'image/'))
images_intersect = list(set(images1).intersection(images2))


find_missing_images(orig_path_image1, os.path.join(savepath, 'image'))
find_missing_images(orig_path_image2, os.path.join(savepath, 'image'))

find_missing_images(path_mask_treat1, os.path.join(savepath, 'mask/Treat'))
find_missing_images(path_mask_treat2, os.path.join(savepath, 'mask/Treat'))

find_missing_images(path_mask_check1, os.path.join(savepath, 'mask/Check'))
find_missing_images(path_mask_check2, os.path.join(savepath, 'mask/Check'))
