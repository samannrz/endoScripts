import shutil

from PIL import Image
import os
from functions import createDIR, overlayMasks_incision

common_path = '/data/DATA/DELPHI_incision'
common_path = 'annotationData'
dest_folder = '/data/DATA/DELPHI_incision/consensus9'


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
    maskH_F = initializeMask(image_orig.size)
    maskS_F = initializeMask(image_orig.size)
    maskH_G = initializeMask(image_orig.size)
    maskS_G = initializeMask(image_orig.size)
    maskH_J = initializeMask(image_orig.size)
    maskS_J = initializeMask(image_orig.size)

    try:
        maskH_N = Image.open(os.path.join(common_path, 'maskTreatN', images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on Nicolas\'s annot on ' + images[i][:-4])
    try:
        maskS_N = Image.open(os.path.join(common_path, 'maskCheckN', images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on Nicolas\'s annot on ' + images[i][:-4])
    #### Jean Luc ####
    try:
        maskH_J = Image.open(os.path.join(common_path, 'maskTreatJ', images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on Jean Luc\'s annot on ' + images[i][:-4])
    try:
        maskS_J = Image.open(os.path.join(common_path, 'maskCheckJ', images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on Jean Luc\'s annot on ' + images[i][:-4])
    #### Giuseppe ####
    try:
        maskH_G = Image.open(os.path.join(common_path, 'maskTreatG', images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on Giuseppe\'s annot on ' + images[i][:-4])
    try:
        maskS_G = Image.open(os.path.join(common_path, 'maskCheckG', images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on Giuseppe\'s annot on ' + images[i][:-4])
    #### Filippo ####
    try:
        maskH_F = Image.open(os.path.join(common_path, 'maskTreatF', images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on Filippo\'s annot on ' + images[i][:-4])
    try:
        maskS_F = Image.open(os.path.join(common_path, 'maskCheckF', images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on Filippo\'s annot on ' + images[i][:-4])
    ####### Consensus #########
    try:
        maskH_C = Image.open(os.path.join(common_path, 'maskTreatI', images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on Consensus\'s annot on ' + images[i][:-4])
    try:
        maskS_C = Image.open(os.path.join(common_path, 'maskCheckI', images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on Consensus\'s annot on ' + images[i][:-4])

    image_overlayed_ref1 = overlayMasks_incision(image_orig, maskH_N, maskS_N)
    image_overlayed_ref2 = overlayMasks_incision(image_orig, maskH_J, maskS_J)
    image_overlayed_ann1 = overlayMasks_incision(image_orig, maskH_G, maskS_G)
    image_overlayed_ann2 = overlayMasks_incision(image_orig, maskH_F, maskS_F)
    image_overlayed_C = overlayMasks_incision(image_orig, maskH_C, maskS_C)

    imagename = images[i][:-4]
    namevid, _, frnumber = imagename.rpartition('_')
    print('writing images to ', os.path.join(dest_folder, namevid + '_' + frnumber + '_i.png'))
    image_overlayed_ref1.save(os.path.join(dest_folder, namevid + '_' + frnumber + '_1.png'))
    image_overlayed_ref2.save(os.path.join(dest_folder, namevid + '_' + frnumber + '_2.png'))
    image_overlayed_ann1.save(os.path.join(dest_folder, namevid + '_' + frnumber + '_3.png'))
    image_overlayed_ann2.save(os.path.join(dest_folder, namevid + '_' + frnumber + '_4.png'))
    image_overlayed_C.save(os.path.join(dest_folder, namevid + '_' + frnumber + '_5.png'))
    shutil.copy(os.path.join(common_path, 'image', images[i]), os.path.join(dest_folder, namevid + '_' + frnumber + '_0.png'))