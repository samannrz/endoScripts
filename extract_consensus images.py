from functions import *
from PIL import Image, ImageDraw


api, tm = get_supervisely_team()
ws = api.workspace.get_info_by_name(tm.id, 'Data annotation')

ANNOTATORs = ['incision.consensus', 'nicolas.bourdel', 'Jean-Luc.Pouly', 'giuseppe.giacomello', 'filippo.ferrari']

ANNOTATOR = ANNOTATORs[0]

save_path = '/data/DATA/DELPHI_incision'
if not os.path.exists(save_path):
    os.mkdir(save_path)

for project in api.project.get_list(ws.id):  # for each project
    for ds in api.dataset.get_list(project.id):
        for vd in api.video.get_list(ds.id):
            video_api = api.video.get_info_by_name(ds.id, vd.name)
            annotation = api.video.annotation.download(video_api.id)
            image_treat_c = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                      (0, 0, 0))
            image_check_c = Image.new('RGB', (annotation['size']['width'], annotation['size']['height']),
                                      (0, 0, 0))
            draw_treat_c = ImageDraw.Draw(image_treat_c)
            draw_check_c = ImageDraw.Draw(image_check_c)

            frames = annotation['frames']
            for fr in frames:
                figures = fr['figures']
                for fig in figures:
                    # find the class of the polygon
                    annotator = fig['labelerLogin']
                    if annotator != 'incision.consensus':
                        continue
                    if annotator != ANNOTATOR:
                        continue

                    frcoor = fig['geometry']['points']['exterior']
                    polygon = [tuple(coor) for coor in frcoor]
                    classobj = findClass(fig['objectId'], annotation['objects'])
                    treat_exists = False
                    check_exists = False
                    if classobj == 'To Treat':
                        # Draw the polygon on the image
                        draw_treat_c.polygon(polygon, fill=(255, 255, 255))
                        # Convert the image to a mask
                        mask_treat_c = image_treat_c.convert("L")
                        treat_exists = True
                    elif classobj == 'To Check':
                        draw_check_c.polygon(polygon, fill=(255, 255, 255))
                        mask_check_c = image_treat_c.convert("L")
                        check_exists = True
                    if treat_exists:
                        mask_treat_c.save(
                        os.path.join(save_path, vd.name + '_' + str(fr['index']).zfill(5) + '_' + ANNOTATOR[
                            0] + '_' + 'treat.png'),
                        'PNG')
                    if check_exists:
                        mask_check_c.save(
                        os.path.join(save_path, vd.name + '_' + str(fr['index']).zfill(5) + '_' + ANNOTATOR[
                            0] + '_' + 'check.png'),
                        'PNG')


