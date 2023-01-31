import json
import os
import cv2
import numpy as np
import pygsheets
from PIL import Image, ImageDraw
import pandas as pd
# import pygsheets


dataPath = '/media/saman/data/Datasets/FEMaLe/WP6/SuperviselyData'
savePath = 'LesionDataset/'

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


createDIR(savePath)
projects =os.listdir (dataPath)
if os.path.exists('LogWP6Creation.txt'):
    # The file exists, so delete it
    os.remove('LogWP6Creation.txt')


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
            if len(frames) <1 :  # if there is no annotation on the video
                continue # go to the next jsonfile (and so next video)

            for fr in frames:

                new_dict = {'bb': [], 'label': []}
                # Create an image with a white background
                figures = fr['figures']
                for fig in figures:
                    if fig['geometryType'] != 'rectangle':
                        continue # go to next object in the frame if it is not a rectangle
                    bboxes = fig['geometry']['points']['exterior']
                    bbox = [b for b in bboxes]
                    #find the class of the polygon
                    classobj = findClass(fig['objectKey'], annotation['objects'])

                    #make the annotations for the frame
                    new_dict['bb'].append(bbox)
                    new_dict['label'].append(classobj)

                # Save image and annotation files for the frame
                vidpath = find(js[:-5], vidsPath)  # find the video with the associated json file
                _, _, vidname = vidpath.rpartition('/')
                # if the file is already saved, skip
                if os.path.exists(savePath + vidname + "_%d.jpg" % fr['index']):
                    continue
                if len(new_dict['bb']) == 0:
                    continue
                try:
                    cv2.imwrite(savePath + vidname + "_%d.jpg" % fr['index'],
                            extractFrame(vidpath, fr['index']))  # save frame as JPEG file
                    with open(savePath + vidname + "_%d.json" % fr['index'], 'w') as f:
                        json.dump(new_dict, f) # save tha bb annotation
                except cv2.error as e:
                    notsavedlist.append(savePath + vidname + ', from project:'+project + ', from dataset:' + ds + ', frame number:'+str(fr['index']))
                    print('This file is not saved ' + savePath + vidname + '_' + str(fr['index']) )
                    imagecounterBAD += 1

                imagecounter += 1
                print(imagecounter)

        # save a log file
        with open('LogWP6Creation.txt', 'a') as f:
            f.write('Project {} '.format(project)+'\n')
            f.write('Dataset {} '.format(ds)+'\n')
            f.write('{} images and annotations are processed to be written to '.format(imagecounter))
            f.write(savePath + '\n')
            f.write('{} images and annotations are NOT written '.format(imagecounterBAD)+'\n')
            f.write('The images are processed from ' + dataPath+'\n')
            f.write('The followings are not saved' + '\n')
            for i in range(len(notsavedlist)):
                f.write(notsavedlist[i])
            f.write('\n\n')











