import json
import shutil

from functions import *
from PIL import Image, ImageDraw
import cv2

batch_num = 100
#data_folder = 'annotationData/'  # The destination folder
data_folder = '/data/DATA/DELPHI_incision/'  # The destination folder

maskHarddir = 'maskTreat'
maskSecudir = 'maskCheck'
dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
        'incision.consensus': 4}


counter = 0
shutil.rmtree(data_folder)
createDIR(data_folder, 'image')
for firstname in [s[0].upper() for s in list(dict.keys())]:
    createDIR(data_folder, maskHarddir + firstname)
    createDIR(data_folder, maskSecudir + firstname)
if batch_num == 100:
    json_eval = open('Evaluation_all' + '.json')
else:
    json_eval = open('Evaluation' + str(batch_num) + '.json')
eval = json.load(json_eval)
evals = eval['evals']
print(len(evals))
api, tm = get_supervisely_team()
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')


for project in api.project.get_list(ws.id):  # for each project
    # if project.name != 'Endometriosis_WS8' and project.name != 'Endometriosis_WS7':
    #     continue
    for ds in api.dataset.get_list(project.id):
        evalfr = evals[0]
        for evalfr in evals:
            videos_in_ds = [vid_info.name for vid_info in api.video.get_list(ds.id)]
            if evalfr['frame'] in videos_in_ds:
                video_api = api.video.get_info_by_name(ds.id, evalfr['frame'])
                annotation = api.video.annotation.download(video_api.id)
                frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame
                if len(frames) < 1:  # if there is no annotation on the video
                    continue  # go to the next jsonfile (and next video)
                for fr in frames:
                    # Create an image with a white background
                    image_HardN = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_SecuN = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_HardJ = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_SecuJ = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_HardG = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_SecuG = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_HardF = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_SecuF = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_HardC = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))
                    image_SecuC = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (0, 0, 0))


                    #                 # Create a draw object
                    drawHardN = ImageDraw.Draw(image_HardN)
                    drawSecuN = ImageDraw.Draw(image_SecuN)
                    drawHardJ = ImageDraw.Draw(image_HardJ)
                    drawSecuJ = ImageDraw.Draw(image_SecuJ)
                    drawHardG = ImageDraw.Draw(image_HardG)
                    drawSecuG = ImageDraw.Draw(image_SecuG)
                    drawHardF = ImageDraw.Draw(image_HardF)
                    drawSecuF = ImageDraw.Draw(image_SecuF)
                    drawHardC = ImageDraw.Draw(image_HardC)
                    drawSecuC = ImageDraw.Draw(image_SecuC)

                    maskHardN = image_HardN.convert("L")
                    maskSecuN = image_SecuN.convert("L")

                    maskHardJ = image_HardJ.convert("L")
                    maskSecuJ = image_SecuJ.convert("L")

                    maskHardG = image_HardG.convert("L")
                    maskSecuG = image_SecuG.convert("L")

                    maskHardF = image_HardF.convert("L")
                    maskSecuF = image_SecuF.convert("L")

                    maskHardC = image_HardC.convert("L")
                    maskSecuC = image_SecuC.convert("L")

                    Hardexists = False
                    Secuexists = False
                    if fr['index'] not in evalfr['index']:
                        continue
                    # print(evalfr['frame'])
                    # print(fr['index'])
                    figures = fr['figures']
                    for fig in figures:
                        # find the class of the polygon
                        classobj = findClass(fig['objectId'], annotation['objects'])
                        Annotator = fig['labelerLogin']
                        if dict.get(Annotator) is None:
                            continue
                        # print(evalfr['frame'] + ' ' + str(evalfr['index']) + ' ' + classobj + ' ' + Annotator)
                        frcoor = fig['geometry']['points']['exterior']
                        polygon = [tuple(coor) for coor in frcoor]
                        if dict[Annotator] == 0:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardN.polygon(polygon, fill=(255, 255, 255))
                                # Convert the image to a mask
                                maskHardN = image_HardN.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuN.polygon(polygon, fill=(255, 255, 255))
                                maskSecuN = image_SecuN.convert("L")
                                Secuexists = True
                        elif dict[Annotator] == 1:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardJ.polygon(polygon, fill=(0, 0, 0))
                                # Convert the image to a mask
                                maskHardJ = image_HardJ.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuJ.polygon(polygon, fill=(255, 255, 255))
                                maskSecuJ = image_SecuJ.convert("L")
                                Secuexists = True
                        elif dict[Annotator] == 2:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardG.polygon(polygon, fill=(255, 255, 255))
                                # Convert the image to a mask
                                maskHardG = image_HardG.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuG.polygon(polygon, fill=(255, 255, 255))
                                maskSecuG = image_SecuG.convert("L")
                                Secuexists = True
                        elif dict[Annotator] == 3:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardF.polygon(polygon, fill=(255, 255, 255))
                                # Convert the image to a mask
                                maskHardF = image_HardF.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuF.polygon(polygon, fill=(255, 255, 255))
                                maskSecuF = image_SecuF.convert("L")
                                Secuexists = True
                        elif dict[Annotator] == 4:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardC.polygon(polygon, fill=(255, 255, 255))
                                # Convert the image to a mask
                                maskHardC = image_HardC.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuC.polygon(polygon, fill=(255, 255, 255))
                                maskSecuC = image_SecuC.convert("L")
                                Secuexists = True

                    # save masks and images
                    # extract the image frame
                    fr_names, fr_extracted = get_frames_from_api(api, video_api.id, video_api.name, evalfr['index'])
                    vidname = evalfr['frame']
                    # save frame as png file
                    cv2.imwrite(data_folder + 'image/' + fr_names[0], cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))
                    # save the masks
                    if Hardexists:
                        maskHardN.save(
                            data_folder + maskHarddir + 'N/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskHardJ.save(
                            data_folder + maskHarddir + 'J/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskHardG.save(
                            data_folder + maskHarddir + 'G/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskHardF.save(
                            data_folder + maskHarddir + 'F/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskHardC.save(
                            data_folder + maskHarddir + 'I/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                    if Secuexists:
                        maskSecuN.save(
                            data_folder + maskSecudir + 'N/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskSecuJ.save(
                            data_folder + maskSecudir + 'J/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskSecuG.save(
                            data_folder + maskSecudir + 'G/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')
                        maskSecuF.save(
                            data_folder + maskSecudir + 'F/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')  #
                        maskSecuC.save(
                            data_folder + maskSecudir + 'I/' + vidname + '_' + str(fr['index']).zfill(5) + '.png',
                            'PNG')  #
                    counter += 1

print(str(counter) + ' images, masks are saved in ' + data_folder)
