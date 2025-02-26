from PIL import Image
import os
from src.functions import overlayMasks_incision


dest_folder = '/data/DATA/supervisely_format/Batch210/final'
dest_folder = '/data/DATA/Incision_predictions/Batch211-FasterViT/final'
dest_folder = '/data/DATA/STAPLE/Batch214/final'
dest_folder = '/data/DATA/TESTS'
common_path_image = '/data/DATA/incision/4'
#common_path_mask = '/data/DATA/Incision_predictions/Batch211-FasterViT/'
common_path_mask = common_path_image



image_folder_name ='image'
mask_folder_name ='mask'

def initializeMask(size):
    a = Image.new(mode="RGBA", size=(size[0], size[1]), color="black")
    return a


images = os.listdir(os.path.join(common_path_image,image_folder_name))
# createDIR('', dest_folder)
lenimg = len(images)
print('There are %d images' % lenimg)

for i in range(lenimg):

    image_orig = Image.open(os.path.join(common_path_image, image_folder_name, images[i]))

    mask_Treat = initializeMask(image_orig.size)
    mask_Check = initializeMask(image_orig.size)

    try:
        mask_Treat = Image.open(os.path.join(common_path_mask, mask_folder_name,'Treat', images[i][:-4] + '.png'))
    except:
        print('There is no Treat Zone' + images[i][:-4])
    try:
        mask_Check = Image.open(os.path.join(common_path_mask, mask_folder_name,'Check', images[i][:-4] + '.png'))
    except:
        print('There is no Check Zone' + images[i][:-4])

    image_overlayed = overlayMasks_incision(image_orig, mask_Treat, mask_Check)

    imagename = images[i][:-4]
    namevid, _, frnumber = imagename.rpartition('_')
    print('writing images to ', os.path.join(dest_folder, namevid + '_' + frnumber + '.png'))
    image_overlayed.save(os.path.join(dest_folder, namevid + '_' + frnumber + '.png'))
