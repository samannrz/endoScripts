import argparse
import json
import sys

from dotenv import load_dotenv
import supervisely_lib as sly
from functions import createDIR
from PIL import Image, ImageDraw
import cv2
def main():
    parser = argparse.ArgumentParser('To extract images and annotations of a batch')
    parser.add_argument('--batch', help='Enter batch number')
    parser.add_argument('--annotator', help='Enter the supervisely id of the annotator: e.g. nicolas.bourdel')
    parser.add_argument('--output', default='annotationData/', help='Enter path of dest. folder or skip')
    parser.add_argument('--outputtreat', default='maskTreat', help='Enter path of dest. folder or skip')
    parser.add_argument('--outputcheck', default='maskCheck', help='Enter path of dest. folder or skip')
    parser.add_argument('--project', default='Endometriosis_WS10', help='supervisely projectname')

    args = parser.parse_args()
    annotator = args.annotator
    batch_num = args.batch
    dict = {'nicolas.bourdel': 0, 'Jean-Luc.Pouly': 1, 'giuseppe.giacomello': 2, 'filippo.ferrari': 3,
            'Ervin.Kallfa': 4, 'ebbe.thinggaard': 5, 'incision.consensus': 6, 'oscar.perch': 7, 'anne-sofie.petersen': 8,
            'gry.olsen': 9, 'j.incision.consensus': 10}
    # annotator ='incision.consensus'
    print(annotator)
    data_folder = args.output  # The destination folder
    maskTreatdir = args.outputtreat
    maskCheckdir = args.outputcheck

    counter = 0

    createDIR(data_folder, 'image')
    createDIR(data_folder, maskTreatdir + '_' + annotator[:2])
    createDIR(data_folder, maskCheckdir + '_' + annotator[:2])

    json_eval = open('../../../data/Evaluations_json/' + 'Evaluation' + str(batch_num) + '.json')
    eval = json.load(json_eval)
    evals = eval['evals']
    print(str(len(evals)) + ' images')
    if sly.is_development():
        load_dotenv(os.path.expanduser("~/supervisely.env"))
    api = sly.Api.from_env()
    tm = api.team.get_info_by_name('Endometriosis')
    ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

    for project in api.project.get_list(ws.id):  # for each project
        if project.name != args.project:
            continue
        for ds in api.dataset.get_list(project.id):
            if project.name == 'Endometriosis_WS4':
                if ds.name == 'Revise_Consensus':
                    continue
            evalfr = evals[0]
            for evalfr in evals:
                videos_in_ds = [vid_info.name for vid_info in api.video.get_list(ds.id)]

                if evalfr['frame'] in videos_in_ds:
                    video_api = api.video.get_info_by_name(ds.id, evalfr['frame'])
                    annotation = api.video.annotation.download(video_api.id)
                    frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame
                    vidname = evalfr['frame']

                    # if vidname != '2020-11-16_004658_VID001_Trim.mp4':
                    #     continue
                    # extract the image frame

                    fr_names, fr_extracted = get_frames_from_api(api, video_api.id, video_api.name, evalfr['index'])

                    if len(frames) < 1:  # if there is no annotation on the video
                        continue  # go to the next jsonfile (and next video)
                    for fr in frames:

                        image_Treat = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                                (0, 0, 0))
                        image_Check = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                                (0, 0, 0))

                        # Create a draw object
                        drawTreat = ImageDraw.Draw(image_Treat)
                        drawCheck = ImageDraw.Draw(image_Check)

                        maskTreat = image_Treat.convert("L")
                        maskCheck = image_Check.convert("L")

                        if fr['index'] not in evalfr['index']:
                            continue

                        figures = fr['figures']
                        for fig in figures:
                            #print(fig.keys())
                            # find the class of the polygon
                            classobj = findClass(fig['objectId'], annotation['objects'])
                            Annotator = fig['labelerLogin']

                            if dict.get(Annotator) is None:
                                continue

                            frcoor = fig['geometry']['points']['exterior']

                            polygon = [tuple(coor) for coor in frcoor]
                            try:
                                dict[annotator]
                            except:
                                print('ERROR: No Annotator:' + annotator)
                                sys.exit(1)


                            if dict[Annotator] != dict[annotator]:
                                continue

                            else:
                                if classobj == 'To Treat':
                                    # Draw the polygon on the image
                                    drawTreat.polygon(polygon, fill=(255, 255, 255))
                                    # Convert the image to a mask
                                    maskTreat = image_Treat.convert("L")
                                elif classobj == 'To Check':
                                    # Draw the polygon on the image
                                    drawCheck.polygon(polygon, fill=(255, 255, 255))
                                    maskCheck = image_Check.convert("L")

                        # save masks and images
                        vidname = evalfr['frame']
                        # extract the image frame
                        fr_names, fr_extracted = get_frames_from_api(api, video_api.id, video_api.name, evalfr['index'])
                        # maskCheck_array = np.array(maskCheck)
                        # maskTreat_array = np.array(maskTreat)
                        # # Perform pixel-wise logical AND
                        # result_array = np.logical_and(maskCheck_array, maskTreat_array)
                        # # Identify the indices where both masks are true
                        # rows, cols = np.where(result_array)
                        # background_value = 0
                        # # Update 'maskCheck' at the identified pixels to the background value
                        # maskCheck_array[rows, cols] = background_value
                        # # Convert the updated NumPy array back to a PIL Image
                        # maskCheck = Image.fromarray(maskCheck_array)

                        # save frame as png file


                        cv2.imwrite(os.path.join(data_folder, 'image', fr_names[0]),
                                    cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))
                        if not os.path.exists(os.path.join(data_folder, maskTreatdir + '_' + annotator[:2],
                                                           vidname + '_' + str(fr['index']).zfill(5) + '.png')):
                            cv2.imwrite(os.path.join(data_folder, maskTreatdir + '_' + annotator[:2],
                                                 vidname + '_' + str(fr['index']).zfill(5) + '.png'),
                                    cv2.cvtColor(np.array(maskTreat), cv2.COLOR_BGR2RGB))
                        if not os.path.exists(os.path.join(data_folder, maskCheckdir + '_' + annotator[:2],
                                                           vidname + '_' + str(fr['index']).zfill(5) + '.png')):
                            cv2.imwrite(os.path.join(data_folder, maskCheckdir + '_' + annotator[:2],
                                                 vidname + '_' + str(fr['index']).zfill(5) + '.png'),
                                    cv2.cvtColor(np.array(maskCheck), cv2.COLOR_BGR2RGB))
                        #print(vidname)

                        counter += 1

    print('Batch_num ' + str(batch_num) + ' : ' + str(
        counter) + ' images, masks are saved in ' + data_folder + ' : ' + annotator)

if __name__ == '__main__':
    main()