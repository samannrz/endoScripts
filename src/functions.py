import os
import shutil

import numpy as np
import pygsheets
from PIL import Image

from plotting.overlay_mask import reColor

def createDIR(*args):
    # create new directory for images
    path = ''
    for name_dir in args:
        path = os.path.join(path, name_dir)
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        print("The " + name_dir + " directory is created!")
        return path


def find(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

import cv2
def extractFrame(video, frame_number):
    vidcap = cv2.VideoCapture(video)
    vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    res, frame = vidcap.read()
    return frame


def findClass(key, objects):
    for obj in objects:
        if key == obj['id']:
            return obj['classTitle']


import supervisely_lib as sly

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

def write_ndarray_to_gsheet(service_file_path, spreadsheet_id, sheet_name, data_array):
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
    return wks_write

def overlayMasks_incision(image_orig, mask1, mask2):
    # This function takes the two masks and overlay them to the image_orig
    bg = image_orig.convert('RGB')

    overlay = mask1.convert('RGB')
    overlay = reColor(overlay, color2=(255, 0, 0))

    overlay2 = mask2.convert('RGB')
    overlay2 = reColor(overlay2, color2=(0, 255, 0))


    # Replace (255,255,0) with (255,0,0)
    data1 = np.array(overlay)  # "data" is a height x width x 4 numpy array
    data2 = np.array(overlay2)  # "data" is a height x width x 4 numpy array
    data = data1 + data2
    red, green, blue = data.T  # Temporarily unpack the bands for readability
    two_colored_areas = (red == 255) & (blue == 0) & (green == 255)
    data[two_colored_areas.T] = (255, 0, 0)  # Transpose back neede
    overlay_final = Image.fromarray(data)
    mask_final = overlay_final.convert('L')
    mask_final = mask_final.point(lambda p: 60 if p > 5 else 0)

    bg.paste(overlay_final, None, mask_final)
    return bg

def find_missing_images(folder1, folder2):
    # Get the list of images in folder1 and folder2
    images_folder1 = set(os.listdir(folder1))
    images_folder2 = set(os.listdir(folder2))

    # Find the missing images
    missing_images = images_folder1 - images_folder2

    # Copy missing images from folder1 to folder2
    for image in missing_images:
        source_path = os.path.join(folder1, image)
        destination_path = os.path.join(folder2, image)
        shutil.copy2(source_path, destination_path)
        print(f"Copying {image} from {folder1} to {folder2}")

