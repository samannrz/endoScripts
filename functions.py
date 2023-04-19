import os
import pygsheets


def createDIR(folder, name_dir):
    # create new directory for images
    path = folder + name_dir
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The " + name_dir + " directory is created!")
        return name_dir


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


def extractFrame(video, frame_number):
    vidcap = cv2.VideoCapture(video)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number - 1)
    res, frame = vidcap.read()
    return frame


def findClass(key, objects):
    for obj in objects:
        if key == obj['id']:
            return obj['classTitle']


import supervisely_lib as sly


def get_supervisely_team(
        mytoken='Gp3sg4GihFSwbQpF51H80T5fgH7Emp0cxIVFwo8zoxdgc7IFj3Mxufwv296TLzP352mF61I4P2DYuZx9mz5I3S2tZs5MFLIS91GWT8ym6mrCMPpFZ3LDKbgbTxmS9l6t'
        , teamName='Endometriosis'):
    api = sly.Api(server_address="https://surgai-surgery.com", token=mytoken)
    tm = api.team.get_info_by_name(teamName)
    return api, tm


def get_frames_from_api(api, video_id, video_name, frames_to_convert):
    image_names = []
    image_names = [
        f"{video_name}_{str(frame_index).zfill(5)}.png"
        for frame_index in frames_to_convert
    ]
    images = api.video.frame.download_nps(
        video_id=video_id, frame_indexes=frames_to_convert
    )
    return image_names, images


def write_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_df):
    """
    this function takes data_df and writes it under spreadsheet_id
    and sheet_name using your credentials under service_file_path
    """
    gc = pygsheets.authorize(service_file=service_file_path)
    sh = gc.open_by_key(spreadsheet_id)
    try:
        sh.add_worksheet(sheet_name)
    except:
        pass
    wks_write = sh.worksheet_by_title(sheet_name)
    wks_write.clear('A1', None, '*')
    wks_write.set_dataframe(data_df, (1, 1), encoding='utf-8', fit=True, copy_index=True)
    wks_write.frozen_rows = 1
