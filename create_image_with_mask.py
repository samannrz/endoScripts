import shutil

from PIL import Image
import os
from functions import createDIR, overlayMasks_incision

common_path = '/Users/saman/Documents/data/DATA/incision/4'
dest_folder = '/Users/saman/Documents/data/DATA/incision/4'
common_path = 'annotationData'
dest_folder = '/Users/saman/Desktop'

def initializeMask(size):
    a = Image.new(mode="RGBA", size=(size[0], size[1]), color="black")
    return a


images = os.listdir(common_path + '/image')
# createDIR('', dest_folder)
lenimg = len(images)
print('There are %d images' % lenimg)

for i in range(lenimg):

    image_orig = Image.open(os.path.join(common_path, 'image', images[i]))

    maskH_N = initializeMask(image_orig.size)
    maskS_N = initializeMask(image_orig.size)

    try:
        maskH_N = Image.open(os.path.join(common_path, 'mask/Treat', images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on Nicolas\'s annot on ' + images[i][:-4])
    try:
        maskS_N = Image.open(os.path.join(common_path, 'mask/Check', images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on Nicolas\'s annot on ' + images[i][:-4])

    image_overlayed_ref1 = overlayMasks_incision(image_orig, maskH_N, maskS_N)

    imagename = images[i][:-4]
    namevid, _, frnumber = imagename.rpartition('_')
    print('writing images to ', os.path.join(dest_folder, namevid + '_' + frnumber + '_i.png'))
    image_overlayed_ref1.save(os.path.join(dest_folder, namevid + '_' + frnumber + '_1.png'))
