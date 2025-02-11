# This script goes through all the supervisely videos and extracts all the check and treat masks of the selected annotators
# Please define a list of the annotators that you wish to create the data: ANNOTATORS = []
from functions import *
import numpy
from PIL import Image, ImageDraw

api, tm = get_supervisely_team()
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

ANNOTATOR_DICT = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
                  'incision.consensus': 4}
ANNOTATOR = 3
dest_path = '/data/DATA/incision'
# dest_path = '/data/DATA/incision/test'

createDIR(dest_path, str(ANNOTATOR))
createDIR(os.path.join(dest_path, str(ANNOTATOR)), 'mask')
createDIR(os.path.join(dest_path, str(ANNOTATOR)), 'image')
createDIR(os.path.join(dest_path, str(ANNOTATOR), 'mask'), 'Treat')
createDIR(os.path.join(dest_path, str(ANNOTATOR), 'mask'), 'Check')

COLOR_DICT = {'To Treat': (255, 255, 255), 'To Check': (255, 255, 255)}


def saveMask(classobj, polygon, vd, fr_name, save_path):
    img = Image.new('RGB', (vd['size']['width'], vd['size']['height']), (0, 0, 0))
    ImageDraw.Draw(img).polygon(polygon, fill=COLOR_DICT[classobj])
    img.save(os.path.join(save_path, fr_name))


for project in api.project.get_list(ws.id):  # for each project

    for ds in api.dataset.get_list(project.id):
        for vd in api.video.get_list(ds.id):
            annotation = api.video.annotation.download(vd.id)
            frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame

            for fr in frames:
                img_treat = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']), (0, 0, 0))
                img_check = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']), (0, 0, 0))
                polygon=[]
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
                if SAVE_SIGNAL:
                    fr_names, fr_extracted = get_frames_from_api(api, vd.id, vd.name, [fr['index']])
                    # if not os.path.exists( os.path.join(dest_path_old, str(ANNOTATOR), 'image', fr_names[0])):
                    cv2.imwrite(os.path.join(dest_path, str(ANNOTATOR), 'image', fr_names[0]),
                                 cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))
                     # saveMask(classobj, polygon, annotation, fr_names[0],
                     #          os.path.join(dest_path, str(ANNOTATOR_DICT[annotator]), 'mask', classobj[3:]))
                    img_check.save(os.path.join(dest_path, str(ANNOTATOR), 'mask', 'Check', fr_names[0]))
                    img_treat.save(os.path.join(dest_path, str(ANNOTATOR), 'mask', 'Treat', fr_names[0]))


