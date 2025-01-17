# This script goes through all the supervisely videos and extracts all the check and treat masks of the selected annotators
# Please define a list of the annotators that you wish to create the data: ANNOTATORS = []
import os

import numpy as np

from functions import *
import numpy
from PIL import Image, ImageDraw

api, tm = get_supervisely_team()
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

ANNOTATOR_DICT = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
                  'Ervin.Kallfa': 5, 'ebbe.thinggaard': 6, 'incision.consensus': 4}
ANNOTATOR_DICT_juniors = {'oscar.perch': 7, 'anne-sofie.petersen': 8, 'gry.oslen': 9, 'j.incision.consensus': 10}
ANNOTATOR_DICT = ANNOTATOR_DICT
ANNOTATOR = 6
print(ANNOTATOR)
dest_path = '/data/DATA/incision/'
# dest_path = '/Users/saman/Documents/data/DATA/incision/'

createDIR(dest_path, str(ANNOTATOR))
createDIR(os.path.join(dest_path, str(ANNOTATOR)), 'mask')
createDIR(os.path.join(dest_path, str(ANNOTATOR)), 'image')
createDIR(os.path.join(dest_path, str(ANNOTATOR), 'mask'), 'Treat')
createDIR(os.path.join(dest_path, str(ANNOTATOR), 'mask'), 'Check')

COLOR_DICT = {'To Treat': (255, 255, 255), 'To Check': (255, 255, 255)}

videos_bug_path = 'videos_with_bugs.txt'
with open(videos_bug_path, 'r') as file:
    # Read all lines, remove newline characters, and store them in an array
    buggy_videos = [line.rstrip() for line in file]

# Print the array containing all lines
print(buggy_videos)

list_bugs = []
def saveMask(classobj, polygon, vd, fr_name, save_path):
    img = Image.new('RGB', (vd['size']['width'], vd['size']['height']), (0, 0, 0))
    ImageDraw.Draw(img).polygon(polygon, fill=COLOR_DICT[classobj])
    img.save(os.path.join(save_path, fr_name))


for project in api.project.get_list(ws.id):  # for each project

    if project.type != 'videos':
        continue
    for ds in api.dataset.get_list(project.id):
        print(project.name)
        print(ds.name)
        saveasbad = 1
        for vd in api.video.get_list(ds.id):
            # if ANNOTATOR == 3 and vd.name in buggy_videos:
            #     saveasbad = 1
            to_discuss = []
            annotation = api.video.annotation.download(vd.id)
            # tags = annotation['tags']
            # for tg in tags:
            #     if tg['name'] == 'Annot. to discuss':
            #         to_discuss.append(tg['frameRange'][0])

            frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame
            for fr in frames:
                # if fr['index'] not in to_discuss:
                #     continue
                img_treat = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']), (0, 0, 0))
                img_check = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']), (0, 0, 0))
                polygon = []
                SAVE_SIGNAL = False
                for fig in fr['figures']:
                    classobj = findClass(fig['objectId'], annotation['objects'])
                    annotator = fig['labelerLogin']
                    if classobj != 'To Treat' and classobj != 'To Check':
                        continue
                    if ANNOTATOR_DICT.get(annotator) is None:
                        continue
                    if ANNOTATOR_DICT[annotator] != ANNOTATOR:
                        continue
                    frcoor = fig['geometry']['points']['exterior']
                    polygon = [tuple(coor) for coor in frcoor]


                    if classobj == 'To Treat':
                        ImageDraw.Draw(img_treat).polygon(polygon, fill=COLOR_DICT[classobj])
                    if classobj == 'To Check':
                        ImageDraw.Draw(img_check).polygon(polygon, fill=COLOR_DICT[classobj])
                    SAVE_SIGNAL = True

                if SAVE_SIGNAL and saveasbad==1:
                    if vd.name in buggy_videos:
                        list_bugs.append(vd.name)

                    fr_names, fr_extracted = get_frames_from_api(api, vd.id, vd.name, [fr['index']])
                    # if fr_names[0] in os.listdir("/data/projects/IncisionDeepLab/input/inference_data_1-28/test_with_consensus/test_images"):
                    if not os.path.exists(os.path.join(dest_path, str(ANNOTATOR), 'image', fr_names[0])):
                        cv2.imwrite(os.path.join(dest_path, str(ANNOTATOR), 'image', fr_names[0]),
                                    cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))
                        cv2.imwrite(os.path.join(dest_path, str(ANNOTATOR), 'mask', 'Check', fr_names[0]),
                                    cv2.cvtColor(np.array(img_check), cv2.COLOR_BGR2RGB))
                        #img_check.save()
                        cv2.imwrite(os.path.join(dest_path, str(ANNOTATOR), 'mask', 'Treat', fr_names[0]),
                                    cv2.cvtColor(np.array(img_treat), cv2.COLOR_BGR2RGB))
                        #img_treat.save()
                        print(vd.name, fr['index'], ': SAVED')

    print('\n')
for i in list_bugs:
    print(i)
