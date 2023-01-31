import json
import numpy as np
import cv2
from TEst import findClass
jsonfile = '/media/saman/data/PycharmProjects/endoDetection/TESTEST/P-0212_Video002_trim.mp4.json'
videofile = '/media/saman/data/PycharmProjects/endoDetection/TESTEST/P-0212_Video002_trim.mp4'
def extractFrame2(video, frame_number):
    vidcap = cv2.VideoCapture(video)
    for i in range(frame_number+1):
        #vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        res, frame = vidcap.read()
    return frame


# open json
jsfile = open(jsonfile)
annotation = json.load(jsfile)

image_HardJ = np.ones((annotation['size']['height'], annotation['size']['width'])) * 255

frames = annotation['frames']
cap = cv2.VideoCapture(videofile)


for fr in frames:
    if fr['index']==887:
        figures = fr['figures']
        for fig in figures:
            if fig['labelerLogin']=='Jean-Luc.Pouly':
                frcoor = fig['geometry']['points']['exterior']
                print(frcoor)
                classobj = findClass(fig['objectKey'], annotation['objects'])
                if classobj == 'To Resect':
                    cv2.fillPoly(image_HardJ, pts=[np.int32(frcoor)], color=(0, 0, 0))
                    cv2.imwrite("TESTEST/_%d.png" % fr['index'], image_HardJ)
                    cv2.imwrite("TESTEST/2_%d.jpg" % fr['index'],
                               extractFrame2(videofile, fr['index']))  # save frame as JPEG file







