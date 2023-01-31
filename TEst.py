import json
import os
import time

import cv2
import numpy as np
from PIL import Image, ImageDraw
import pandas as pd
import pygsheets


common_path = 'SuperviselyData'
maskHarddir = 'maskHard'
maskSecudir = 'maskSecurity'


def createDIR(namedir):
    # create new directory for images
    path = 'Dataset/' + namedir
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The " + namedir + " directory is created!")
        return namedir


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def extractFrame(video, frame_number):
    vidcap = cv2.VideoCapture(video)
    for i in range(frame_number + 1):
        # vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        res, frame = vidcap.read()
    return frame

def findClass(key, objects):
    for obj in objects:
        if key == obj['key']:
            return obj['classTitle']


# def draw_zone(cl, drawHardN,drawSoftN,drawHardJ,drawSoftJ,drawHardG,drawSoftG,drawHardF,drawSoftF, labeler):


def mydraw(drawHS, imageHS, polygon, cl):
    if cl == 'Hard Zone':
        # Draw the polygon on the image
        drawHS.polygon(polygon, fill=(0, 0, 0))
        # Convert the image to a mask
        maskHard = imageHS.convert("L")
        Hardexists = True
    elif cl == 'Security Zone':
        # Draw the polygon on the image
        drawHS.polygon(polygon, fill=(0, 0, 0))
        maskSecu = imageHS.convert("L")
        Secuexists = True

    return maskHard, maskSecu


prList = []
dsList = []
vidList = []

createDIR('image')
for firstname in ['N', 'J', 'G', 'F']:
    createDIR(maskHarddir + firstname)
    createDIR(maskSecudir + firstname)
projects = os.listdir(common_path)
json_eval = open('Evaluation3.json')
eval = json.load(json_eval)
evals = eval['evals']
#
for project in projects:  # for each project
    if not os.path.isdir(common_path + '/' + project) or project != 'Endometriosis_WS1':
        continue
    datasets = os.listdir(common_path + '/' + project)
    for ds in datasets:
        dspath = common_path + '/' + project + '/' + ds
        if not os.path.isdir(dspath):
            continue
        annsPath = dspath + '/ann'
        vidsPath = dspath + '/video'
        evalfr = evals[0]
        jsonFiles = os.listdir(annsPath)

        for evalfr in evals:
            if evalfr['frame'] + '.json' in jsonFiles:
                jsfile = open(annsPath + '/' + evalfr['frame'] + '.json')
                annotation = json.load(jsfile)
                frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame
                if len(frames) < 1:  # if there is no annotation on the video
                    continue  # go to the next jsonfile (and next video)
                for fr in frames:
                    # Create an image with a white background
                    image_HardN = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_SecuN = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_HardJ = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_SecuJ = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_HardG = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_SecuG = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_HardF = np.ones((annotation['size']['height'], annotation['size']['width']))*255
                    image_SecuF = np.ones((annotation['size']['height'], annotation['size']['width']))*255

                    #                 # Create a draw object

                    dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3}
                    Hardexists = False
                    Secuexists = False
                    if fr['index'] not in evalfr['index']:
                        continue
                    print(fr['index'])
                    figures = fr['figures']
                    for fig in figures:
                        frcoor = fig['geometry']['points']['exterior']
                        # print(type(polygon[0][0]))
                        # for ilen in range(len(polygon)):
                        #     polygon[ilen]=(polygon[ilen][0]-10,polygon[ilen][1] - 40)
                        # find the class of the polygon
                        classobj = findClass(fig['objectKey'], annotation['objects'])
                        Annotator = fig['labelerLogin']
                        if dict.get(Annotator) is None:
                            continue
                        if dict[Annotator] == 0:
                            if classobj == 'To Resect':
                                cv2.fillPoly(image_HardN, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Hardexists = True
                            elif classobj == 'To Check':
                                cv2.fillPoly(image_SecuN, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Secuexists = True
                        elif dict[Annotator] == 1:
                            if classobj == 'To Resect':
                                cv2.fillPoly(image_HardJ, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Hardexists = True
                            elif classobj == 'To Check':
                                cv2.fillPoly(image_SecuJ, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Secuexists = True
                        elif dict[Annotator] == 2:
                            if classobj == 'To Resect':
                                cv2.fillPoly(image_HardG, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Hardexists = True
                            elif classobj == 'To Check':
                                cv2.fillPoly(image_SecuG, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Secuexists = True
                        elif dict[Annotator] == 3:
                            if classobj == 'To Resect':
                                cv2.fillPoly(image_HardF, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Hardexists = True
                            elif classobj == 'To Check':
                                cv2.fillPoly(image_SecuF, pts=[np.int32(frcoor)], color=(0, 0, 0))
                                Secuexists = True

                    # save masks and images
                    # save the image frame
                    vidpath = find(evalfr['frame'], vidsPath)  # find the video with the associated json file
                    _, _, vidname = vidpath.rpartition('/')
                    # if vidname == 'P-0266_Video001_trim.mp4':
                    #     continue
                    # print(vidname)
                    # print(Annotator)
                    cv2.imwrite('Dataset/image/' + vidname + "_%d.jpg" % fr['index'],
                                extractFrame(vidpath, fr['index']))  # save frame as JPEG file
                    # cv2.imshow('image window', image_HardN)
                    # cv2.waitKey(0)

                    # save the masks
                    if Hardexists:
                        cv2.imwrite('Dataset/' + maskHarddir + 'N/' + vidname + "_%d.png" % fr['index'], image_HardN)
                        cv2.imwrite('Dataset/' + maskHarddir + 'J/' + vidname + "_%d.png" % fr['index'], image_HardJ)
                        cv2.imwrite('Dataset/' + maskHarddir + 'G/' + vidname + "_%d.png" % fr['index'], image_HardG)
                        cv2.imwrite('Dataset/' + maskHarddir + 'F/' + vidname + "_%d.png" % fr['index'], image_HardF)
                    if Secuexists:
                        cv2.imwrite('Dataset/' + maskSecudir + 'N/' + vidname + "_%d.png" % fr['index'], image_SecuN)
                        cv2.imwrite('Dataset/' + maskSecudir + 'J/' + vidname + "_%d.png" % fr['index'], image_SecuJ)
                        cv2.imwrite('Dataset/' + maskSecudir + 'G/' + vidname + "_%d.png" % fr['index'], image_SecuG)
                        cv2.imwrite('Dataset/' + maskSecudir + 'F/' + vidname + "_%d.png" % fr['index'], image_SecuF)
                    prList.append(project)
                    dsList.append(ds)
                    vidList.append(vidname)
#
# # data_df = pd.DataFrame(
# #     {'Vid. Name': vidList, 'Project': prList, 'Dataset': dsList})
# # sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
# # sheetID = '1UIA6ve-AQi5KMPVONoN5c0yBWLnIQ5RHem383WwqiB4'
# # sheetName = 'info_'+Name#+str(datetime.date.today())
# # # data_df.to_excel('stats-Results.xlsx', sheetName)
# # write_to_gsheet(sfpath, sheetID, sheetName, data_df)
# #
#
#
#
#
#
#
#
#
#
