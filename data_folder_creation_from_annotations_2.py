# This script goes through all the supervisely videos and extracts all the check and treat masks of the selected annotators
# Please define a list of the annotators that you wish to create the data: ANNOTATORS = []
from functions import *
import numpy
from PIL import Image, ImageDraw

api, tm = get_supervisely_team()
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

ANNOTATOR_DICT = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
                  'incision.consensus': 4}
ANNOTATOR = 0ß
dest_path = '/data/DATA/incision/'
# dest_path = '/Users/saman/Documents/data/DATA/incision/'

createDIR(dest_path, str(ANNOTATOR))
createDIR(os.path.join(dest_path, str(ANNOTATOR)), 'mask')
createDIR(os.path.join(dest_path, str(ANNOTATOR)), 'image')
createDIR(os.path.join(dest_path, str(ANNOTATOR), 'mask'), 'Treat')
createDIR(os.path.join(dest_path, str(ANNOTATOR), 'mask'), 'Check')

COLOR_DICT = {'To Treat': (255, 255, 255), 'To Check': (255, 255, 255)}


# list_consensus_8 = os.listdir('/data/DATA/DELPHI_incision/consensus8')
# list_consensus_9 = os.listdir('/data/DATA/DELPHI_incision/consensus9')
#
# list8 = [im[:-6] + im[-4:] for im in list_consensus_8]
# list9 = [im[:-6] + im[-4:] for im in list_consensus_9]
#
# list8_9 = list(set(list8)) + list(set(list9))
#
# im_list = os.listdir('/data/projects/IncisionDeepLab/input/incision/orig_data_all/valid_images')


def saveMask(classobj, polygon, vd, fr_name, save_path):
    img = Image.new('RGB', (vd['size']['width'], vd['size']['height']), (0, 0, 0))
    ImageDraw.Draw(img).polygon(polygon, fill=COLOR_DICT[classobj])
    img.save(os.path.join(save_path, fr_name))


for project in api.project.get_list(ws.id):  # for each project
    # if project.name == 'Endometriosis_WS7' or  project.name == 'Endometriosis_WS1' or  project.name == 'Endometriosis_WS2' :
    #     continue
    if project.type != 'videos':
        continue
    for ds in api.dataset.get_list(project.id):
        print(project.name)
        print(ds.name)
        for vd in api.video.get_list(ds.id):
            annotation = api.video.annotation.download(vd.id)
            frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame
            for fr in frames:
                # if vd.name + '_'+str(fr['index']).zfill(5)+'.png' not in list8_9:
                #     continue
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
                    if not os.path.exists( os.path.join(dest_path, str(ANNOTATOR), 'image', fr_names[0])):
                        cv2.imwrite(os.path.join(dest_path, str(ANNOTATOR), 'image', fr_names[0]),
                                     cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))

                        img_check.save(os.path.join(dest_path, str(ANNOTATOR), 'mask', 'Check', fr_names[0]))
                        img_treat.save(os.path.join(dest_path, str(ANNOTATOR), 'mask', 'Treat', fr_names[0]))
                        print(vd.name, fr['index'], ': SAVED')


    print('\n')
