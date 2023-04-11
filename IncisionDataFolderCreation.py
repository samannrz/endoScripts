import json
from functions import *
from PIL import Image, ImageDraw
import cv2

maskHarddir = 'maskHard'
maskSecudir = 'maskSecurity'


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


counter = 0
data_folder = 'annotationData/'  # The destination folder
createDIR(data_folder, 'image')
for firstname in ['N', 'J', 'G', 'F']:
    createDIR('annotationData/', maskHarddir + firstname)
    createDIR('annotationData/', maskSecudir + firstname)
json_eval = open('Evaluation3.json')
eval = json.load(json_eval)
evals = eval['evals']
api, tm = get_supervisely_team()
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

for project in api.project.get_list(ws.id):  # for each project
    if project.name != 'Endometriosis_WS1':
        continue
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
                                            (255, 255, 255))
                    image_SecuN = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))
                    image_HardJ = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))
                    image_SecuJ = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))
                    image_HardG = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))
                    image_SecuG = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))
                    image_HardF = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))
                    image_SecuF = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                            (255, 255, 255))

                    #                 # Create a draw object
                    drawHardN = ImageDraw.Draw(image_HardN)
                    drawSecuN = ImageDraw.Draw(image_SecuN)
                    drawHardJ = ImageDraw.Draw(image_HardJ)
                    drawSecuJ = ImageDraw.Draw(image_SecuJ)
                    drawHardG = ImageDraw.Draw(image_HardG)
                    drawSecuG = ImageDraw.Draw(image_SecuG)
                    drawHardF = ImageDraw.Draw(image_HardF)
                    drawSecuF = ImageDraw.Draw(image_SecuF)
                    maskHardN = image_HardN.convert("L")

                    maskHardN = image_HardN.convert("L")
                    maskSecuN = image_HardN.convert("L")

                    maskHardJ = image_HardN.convert("L")
                    maskSecuJ = image_HardN.convert("L")

                    maskHardG = image_HardN.convert("L")
                    maskSecuG = image_HardN.convert("L")

                    maskHardF = image_HardN.convert("L")
                    maskSecuF = image_HardN.convert("L")

                    dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3}
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
                                drawHardN.polygon(polygon, fill=(0, 0, 0))
                                # Convert the image to a mask
                                maskHardN = image_HardN.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuN.polygon(polygon, fill=(0, 0, 0))
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
                                drawSecuJ.polygon(polygon, fill=(0, 0, 0))
                                maskSecuJ = image_SecuJ.convert("L")
                                Secuexists = True
                        elif dict[Annotator] == 2:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardG.polygon(polygon, fill=(0, 0, 0))
                                # Convert the image to a mask
                                maskHardG = image_HardG.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuG.polygon(polygon, fill=(0, 0, 0))
                                maskSecuG = image_SecuG.convert("L")
                                Secuexists = True
                        elif dict[Annotator] == 3:
                            if classobj == 'To Treat':
                                # Draw the polygon on the image
                                drawHardF.polygon(polygon, fill=(0, 0, 0))
                                # Convert the image to a mask
                                maskHardF = image_HardF.convert("L")
                                Hardexists = True
                            elif classobj == 'To Check':
                                # Draw the polygon on the image
                                drawSecuF.polygon(polygon, fill=(0, 0, 0))
                                maskSecuF = image_SecuF.convert("L")
                                Secuexists = True

                    # save masks and images
                    # extract the image frame
                    fr_names, fr_extracted = get_frames_from_api(api, video_api.id, video_api.name, evalfr['index'])
                    vidname = evalfr['frame']
                    # save frame as png file
                    cv2.imwrite(data_folder + 'image/' + fr_names[0], fr_extracted[0])
                    # save the masks
                    if Hardexists:
                        maskHardN.save(data_folder + maskHarddir + 'N/' + vidname + "_%d.png" % fr['index'], 'PNG')
                        maskHardJ.save(data_folder + maskHarddir + 'J/' + vidname + "_%d.png" % fr['index'], 'PNG')
                        maskHardG.save(data_folder + maskHarddir + 'G/' + vidname + "_%d.png" % fr['index'], 'PNG')
                        maskHardF.save(data_folder + maskHarddir + 'F/' + vidname + "_%d.png" % fr['index'], 'PNG')
                    if Secuexists:
                        maskSecuN.save(data_folder + maskSecudir + 'N/' + vidname + "_%d.png" % fr['index'], 'PNG')
                        maskSecuJ.save(data_folder + maskSecudir + 'J/' + vidname + "_%d.png" % fr['index'], 'PNG')
                        maskSecuG.save(data_folder + maskSecudir + 'G/' + vidname + "_%d.png" % fr['index'], 'PNG')
                        maskSecuF.save(data_folder + maskSecudir + 'F/' + vidname + "_%d.png" % fr['index'], 'PNG')  #
                    counter += 1

print(str(counter) + ' images, masks are saved in ' + data_folder)
