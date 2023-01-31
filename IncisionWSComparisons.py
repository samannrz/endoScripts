import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import os
import pandas as pd
import pygsheets
import datetime

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
    mask1 = mask1.point(lambda p: 80 if p < 225 else 0)

    overlay2 = mask2.convert('RGB')
    overlay2 = reColor(overlay2, (250,160,0))
    mask2 = overlay2.convert('L')
    mask2 = mask2.point(lambda p: 70 if p < 255 else 0)

    bg.paste(overlay, None, mask1)
    bg.paste(overlay2, None, mask2)
    return bg
def plotAllpx(figg,counter,b,c,d):
    print('in function:')
    print(type(figg))
    figg.add_trace(go.Image(z=b), counter+1, 0+1)
    figg.add_trace(go.Image(z=c), counter+1, 1+1)
    figg.add_trace(go.Image(z=d), counter+1, 2+1)
    figg.update_layout(polar=dict(radialaxis=dict(showticklabels=False)))
    figg.update_layout(polar=dict(radialaxis=dict(visible=False)))
    figg.update_layout(polar=dict(angularaxis=dict(showticklabels=False)))
    figg.update_layout(xaxis_visible=False, yaxis_visible=False, xaxis2_visible=False, yaxis2_visible=False)
    figg.update_xaxes(visible=False, row=counter, col=1)
    figg.update_yaxes(visible=False, row=counter, col=2)
    figg.update_xaxes(visible=False, row=counter, col=3)

    return px

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
# lenimg=2
print('There are %d images' %lenimg)
batch_size =6

fig, ax = plt.subplots(batch_size, 4)

# a=0

nameList = []
frameList = []
HFstat = []
SFstat = []
HGstat = []
SGstat = []

for  j in range(math.ceil(lenimg/batch_size)):
    counter =1
    if j > math.ceil(lenimg/batch_size)-1:
        fig1=make_subplots(lenimg%batch_size, 3,
                          horizontal_spacing = 0.00,vertical_spacing = 0.01)
        fig2 = make_subplots(lenimg % batch_size, 3,
                             horizontal_spacing=0.00, vertical_spacing=0.01)
    else:
        fig1=make_subplots(batch_size, 3,
                          horizontal_spacing = 0.00,vertical_spacing = 0.01)
        fig2 = make_subplots(batch_size, 3,
                             horizontal_spacing=0.00, vertical_spacing=0.01)
    for i in range(j*batch_size,(j+1)*batch_size):
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
        maskH_N_array = ~np.array(maskH_N.convert('1'))
        maskS_N_array = ~np.array(maskS_N.convert('1'))
        maskH_1_array = ~np.array(maskH_G.convert('1'))
        maskS_1_array = ~np.array(maskS_G.convert('1'))
        maskH_2_array = ~np.array(maskH_F.convert('1'))
        maskS_2_array = ~np.array(maskS_F.convert('1'))

        try:
            Hard_1N = maskH_1_array & maskH_N_array
            Hard_2N = maskH_2_array & maskH_N_array
            H2N = round((np.count_nonzero(Hard_2N) / np.count_nonzero(maskH_N_array)) * 100, 2)
            H1N = round((np.count_nonzero(Hard_1N) / np.count_nonzero(maskH_N_array)) * 100, 2)
        except ZeroDivisionError:
            H2N = 0
            H1N = 0

        try:
            Secu_2N = maskS_2_array & maskS_N_array
            Secu_1N = maskS_1_array & maskS_N_array
            S1N = round((np.count_nonzero(Secu_1N) / np.count_nonzero(maskS_N_array)) * 100, 2)
            S2N = round((np.count_nonzero(Secu_2N) / np.count_nonzero(maskS_N_array)) * 100, 2)
        except ZeroDivisionError:
            S2N = 0
            S1N = 0
        if plot_ann > 0:
            image_overlayed_ref = overlayMask(image_orig, maskH_N, maskS_N)
            image_overlayed_ann1 = overlayMask(image_orig, maskH_G, maskS_G)
            image_overlayed_ann2 = overlayMask(image_orig, maskH_F, maskS_F)
            if plot_ann ==1:
                image_overlayed_ann = image_overlayed_ann1
                Hscore = H1N
                Sscore = S1N
            if plot_ann == 2:
                image_overlayed_ann = image_overlayed_ann2
                Hscore = H2N
                Sscore = S2N

            fig1.add_trace(go.Image(z=image_orig), counter, 1)
            fig1.add_trace(go.Image(z=image_overlayed_ref),counter,  2)
            fig1.add_trace(go.Image(z=image_overlayed_ann), counter, 3)
            fig1.update_layout(height=1080, width=1080)
            fig1.update_xaxes(visible=False, row=counter, col=1)
            fig1.update_xaxes(visible=False, row=counter, col=2)
            fig1.update_xaxes(visible=False, row=counter, col=3)
            # fig1.update_yaxes(visible=False, row=counter, col=1)
            fig1.update_yaxes(visible=False, row=counter, col=2)
            fig1.update_yaxes(visible=False, row=counter, col=3)
            fig1.update_yaxes(title='<span style="font-size: 10px;">'+'H.sc: ' + str(Hscore)+'<br>'+'Sec.sc: ' + str(Sscore)+'</span>', row=counter, col=1)

            counter+=1

            imagename = images[i][:-4]
            namevid, _, frnumber = imagename.rpartition('_')
            nameList.append(namevid[:-4])
            frameList.append(frnumber)
            HFstat.append(H2N)
            SFstat.append(S2N)
            HGstat.append(H1N)
            SGstat.append(S1N)

    # fig.show()
    fig1.write_html('ImgOut/'+'Ann'+str(plot_ann)+'_'+ str(j)+'.html')

data_df = pd.DataFrame(
    {'Vid. Name': nameList, '# frame': frameList, 'Filippo Hard Score': HFstat, 'Filippo Security Score': SFstat, 'Giuseppe Hard Score': HGstat, 'Giuseppe Security Score': SGstat})
sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1UIA6ve-AQi5KMPVONoN5c0yBWLnIQ5RHem383WwqiB4'
sheetName = str(datetime.date.today())
data_df.to_excel('stats-Results.xlsx', sheetName)
write_to_gsheet(sfpath, sheetID, sheetName, data_df)

