import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
import os
import pandas as pd
from functions import write_to_gsheet, createDIR
import datetime
from overlay_mask import reColor
from statistics import mean

batch_num = 11
# from IncisionDataFolderCreation import batch_num

common_path = 'annotationData/'
# machine_path = '/data/projects/IncisionDeepLab/outputs_consensus_Batch3-7/inference_results'
# machine_path = '/data/projects/IncisionDeepLab/outputs_consensus_Batch3-7_mobilenet/inference_results'
machine_path = '/data/DATA/Incision_predictions/Batch11/all/final'
dest_folder = 'ImgOut'
draw_machine_prediction = False


def overlayMasks_incision(image_orig, mask1, mask2):
    # This function takes the two masks and overlay them to the image_orig
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, color2=(255, 0, 0))

    overlay2 = mask2.convert('RGB')
    overlay2 = reColor(overlay2, color2=(0, 255, 0))

    # Replace (255,255,0) with (255,0,0)
    data1 = np.array(overlay)  # "data" is a height x width x 4 numpy array
    data2 = np.array(overlay2)  # "data" is a height x width x 4 numpy array
    data = data1 + data2
    red, green, blue = data.T  # Temporarily unpack the bands for readability
    two_colored_areas = (red == 255) & (blue == 0) & (green == 255)
    data[two_colored_areas.T] = (255, 0, 0)  # Transpose back neede
    overlay_final = Image.fromarray(data)
    mask_final = overlay_final.convert('L')
    mask_final = mask_final.point(lambda p: 60 if p > 5 else 0)

    bg.paste(overlay_final, None, mask_final)
    return bg


def initializeMask(size):
    a = Image.new(mode="RGBA", size=(size[0], size[1]), color="black")
    return a


images = os.listdir(common_path + '/image')
createDIR('', dest_folder)
lenimg = len(images)
print('There are %d images' % lenimg)
batch_size = 4
space_height = 120
ep = 1e-15
nameList = []
frameList = []
HFNstat = []
SFNstat = []
HFJstat = []
SFJstat = []
HGNstat = []
SGNstat = []
HGJstat = []
SGJstat = []
MGNstat = []
MGJstat = []
MFNstat = []
MFJstat = []
MNJstat = []
HNJstat = []
SNJstat = []
HCFstat = []
SCFstat = []
MCFstat = []
HCNstat = []
SCNstat = []
MCNstat = []
HCGstat = []
SCGstat = []
MCGstat = []
HCJstat = []
SCJstat = []
MCJstat = []


for j in range(math.ceil(lenimg / batch_size)):
    counter = 1
    batchstart = True
    hh = 0
    print(j)
    for i in range(j * batch_size, (j + 1) * batch_size):
        if i > lenimg - 1:
            break
        image_orig = Image.open(os.path.join(common_path, 'image', images[i]))

        maskH_N = initializeMask(image_orig.size)
        maskS_N = initializeMask(image_orig.size)
        maskH_F = initializeMask(image_orig.size)
        maskS_F = initializeMask(image_orig.size)
        maskH_G = initializeMask(image_orig.size)
        maskS_G = initializeMask(image_orig.size)
        maskH_J = initializeMask(image_orig.size)
        maskS_J = initializeMask(image_orig.size)
        maskH_ER = initializeMask(image_orig.size)
        maskS_ER = initializeMask(image_orig.size)
        maskH_EB = initializeMask(image_orig.size)
        maskS_EB = initializeMask(image_orig.size)

        try:
            maskH_N = Image.open(os.path.join(common_path, 'maskTreat', images[i][:-4] + '.png'))
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
        try:
            maskH_ER = Image.open(os.path.join(common_path, 'maskTreatI', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Consensus\'s annot on ' + images[i][:-4])
        try:
            maskS_C = Image.open(os.path.join(common_path, 'maskCheckI', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Consensus\'s annot on ' + images[i][:-4])

        maskH_N_array = np.array(maskH_N.convert('1'))
        maskS_N_array = np.array(maskS_N.convert('1'))
        maskH_J_array = np.array(maskH_J.convert('1'))
        maskS_J_array = np.array(maskS_J.convert('1'))
        maskH_1_array = np.array(maskH_G.convert('1'))
        maskS_1_array = np.array(maskS_G.convert('1'))
        maskH_2_array = np.array(maskH_F.convert('1'))
        maskS_2_array = np.array(maskS_F.convert('1'))
        maskH_ER_array = np.array(maskH_ER.convert('1'))
        maskS_ER_array = np.array(maskS_ER.convert('1'))
        maskH_EB_array = np.array(maskH_EB.convert('1'))
        maskS_EB_array = np.array(maskS_EB.convert('1'))

#########################
        image_overlayed_ref1 = overlayMasks_incision(image_orig, maskH_N, maskS_N)
        image_overlayed_ref2 = overlayMasks_incision(image_orig, maskH_J, maskS_J)
        image_overlayed_ann1 = overlayMasks_incision(image_orig, maskH_G, maskS_G)
        image_overlayed_ann2 = overlayMasks_incision(image_orig, maskH_F, maskS_F)
        image_overlayed_ER = overlayMasks_incision(image_orig, maskH_ER, maskS_ER)
        image_overlayed_EB = overlayMasks_incision(image_orig, maskH_EB, maskS_EB)

        if batchstart:
            batchstart = False
            if j > math.floor(lenimg / batch_size) - 1:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    2 * (lenimg % batch_size) * 1080 + space_height * (lenimg % batch_size)),
                                (255, 255, 255))
            else:
                im3 = Image.new("RGB", (
                    3 * 1920 + 20,
                    2 * batch_size * 1080 + space_height * (batch_size + 1)),
                                (255, 255, 255))

        if image_overlayed_ref1.width < 1920:
            newsize = (1920, 1080)
            image_overlayed_ref1 = image_overlayed_ref1.resize(newsize)
            image_overlayed_ref2 = image_overlayed_ref2.resize(newsize)
            image_overlayed_ann2 = image_overlayed_ann2.resize(newsize)
            image_overlayed_ann1 = image_overlayed_ann1.resize(newsize)
            image_orig = image_orig.resize(newsize)
            image_overlayed_cons = image_overlayed_cons.resize(newsize)

        WIDTH = image_overlayed_ref1.width
        HEIGHT = image_orig.height
        # Paste the images onto the white background

        im3.paste(image_orig, (0, hh + space_height))
        im3.paste(image_overlayed_ref1, (WIDTH + 10, hh + space_height))
        im3.paste(image_overlayed_ref2, (2 * WIDTH + 20, hh + space_height))

        im3.paste(image_overlayed_ann1, (WIDTH + 10, hh + 2 * space_height + HEIGHT - 100))
        im3.paste(image_overlayed_ann2, (2 * WIDTH + 20, hh + 2 * space_height + HEIGHT - 100))
        cv2.imwrite(dest_folder+'/' + images[i]+ ".jpg",
                    cv2.cvtColor(np.array(image_overlayed_cons), cv2.COLOR_BGR2RGB))
        if draw_machine_prediction:
            image_machine = Image.open(os.path.join(machine_path, images[i]))
            im3.paste(image_machine.resize((1920, 1080)), (0, hh + 2 * space_height + HEIGHT - 100))

        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("arial.ttf", 50)
        # Draw the text on the image
        imagename = images[i][:-4]

        namevid, _, frnumber = imagename.rpartition('_')
        draw.text((0 / 2 * image_overlayed_ann1.width, hh + .5 * space_height), namevid, fill=(0, 0, 0), font=font)
        hh = hh + 2 * image_orig.height + space_height

        counter += 1

        imagename = images[i][:-4]
        namevid, _, frnumber = imagename.rpartition('_')
        nameList.append(namevid[:-4])
        frameList.append(frnumber)
        HFNstat.append(H2N)
        HFJstat.append(H2J)
        SFNstat.append(S2N)
        SFJstat.append(S2J)

        HGNstat.append(H1N)
        HGJstat.append(H1J)
        SGNstat.append(S1N)
        SGJstat.append(S1J)

        MFNstat.append(M2N)
        MFJstat.append(M2J)
        MGNstat.append(M1N)
        MGJstat.append(M1J)

        HNJstat.append(HNJ)
        SNJstat.append(SNJ)
        MNJstat.append(MNJ)


    cv2.imwrite(dest_folder + '/Batch' + str(batch_num) + '-Comparison' + str(j + 1) + ".jpg",
                cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))


#  im3.save(dest_folder +'/Batch' + str(batch_num) + '-Comparison' + str(j + 1) + ".jpg")

# im3.close()
nameList.append('Average')
frameList.append('')
HFNstat.append(mean(HFNstat))
HFJstat.append(mean(HFJstat))
SFNstat.append(mean(SFNstat))
SFJstat.append(mean(SFJstat))
HGNstat.append(mean(HGNstat))
HGJstat.append(mean(HGJstat))

SGNstat.append(mean(SGNstat))
SGJstat.append(mean(SGJstat))
MFNstat.append(mean(MFNstat))
MFJstat.append(mean(MFJstat))
MGNstat.append(mean(MGNstat))
MGJstat.append(mean(MGJstat))
HNJstat.append(mean(HNJstat))
SNJstat.append(mean(SNJstat))
MNJstat.append(mean(MNJstat))

data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'FF-NB Treat': HFNstat, 'FF-NB Check': SFNstat,
     'FF-NB Merge': MFNstat, 'GG-NB Treat': HGNstat, 'GG-NB Check': SGNstat,
     'GG-NB Merge': MGNstat, 'FF-JLP Treat': HFJstat, 'FF-JLP Check': SFJstat,
     'FF-JLP Merge': MFJstat, 'GG-JLP Treat': HGJstat, 'GG-JLP Check': SGJstat,
     'GG-JLP Merge': MGJstat, 'NB-JLP Treat': HNJstat, 'NB-JLP Check': SNJstat,
     'NB-JLP Merge': MNJstat})
# sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
# sheetID = '1HiWuZGv5_Y_BjxnV2gIgDN2VA7WVawuvUd545Wr5FlY'
# sheetName = str(datetime.date.today()) + '-Batch' + str(batch_num)
# write_to_gsheet(sfpath, sheetID, sheetName, data_df)
data_df.to_pickle('batch' + str(batch_num) + '.pkl')
print('batch' + str(batch_num) + '.pkl saved')
