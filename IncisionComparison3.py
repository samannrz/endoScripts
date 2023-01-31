import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
import pygsheets
import datetime
import time

common_path = 'Dataset'
# maskHarddir = 'maskHard'
# maskSecudir = 'maskSecurity'
plot_ann = 1


def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1', None, '*')
    wks_write.set_dataframe(data_df, (1, 1), encoding='utf-8', fit=True)
    wks_write.frozen_rows = 1


def reColor(mask, color):
    data = np.array(mask)  # "data" is a height x width x 4 numpy array
    red, green, blue = data.T  # Temporarily unpack the bands for readability

    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red == 0) & (blue == 0) & (green == 0)
    data[black_areas.T] = color  # Transpose back needed
    mask2 = Image.fromarray(data)
    return mask2


def mergeMasks(mask1, mask2):
    mask = np.zeros((mask1.shape[0], mask1.shape[1]))
    mask2[mask2 == 0] = 2
    mask1[mask1 == 0] = 1
    mask = mask + mask1 + mask2
    return mask


def overlayMask(image_orig, mask1, mask2):
    # This function takes the two masks and overlay them to the image_orig
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, (255, 0, 0))
    mask1 = overlay.convert('L')
    mask1 = mask1.point(lambda p: 80 if p < 225 else 0)

    overlay2 = mask2.convert('RGB')
    overlay2 = reColor(overlay2, (250, 160, 0))
    mask2 = overlay2.convert('L')
    mask2 = mask2.point(lambda p: 70 if p < 255 else 0)

    bg.paste(overlay, None, mask1)
    bg.paste(overlay2, None, mask2)
    return bg


def initializeMask(size):
    a = Image.new(mode="RGBA", size=(size[0], size[1]), color="white")

    return a


images = os.listdir(common_path + '/image')
lenimg = len(images)
# lenimg=5
print('There are %d images' % lenimg)
batch_size = 4
space_height = 120

nameList = []
frameList = []
HFstat = []
SFstat = []
HGstat = []
SGstat = []
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

        try:
            maskH_N = Image.open(os.path.join(common_path, 'maskHardN', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Nicolas\'s annot on ' + images[i][:-4])
        try:
            maskS_N = Image.open(os.path.join(common_path, 'maskSecurityN', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Nicolas\'s annot on ' + images[i][:-4])
        #### Jean Luc ####
        try:
            maskH_J = Image.open(os.path.join(common_path, 'maskHardJ', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Jean Luc\'s annot on ' + images[i][:-4])
        try:
            maskS_J = Image.open(os.path.join(common_path, 'maskSecurityJ', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Jean Luc\'s annot on ' + images[i][:-4])
        #### Giuseppe ####
        try:
            maskH_G = Image.open(os.path.join(common_path, 'maskHardG', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Giuseppe\'s annot on ' + images[i][:-4])
        try:
            maskS_G = Image.open(os.path.join(common_path, 'maskSecurityG', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Giuseppe\'s annot on ' + images[i][:-4])
        #### Filippo ####
        try:
            maskH_F = Image.open(os.path.join(common_path, 'maskHardF', images[i][:-4] + '.png'))
        except:
            print('There is no Hard Zone on Filippo\'s annot on ' + images[i][:-4])
        try:
            maskS_F = Image.open(os.path.join(common_path, 'maskSecurityF', images[i][:-4] + '.png'))
        except:
            print('There is no Security Zone on Filippo\'s annot on ' + images[i][:-4])
        # plt.tight_layout()
        maskH_N_array = ~np.array(maskH_N.convert('1'))
        maskS_N_array = ~np.array(maskS_N.convert('1'))
        maskH_J_array = ~np.array(maskH_J.convert('1'))
        maskS_J_array = ~np.array(maskS_J.convert('1'))
        maskH_1_array = ~np.array(maskH_G.convert('1'))
        maskS_1_array = ~np.array(maskS_G.convert('1'))
        maskH_2_array = ~np.array(maskH_F.convert('1'))
        maskS_2_array = ~np.array(maskS_F.convert('1'))

        try:
            # Comparison of Hard zones
            # Comparison with Nicolas
            Hard_1N = maskH_1_array & maskH_N_array
            Hard_2N = maskH_2_array & maskH_N_array
            H2N = round((np.count_nonzero(Hard_2N) / np.count_nonzero(maskH_N_array)) * 100, 2)
            H1N = round((np.count_nonzero(Hard_1N) / np.count_nonzero(maskH_N_array)) * 100, 2)
        except ZeroDivisionError:
            H2N = 0
            H1N = 0

        try:
            # Comparison of Hard zones
            # Comparison with Jean Luc
            Hard_1J = maskH_1_array & maskH_J_array
            Hard_2J = maskH_2_array & maskH_J_array
            H2J = round((np.count_nonzero(Hard_2J) / np.count_nonzero(maskH_J_array)) * 100, 2)
            H1J = round((np.count_nonzero(Hard_1J) / np.count_nonzero(maskH_J_array)) * 100, 2)
        except ZeroDivisionError:
            H2J = 0
            H1J = 0

        try:
            # Comparison of Soft zones
            # Comparison with Nicolas
            Secu_2N = maskS_2_array & maskS_N_array
            Secu_1N = maskS_1_array & maskS_N_array
            S1N = round((np.count_nonzero(Secu_1N) / np.count_nonzero(maskS_N_array)) * 100, 2)
            S2N = round((np.count_nonzero(Secu_2N) / np.count_nonzero(maskS_N_array)) * 100, 2)
        except ZeroDivisionError:
            S2N = 0
            S1N = 0
        try:
            # Comparison of Soft zones
            # Comparison with Jean Luc
            Secu_2J = maskS_2_array & maskS_J_array
            Secu_1J = maskS_1_array & maskS_J_array
            S1J = round((np.count_nonzero(Secu_1J) / np.count_nonzero(maskS_J_array)) * 100, 2)
            S2J = round((np.count_nonzero(Secu_2J) / np.count_nonzero(maskS_J_array)) * 100, 2)
        except ZeroDivisionError:
            S2J = 0
            S1J = 0

        image_overlayed_ref1 = overlayMask(image_orig, maskH_N, maskS_N)
        image_overlayed_ref2 = overlayMask(image_orig, maskH_J, maskS_J)
        image_overlayed_ann1 = overlayMask(image_orig, maskH_G, maskS_G)
        image_overlayed_ann2 = overlayMask(image_orig, maskH_F, maskS_F)

        if batchstart:
            batchstart = False
            if j > math.floor(lenimg / batch_size) - 1:
                im3 = Image.new("RGB", (
                    3 * 1920+20,
                    2 * (lenimg % batch_size) * 1080 + space_height * (lenimg % batch_size)),
                                (255, 255, 255))
            else:
                im3 = Image.new("RGB", (
                    3 * 1920+20,
                    2 * batch_size * 1080 + space_height * (batch_size + 1)),
                                (255, 255, 255))

        # Paste the images onto the white background
        WIDTH = image_overlayed_ref1.width
        HEIGHT = image_orig.height
        # print(WIDTH)
        im3.paste(image_orig, (0, hh + space_height))
        im3.paste(image_overlayed_ref1, (WIDTH+10, hh + space_height))
        im3.paste(image_overlayed_ref2, (2 * WIDTH+20, hh + space_height))

        im3.paste(image_overlayed_ann1, (WIDTH+10, hh + 2* space_height+HEIGHT-100))
        im3.paste(image_overlayed_ann2, (2 * WIDTH+20, hh +2* space_height+HEIGHT-100))
        draw = ImageDraw.Draw(im3)
        font = ImageFont.truetype("arial.ttf", 50)
        # Draw the text on the image
        imagename = images[i][:-4]

        namevid, _, frnumber = imagename.rpartition('_')
        draw.text((0 / 2 * image_overlayed_ann1.width, hh + .5 * space_height), namevid, fill=(0, 0, 0), font=font)
        # draw.text((3 / 2 * image_overlayed_ann1.width, hh), 'Hard score: ' + str(H1N), fill=(0, 0, 0), font=font)
        # draw.text((3 / 2 * image_overlayed_ann1.width, hh + .5 * space_height), 'Sec. score: ' + str(S1N),
        #           fill=(0, 0, 0), font=font)
        # draw.text((5 / 2 * image_overlayed_ann2.width, hh), 'Hard score: ' + str(H2N), fill=(0, 0, 0), font=font)
        # draw.text((5 / 2 * image_overlayed_ann2.width, hh + .5 * space_height), 'Sec. score: ' + str(S2N),
        #           fill=(0, 0, 0), font=font)

        hh = hh + 2*image_orig.height + space_height

        counter += 1

        imagename = images[i][:-4]
        namevid, _, frnumber = imagename.rpartition('_')
        nameList.append(namevid[:-4])
        frameList.append(frnumber)
        HFstat.append(H2N)
        SFstat.append(S2N)
        HGstat.append(H1N)
        SGstat.append(S1N)
        # print(images[i])
        # if images[i] == '2022-03-17_043549_VID001_Trim_2.mp4_967.jpg':
        #     print('HI')
        #     im3.show()

    # time.sleep(2)
    # Save the combined image
    im3.save("ImgOut/Batch2-Comparison" + str(j + 1) + ".jpg")

    # im3.close()

data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'Filippo Hard Score': HFstat, 'Filippo Security Score': SFstat,
     'Giuseppe Hard Score': HGstat, 'Giuseppe Security Score': SGstat})
sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1UIA6ve-AQi5KMPVONoN5c0yBWLnIQ5RHem383WwqiB4'
sheetName = str(datetime.date.today())
data_df.to_excel('stats-Results.xlsx', sheetName)
write_to_gsheet(sfpath, sheetID, sheetName, data_df)
