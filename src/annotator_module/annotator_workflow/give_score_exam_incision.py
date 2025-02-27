'''
After an Exam, the results are saved and calculated through this script
Args:
    exam_dataset_id
    data_folder: the path of the destination folder to save the results
    consensus_path: this should contain the consensus(reference) images (just for their names) which are saved somewhere
Returns:
    float: the calculated score is printed out
    the results are saved in data_folder

'''
from dotenv import load_dotenv
from functions import createDIR, findClass, get_frames_from_api
import supervisely_lib as sly
from PIL import Image, ImageDraw, ImageFont
import cv2, os, shutil


exam_dataset_id = 2739  # V1-Session1=2739 V1-Session2=2765
data_folder = 'Exam/'  # The destination folder
consensus_path = '/data/DATA/incision/4/image'

annotator_examed = 'anne-sofie.petersen'
annotator_ref = 'saman.noorzadeh'

maskHarddir = 'maskTreat'
maskSecudir = 'maskCheck'

if os.path.exists(os.path.join(data_folder, 'image')):
    shutil.rmtree(os.path.join(data_folder, 'image'))

createDIR(data_folder, 'image')
createDIR(data_folder, 'Res')
createDIR(data_folder, maskHarddir + annotator_examed[0])
createDIR(data_folder, maskHarddir + annotator_ref[0])
createDIR(data_folder, maskSecudir + annotator_examed[0])
createDIR(data_folder, maskSecudir + annotator_ref[0])
if sly.is_development():
    load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api.from_env()
tm = api.team.get_info_by_name('Endometriosis')
AR_list = []
images = os.listdir(consensus_path)
for vd in api.video.get_list(exam_dataset_id):
    index = [im for im in images if im.startswith(vd.name)]
    index = int(index[0][-9:-4])

    video_api = api.video.get_info_by_name(exam_dataset_id, vd.name)
    annotation = api.video.annotation.download(video_api.id)
    frames = annotation['frames']  # frame is the annotation info (type: list of dict) on that frame
    image_Hard_ann = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                               (0, 0, 0))
    image_Secu_ann = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                               (0, 0, 0))
    image_Hard_ref = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                               (0, 0, 0))
    image_Secu_ref = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                               (0, 0, 0))

    # Create a draw object
    drawHard_ann = ImageDraw.Draw(image_Hard_ann)
    drawSecu_ann = ImageDraw.Draw(image_Secu_ann)
    maskHard_ann = image_Hard_ann.convert("L")
    maskSecu_ann = image_Secu_ann.convert("L")

    drawHard_ref = ImageDraw.Draw(image_Hard_ref)
    drawSecu_ref = ImageDraw.Draw(image_Secu_ref)
    maskHard_ref = image_Hard_ref.convert("L")
    maskSecu_ref = image_Secu_ref.convert("L")
    for fr in frames:

        if int(fr['index']) != index:
            # print(fr['index'], index)
            continue
        figures = fr['figures']
        for fig in figures:
            # find the class of the polygon
            classobj = findClass(fig['objectId'], annotation['objects'])
            frcoor = fig['geometry']['points']['exterior']
            polygon = [tuple(coor) for coor in frcoor]
            Annotator = fig['labelerLogin']

            if Annotator == annotator_examed:

                if classobj == 'To Treat':
                    # Draw the polygon on the image
                    drawHard_ann.polygon(polygon, fill=(255, 255, 255))
                    # Convert the image to a mask
                    maskHard_ann = image_Hard_ann.convert("L")
                elif classobj == 'To Check':
                    # Draw the polygon on the image
                    drawSecu_ann.polygon(polygon, fill=(255, 255, 255))
                    maskSecu_ann = image_Secu_ann.convert("L")
            if Annotator == annotator_ref:
                if classobj == 'To Treat':
                    # Draw the polygon on the image
                    drawHard_ref.polygon(polygon, fill=(255, 255, 255))
                    # Convert the image to a mask
                    maskHard_ref = image_Hard_ref.convert("L")
                elif classobj == 'To Check':
                    # Draw the polygon on the image
                    drawSecu_ref.polygon(polygon, fill=(255, 255, 255))
                    maskSecu_ref = image_Secu_ref.convert("L")
        print(video_api.id, video_api.name)
        fr_names, fr_extracted = get_frames_from_api(api, video_api.id, video_api.name, [index])
        vidname = vd.name
        cv2.imwrite(data_folder + 'image/' + fr_names[0], cv2.cvtColor(fr_extracted[0], cv2.COLOR_BGR2RGB))
        # save the masks
        maskHard_ann.save(
            data_folder + maskHarddir + annotator_examed[0] + '/' + vd.name + '_' + str(fr['index']).zfill(5) + '.png',
            'PNG')
        maskSecu_ann.save(
            data_folder + maskSecudir + annotator_examed[0] + '/' + vd.name + '_' + str(fr['index']).zfill(5) + '.png',
            'PNG')
        maskHard_ref.save(
            data_folder + maskHarddir + annotator_ref[0] + '/' + vd.name + '_' + str(fr['index']).zfill(5) + '.png',
            'PNG')
        maskSecu_ref.save(
            data_folder + maskSecudir + annotator_ref[0] + '/' + vd.name + '_' + str(fr['index']).zfill(5) + '.png',
            'PNG')


######################################################
######################################################
def initializeMask(size):
    a = Image.new(mode="RGBA", size=(size[0], size[1]), color="black")
    return a


space_height = 120
hh = 100

images = os.listdir(data_folder + 'image')
im3 = Image.new("RGB", (3 * 1920 + 20, hh + (len(images)) * 1080 + space_height * len(images)), (255, 255, 255))

for i in range(len(images)):
    image_orig = Image.open(os.path.join(data_folder, 'image', images[i]))

    maskH_ann = initializeMask(image_orig.size)
    maskS_ann = initializeMask(image_orig.size)
    maskH_ref = initializeMask(image_orig.size)
    maskS_ref = initializeMask(image_orig.size)
    try:
        maskH_ann = Image.open(os.path.join(data_folder, 'maskTreat' + annotator_examed[0], images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on examed\'s annot on ' + images[i][:-4])
    try:
        maskS_ann = Image.open(os.path.join(data_folder, 'maskCheck' + annotator_examed[0], images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on examed\'s annot on ' + images[i][:-4])
    #### Jean Luc ####
    try:
        maskH_ref = Image.open(os.path.join(data_folder, 'maskTreat' + annotator_ref[0], images[i][:-4] + '.png'))
    except:
        print('There is no Hard Zone on ref\'s annot on ' + images[i][:-4])
    try:
        maskS_ref = Image.open(os.path.join(data_folder, 'maskCheck' + annotator_ref[0], images[i][:-4] + '.png'))
    except:
        print('There is no Security Zone on ref\'s annot on ' + images[i][:-4])

    maskH_ann_array = np.array(maskH_ann.convert('1'))
    maskS_ann_array = np.array(maskS_ann.convert('1'))
    maskH_ref_array = np.array(maskH_ref.convert('1'))
    maskS_ref_array = np.array(maskS_ref.convert('1'))

    try:
        # score of Hard zones with ANNOT & ref
        AR_treat = round((np.count_nonzero(maskH_ann_array & maskH_ref_array) / np.count_nonzero(
            maskH_ref_array | maskH_ann_array)) * 100, 2)
    except ZeroDivisionError:
        AR_treat = 1

    try:
        # score of Check zones with ANNOT & ref
        AR_check = round((np.count_nonzero(maskS_ann_array & maskS_ref_array) / np.count_nonzero(
            maskS_ann_array | maskS_ref_array)) * 100, 2)
    except ZeroDivisionError:
        AR_check = 1
    AR_list.append(AR_check)
    AR_list.append(AR_treat)

    image_overlayed_ref = overlayMasks_incision(image_orig, maskH_ann, maskS_ann)
    image_overlayed_ann = overlayMasks_incision(image_orig, maskH_ref, maskS_ref)
    if image_overlayed_ref.width < 1920:
        newsize = (1920, 1080)
        image_overlayed_ref = image_overlayed_ref.resize(newsize)
        image_overlayed_ann = image_overlayed_ann.resize(newsize)
        image_orig = image_orig.resize(newsize)

    WIDTH = image_overlayed_ref.width
    HEIGHT = image_orig.height
    # Paste the images onto the white background

    im3.paste(image_orig, (0, hh + space_height))
    im3.paste(image_overlayed_ref, (WIDTH + 10, hh + space_height))
    im3.paste(image_overlayed_ann, (2 * WIDTH + 20, hh + space_height))

    draw = ImageDraw.Draw(im3)
    font1 = ImageFont.truetype("../../arial.ttf", 50)
    font = ImageFont.truetype("../../arial.ttf", 100)
    color_check = 'red'
    color_treat = 'red'
    if AR_check > 25:
        color_check = 'green'
    if AR_treat > 25:
        color_treat = 'green'

    # Draw the text on the image
    imagename = images[i][:-4]

    namevid, _, frnumber = imagename.rpartition('_')

    draw.text((0.01 * image_overlayed_ann.width, hh + .5 * space_height), namevid + '_' + str(frnumber), fill=(0, 0, 0),
              font=font1)
    draw.text((1 * image_overlayed_ann.width, hh + .5 * space_height - 40), 'Treat Score:' + str(AR_treat),
              fill=(0, 0, 0),
              font=font, color=color_treat)
    draw.text((1.5 * image_overlayed_ann.width, hh + .5 * space_height - 40), 'Check Score:' + str(AR_check),
              fill=(0, 0, 0),
              font=font, color=color_check)
    draw.text((2.4 * image_overlayed_ann.width, 0 + .5 * space_height - 40), 'Ground Truth',
              fill=(0, 0, 0),
              font=font, color=color_check)
    draw.text((1.3 * image_overlayed_ann.width, 0 + .5 * space_height - 40), annotator_examed,
              fill=(0, 0, 0),
              font=font, color=color_check)
    hh = hh + HEIGHT + space_height

cv2.imwrite(data_folder + '/Res/' + annotator_examed + "_session1.jpg", cv2.cvtColor(np.array(im3), cv2.COLOR_BGR2RGB))
print('FINAL SCORE: ', sum(AR_list) / len(AR_list))
