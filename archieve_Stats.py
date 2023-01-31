import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import datetime
import os
import pandas as pd
import pygsheets
import cv2

common_path = 'Dataset'
maskHarddir = 'maskHard'
maskSecudir = 'maskSecurity'

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
def initializeMasks (size):
    a = np.full((size[1],size[0]), False, dtype=bool)
    b = np.full((size[1], size[0]), False, dtype=bool)
    c = np.full((size[1], size[0]), False, dtype=bool)
    d = np.full((size[1], size[0]), False, dtype=bool)
    e = np.full((size[1], size[0]), False, dtype=bool)
    f = np.full((size[1], size[0]), False, dtype=bool)


    return a,b,c,d,e,f

images = os.listdir(common_path + '/image')
lenimg = len(images)
# lenimg=5
print('There are %d iamges' %lenimg)
a=0
j=0
G=True
nameList = []
frameList = []
HFstat = []
SFstat = []
HGstat = []
SGstat = []

for i in range(lenimg):
    print('processing image %d'%i)
    image_orig = Image.open(os.path.join(common_path,'image', images[i]))
    print(type(image_orig))
    maskH_N,maskS_N,maskH_F,maskS_F,maskH_G,maskS_G= initializeMasks (image_orig.size)

    try:
        maskH_N = ~np.array(Image.open(os.path.join(common_path,'maskHardN', images[i][:-4]+'.png')).convert('1'))
    except:
        print('There is no Hard Zone on Nicolas\'s annot on ' + images[i][:-4])
    try:
        maskS_N = ~np.array(Image.open(os.path.join(common_path, 'maskSecurityN', images[i][:-4] + '.png')).convert('1'))
    except:
        print('There is no Security Zone on Nicolas\'s annot on ' + images[i][:-4])
        G = False
    try:
        maskH_G = ~np.array(Image.open(os.path.join(common_path, 'maskHardG', images[i][:-4] + '.png')).convert('1'))
    except:
        print('There is no Hard Zone on Giuseppe\'s annot on '+ images[i][:-4])
    try:
        maskS_G = ~np.array(Image.open(os.path.join(common_path, 'maskSecurityG', images[i][:-4] + '.png')).convert('1'))
    except:
        print('There is no Security Zone on Giuseppe\'s annot on '+ images[i][:-4])
    try:
        maskH_F = ~np.array(Image.open(os.path.join(common_path, 'maskHardF', images[i][:-4] + '.png')).convert('1'))
    except:
        print('There is no Hard Zone on Filippo\'s annot on '+ images[i][:-4])
    try:
        maskS_F = ~np.array(Image.open(os.path.join(common_path, 'maskSecurityF', images[i][:-4] + '.png')).convert('1'))
    except:
        print('There is no Security Zone on Filippo\'s annot on '+ images[i][:-4])


    try:
        Hard_GN = maskH_G & maskH_N
        Hard_FN = maskH_F & maskH_N
        HFN = round((np.count_nonzero(Hard_FN) / np.count_nonzero(maskH_N))*100,2)
        HGN = round((np.count_nonzero(Hard_GN) / np.count_nonzero(maskH_N))*100,2)
    except ZeroDivisionError:
        print('nan1')
        HFN = 'nan'
        HGN = 'nan'

    try:
        Secu_FN = maskS_F & maskS_N
        Secu_GN = maskS_G & maskS_N
        SGN = round((np.count_nonzero(Secu_GN) / np.count_nonzero(maskS_N))*100,2)
        SFN = round((np.count_nonzero(Secu_FN) / np.count_nonzero(maskS_N))*100,2)
    except ZeroDivisionError:
        print('nan2')
        SFN = 'nan'
        SGN = 'nan'



    imagename = images[i][:-4]
    namevid, _, frnumber = imagename.rpartition('_')
    nameList.append(namevid[:-4])
    frameList.append(frnumber)
    HFstat.append(HFN)
    SFstat.append(SFN)
    HGstat.append(HGN)
    SGstat.append(SGN)


data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'Filippo Hard Score': HFstat, 'Filippo Security Score': SFstat, 'Giuseppe Hard Score': HGstat, 'Giuseppe Security Score': SGstat})
sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1UIA6ve-AQi5KMPVONoN5c0yBWLnIQ5RHem383WwqiB4'
sheetName = str(datetime.date.today())
data_df.to_excel('stats-Results.xlsx', sheetName)
write_to_gsheet(sfpath, sheetID, sheetName, data_df)












