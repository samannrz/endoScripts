import json
import os
import cv2
import numpy as np
import pygsheets
from PIL import Image, ImageDraw
import pandas as pd
# import pygsheets


dataPath = '/media/saman/data/Datasets/FEMaLe/Lesion Classification'
savePath_img = 'LesionDataset/images/'
savePath_lbl = 'LesionDataset/labels/'


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

def createDIR (path):
    # create new directory for images
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The "+ path + " directory is created!")

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

def bbox2yolo(bbox,size):
    xcenter = (bbox[0][0]+bbox[1][0])/(2*size['width'])
    ycenter = (bbox[0][1] + bbox[1][1]) / (2 * size['height'])
    figwidth = (bbox[1][0]-bbox[0][0])/(size['width'])
    figheight = (bbox[1][1]-bbox[0][1])/(size['height'])
    return xcenter ,ycenter, figwidth, figheight


createDIR(savePath_img)
createDIR(savePath_lbl)

if os.path.exists('LogWP6Creation.txt'):
    # The file exists, so delete it
    os.remove('LogWP6Creation.txt')


lesiondic = {
        'Adhesions.Dense': 0,
        'Adhesions.Filmy': 1,
        'Superficial.White': 2,
        'Superficial.Black': 3,
        'Superficial.Red': 4,
        'Superficial.Subtle': 5,
        'Ovarian.Endometrioma': 6,
        'Ovarian.Chocolate Fluid': 7,
        'Deep Endometriosis': 8,
        'Ovarian.Endometrioma[B]': 9
    }

projects = os.listdir(dataPath)
print(dataPath)
for project in projects: # for each project
    print('\nProcessing ' + project + ':')
    if not os.path.isdir(dataPath + '/' +project) :
        continue
    datasets = os.listdir(dataPath + '/' +project)
    imagecounter = 0
    imagecounterBAD = 0
    notsavedlist = []
    for ds in datasets:
        dspath = dataPath + '/' + project +'/'+ ds
        if not os.path.isdir(dspath):
            continue
        print(ds)

        annsPath = dspath +'/ann'
        vidsPath = dspath+'/video'
        jsonFiles = os.listdir(annsPath)
        for js in jsonFiles: #each json file is for one video
            jsfile = open(annsPath+'/'+js)
            annotation = json.load(jsfile)
            frames = (annotation['frames']) # frame is the annotation info (type: list of dict) on that frame
            img_size = annotation['size']

            if len(frames) <1 :  # if there is no annotation on the video
                continue # go to the next jsonfile (and so next video)

            for fr in frames:

                # Create an image with a white background
                figures = fr['figures']
                for fig in figures:
                    if fig['geometryType'] != 'rectangle':
                        continue # go to next figure in the frame if it is not a rectangle
                    bboxes = fig['geometry']['points']['exterior']

                    # bbox is as [[xmin,xmax],[ymin,ymax]]
                    bbox = [b for b in bboxes]
                    # find the class of the polygon
                    classobj = findClass(fig['objectKey'], annotation['objects'])
                    box = bbox2yolo(bbox,img_size)
                    txtline = [(lesiondic[classobj])]+box
                    print(txtline)

                # Save image and annotation files for the frame
                vidpath = find(js[:-5], vidsPath)  # find the video with the associated json file
                _, _, vidname = vidpath.rpartition('/')
                # if the file is already saved, skip
                if os.path.exists(savePath_img + vidname + "_%d.jpg" % fr['index']):
                    continue
                if len(box) == 0:
                    imagecounterBAD +=1
                    continue
                try:
                    cv2.imwrite(savePath_img + vidname + "_%d.jpg" % fr['index'],
                            extractFrame(vidpath, fr['index']))  # save frame as JPEG file
                    # save the label file
                    with open(savePath_lbl + vidname + "_%d.txt" % fr['index'], 'a') as f:
                        f.write('\n'.join([' '.join(txt) for txt in txtline]))

                except cv2.error as e:
                    notsavedlist.append(savePath_img + vidname + ', from project:'+project + ', from dataset:' + ds + ', frame number:'+str(fr['index']))
                    print('This file is not saved: ' + vidname + '_' + str(fr['index']) )
                    imagecounterBAD += 1

                imagecounter += 1
                print(imagecounter)

        # save a log file
        with open('LogWP6Creation.txt', 'a') as f:
            f.write('Project {} '.format(project)+'\n')
            f.write('Dataset {} '.format(ds)+'\n')
            f.write('{} images and annotations are processed to be written to '.format(imagecounter))
            f.write(savePath_img +' and ' +savePath_lbl+ '\n')
            f.write('{} images and annotations are NOT written '.format(imagecounterBAD)+'\n')
            f.write('The images are processed from ' + dataPath+'\n')
            f.write('The followings are not saved' + '\n')
            for i in range(len(notsavedlist)):
                f.write(notsavedlist[i])
            f.write('\n\n')

