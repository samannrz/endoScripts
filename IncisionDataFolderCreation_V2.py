import json
import shutil

from functions import *
from PIL import Image, ImageDraw
import cv2

# batch_num = 3
dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
        'Ervin.Kalfa': 4, 'ebbe.thinggaard': 5}
annotator = 'Ervin.Kalfa'
save_image = True
for batch_num in [21]:

    data_folder = 'annotationData/'  # The destination folder

    maskTreatdir = 'maskTreat'
    maskCheckdir = 'maskCheck'

    counter = 0
    shutil.rmtree(data_folder)
    createDIR(data_folder, 'image')
    createDIR(data_folder, maskTreatdir + '_'+ annotator)
    createDIR(data_folder, maskCheckdir + '_'+ annotator)

    json_eval = open('Evaluation' + str(batch_num) + '.json')
    eval = json.load(json_eval)
    evals = eval['evals']
    print(len(evals))
    api, tm = get_supervisely_team()
    ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

    for project in api.project.get_list(ws.id):  # for each project
        if project.name != 'Endometriosis_WS9':
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

                        image_Treat = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                                (0, 0, 0))

                        image_Check = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                                (0, 0, 0))

                        # Create a draw object
                        drawTreat = ImageDraw.Draw(image_Treat)
                        drawCheck = ImageDraw.Draw(image_Check)

                        maskTreat = image_Treat.convert("L")
                        maskCheck = image_Check.convert("L")

                        Treatexists = False
                        Checkexists = False
                        if fr['index'] not in evalfr['index']:
                            continue

                        figures = fr['figures']
                        for fig in figures:
                            # find the class of the polygon
                            classobj = findClass(fig['objectId'], annotation['objects'])
                            Annotator = fig['labelerLogin']
                            if dict.get(Annotator) is None:
                                continue

                            frcoor = fig['geometry']['points']['exterior']
                            polygon = [tuple(coor) for coor in frcoor]
                            if dict[Annotator] != dict[annotator]:
                                continue
                            else:
                                if classobj == 'To Treat':
                                    # Draw the polygon on the image
                                    drawTreat.polygon(polygon, fill=(255, 255, 255))
                                    # Convert the image to a mask
                                    maskTreat = image_Treat.convert("L")
                                    Hardexists = True
                                elif classobj == 'To Check':
                                    # Draw the polygon on the image
                                    drawCheck.polygon(polygon, fill=(255, 255, 255))
                                    maskCheck = image_Check.convert("L")
                                    Secuexists = True
                        # save masks and images
                        # extract the image frame
                        fr_names, fr_extracted = get_frames_from_api(api, video_api.id, video_api.name, evalfr['index'])
                        vidname = evalfr['frame']
                        print(vidname)
                        # save frame as png file
                        if save_image:
                            cv2.imwrite(data_folder + 'image/' + fr_names[0],
                                        cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))
                        # save the masks
                        maskTreat.save(os.path.join(data_folder + maskTreatdir + '_' + annotator,
                                                    vidname + '_' + str(fr['index']).zfill(5) + '.png'), 'PNG')
                        maskCheck.save(os.path.join(data_folder + maskCheckdir + '_' + annotator,
                                                    vidname + '_' + str(fr['index']).zfill(5) + '.png'), 'PNG')

                        counter += 1

    print('Batch_num ' + str(batch_num) + ' : ' + str(
        counter) + ' images, masks are saved in ' + data_folder + ' : ' + annotator)
    # with open("comparison_consensus.py.py") as f:
    #     exec(f.read())
