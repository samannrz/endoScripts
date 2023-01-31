import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math


import os

common_path = 'Dataset'
maskHarddir = 'maskHardN'
maskSecudir = 'maskSecurityN'

def reColor(mask,color):
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    data[black_areas.T] = color  # Transpose back needed
    mask2 = Image.fromarray(data)
    return mask2

def mergeMasks(mask1,mask2):
    mask=np.zeros((mask1.shape[0],mask1.shape[1]))
    mask2[mask2 == 0] = 2
    mask1[mask1 == 0] = 1
    mask = mask+mask1+mask2
    return mask

def overlayMask(image_orig,mask1,mask2):
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, (255, 0, 0))
    mask1 = overlay.convert('L')
    mask1 = mask1.point(lambda p: 60 if p < 225 else 0)

    overlay2 = mask2.convert('RGB')
    overlay2 = reColor(overlay2, (250,160,0))
    mask2 = overlay2.convert('L')
    mask2 = mask2.point(lambda p: 70 if p < 255 else 0)

    bg.paste(overlay, None, mask1)
    bg.paste(overlay2, None, mask2)
    return bg

def plotAll(ax,counter,b,c,d,e):
    ax[counter, 0].imshow(b)
    ax[counter, 1].imshow(c)
    ax[counter, 2].imshow(d)
    ax[counter, 3].imshow(e)
    for i in range(ax.shape[1]):
        ax[counter, i].set_xticklabels([])
        ax[counter, i].set_yticklabels([])
        ax[counter, i].get_xaxis().set_visible(False)
        ax[counter, i].get_yaxis().set_visible(False)
        ax[counter, i].title.set_visible(False)
    return ax

def initializeMasks(size):
    a = Image.new(mode="RGBA", size=(size[0],size[1]), color="white")
    b = Image.new(mode="RGBA", size=(size[0],size[1]), color="white")
    c = Image.new(mode="RGBA", size=(size[0],size[1]), color="white")
    d = Image.new(mode="RGBA", size=(size[0],size[1]), color="white")
    e = Image.new(mode="RGBA", size=(size[0],size[1]), color="white")
    f = Image.new(mode="RGBA", size=(size[0],size[1]), color="white")
    return a,b,c,d,e,f


images = os.listdir(common_path + '/image')
lenimg = len(images)
lenimg=5
print('There are %d iamges' %lenimg)
batch_size =5

fig, ax = plt.subplots(batch_size, 4)

a=0
j=0
for  j in range(math.ceil(lenimg/batch_size)):
    counter =0
    plt.close()
    if j > math.ceil(lenimg/batch_size)-1:
        fig, ax = plt.subplots(lenimg%batch_size, 4)
    else:
        fig, ax = plt.subplots(batch_size, 4)
    for i in range(j*batch_size,(j+1)*batch_size):
        print('processing image %d'%i)
        if i>lenimg-1:
            break
        image_orig = Image.open(os.path.join(common_path,'image', images[i]))
        maskH_N, maskS_N, maskH_F, maskS_F, maskH_G, maskS_G = initializeMasks(image_orig.size)

        try:
            maskH_N = Image.open(os.path.join(common_path,'maskHardN', images[i][:-4]+'.png'))
        except:
            print('There is no Hard Zone on Nicolas\'s annot on ' + images[i][:-4])
        try:
            maskS_N = Image.open(os.path.join(common_path, 'maskSecurityN', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Nicolas\'s annot on ' + images[i][:-4])
        try:
            maskH_G = Image.open(os.path.join(common_path, 'maskHardG', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Giuseppe\'s annot on '+ images[i][:-4])
        try:
            maskS_G = Image.open(os.path.join(common_path, 'maskSecurityG', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Giuseppe\'s annot on '+ images[i][:-4])
        try:
            maskH_F = Image.open(os.path.join(common_path, 'maskHardF', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Filippo\'s annot on '+ images[i][:-4])
        try:
            maskS_F = Image.open(os.path.join(common_path, 'maskSecurityF', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Filippo\'s annot on '+ images[i][:-4])
        # plt.tight_layout()
        image_overlayed_ref = overlayMask(image_orig,maskH_N,maskS_N)
        image_overlayed_ann1 = overlayMask(image_orig, maskH_G, maskS_G)
        image_overlayed_ann2 = overlayMask(image_orig, maskH_F, maskS_F)
        ax=plotAll(ax,counter,image_orig,image_overlayed_ref,image_overlayed_ann1,image_overlayed_ann2)
        counter+=1
    plt.subplots_adjust(hspace=.05)
    plt.subplots_adjust(wspace=0)

    # plt.show()
    plt.savefig('Batch'+ str(j)+'.png')
    # html = file_html(plot, CDN, "Sine")

