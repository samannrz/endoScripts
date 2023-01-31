import json
import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd
import pygsheets

Name = 'Nicolas'
common_path = 'SuperviselyData'+Name
maskHarddir = 'maskHard'+Name[0]
maskSecudir = 'maskSecurity'+Name[0]


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

def createDIR (namedir):
    # create new directory for images
    path =  'Dataset/' + namedir
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The "+ namedir + " directory is created!")
        return namedir

def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
             return os.path.join(root, name)


def extractFrame(video,frame_number):
    vidcap = cv2.VideoCapture(video)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
    res, frame =vidcap.read()
    return frame

def findClass(key, objects):
    for obj in objects:
        if key == obj['key']:
            return obj['classTitle']

prList =[]
dsList =[]
vidList=[]

createDIR('image')
createDIR(maskHarddir)
createDIR(maskSecudir)
projects =os.listdir (common_path)
for project in projects: # for each project
    if not os.path.isdir(common_path + '/' +project) or  project == 'Endometriosis_WS1':
        continue
    datasets = os.listdir(common_path + '/' +project)
    for ds in datasets:
        dspath = common_path + '/' + project +'/'+ ds
        if not os.path.isdir(dspath):
            continue
        annsPath = dspath +'/ann'
        vidsPath = dspath+'/video'
        jsonFiles = os.listdir(annsPath)
        for js in jsonFiles: #each json file is for one video
            jsfile = open(annsPath+'/'+js)
            annotation = json.load(jsfile)
            frames = (annotation['frames']) # frame is the annotation info (type: list of dict) on that frame
            # print((frames))
            if len(frames) <1 :  # if there is no annotation on the video
                continue # go to the next jsonfile (and next video)
            for fr in frames:
                # if fr['index']!=967:
                #     continue
                # Create an image with a white background
                imageHard = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']), (255, 255, 255))
                imageSecu = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                      (255, 255, 255))
                # Create a draw object
                drawHard = ImageDraw.Draw(imageHard)
                drawSecu = ImageDraw.Draw(imageSecu)
                Hardexists = False
                Secuexists = False

                figures = fr['figures']
                for fig in figures:
                    frcoor = fig['geometry']['points']['exterior']
                    polygon = [tuple(coor) for coor in frcoor]
                    # print(type(polygon[0][0]))
                    # for ilen in range(len(polygon)):
                    #     polygon[ilen]=(polygon[ilen][0]-10,polygon[ilen][1] - 40)
                    #find the class of the polygon
                    classobj = findClass(fig['objectKey'], annotation['objects'])
                    if classobj == 'Hard Zone':
                        # Draw the polygon on the image
                        drawHard.polygon(polygon, fill=(0, 0, 0))
                        # Convert the image to a mask
                        maskHard = imageHard.convert("L")
                        Hardexists= True
                    elif classobj == 'Security Zone':
                        # Draw the polygon on the image
                        drawSecu.polygon(polygon, fill=(0, 0, 0))
                        maskSecu = imageSecu.convert("L")
                        Secuexists= True

                    #save masks and images
                    # save the image frame
                    vidpath = find(js[:-5], vidsPath)  # find the video with the associated json file
                    _, _, vidname = vidpath.rpartition('/')

                    cv2.imwrite('Dataset/image/' + vidname + "_%d.jpg" % fr['index'],
                                extractFrame(vidpath, fr['index']))  # save frame as JPEG file
                    #save the masks
                    if Hardexists:
                        maskHard.save('Dataset/' + maskHarddir + '/' + vidname + "_%d.png" % fr['index'], 'PNG')
                    if Secuexists:
                        maskSecu.save('Dataset/'+ maskSecudir+ '/' + vidname + "_%d.png" % fr['index'], 'PNG')

                prList.append(project)
                dsList.append(ds)
                vidList.append(vidname)

# data_df = pd.DataFrame(
#     {'Vid. Name': vidList, 'Project': prList, 'Dataset': dsList})
# sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
# sheetID = '1UIA6ve-AQi5KMPVONoN5c0yBWLnIQ5RHem383WwqiB4'
# sheetName = 'info_'+Name#+str(datetime.date.today())
# # data_df.to_excel('stats-Results.xlsx', sheetName)
# write_to_gsheet(sfpath, sheetID, sheetName, data_df)
#









