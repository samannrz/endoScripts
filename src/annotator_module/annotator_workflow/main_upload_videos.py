# This script is to upload all videos in a specific folder (vidpath) from a local path to a dataset in supervisely


import os
import supervisely_lib as sly
from dotenv import load_dotenv
from supervisely.task import progress

# Set the parameters first
# IMPORTANT : Write the project_id
project_id  = 1416 #which project you are working? #(996 for smoke)
dataset =  'Sao Paulo' #the name of the dataset. It can exist or nor (like 'Saman' for smoke)
vidpath = '/data/Videos/endodata/sequ/' #the path of your videos

##########################
# Saman's token on surgai-surgery.com
if sly.is_development():
    load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api.from_env()

##########################

ds_info = api.dataset.get_list(project_id)

# check if the dataset exists, put the videos inside
for i in range(len(ds_info)):
    if dataset == ds_info[i].name:
        ds_id = ds_info[i].id
# if dataset does not exist, create one
try:
    ds_id
except NameError:
    new_ds = api.dataset.create(project_id, dataset)
    ds_id = new_ds.id

video_names = os.listdir(vidpath)
video_paths = [vidpath + s for s in video_names]
print('Video Paths:')
print(video_paths)
video_infos = api.video.upload_paths(ds_id, names=video_names, paths=video_paths)
