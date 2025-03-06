# this script write to a sheet on drive named 'Tagged info' a list of videos, with their project name, dataset name,
# the number of the dollowing tags and their counts: TAGS: 'To Annotate' & 'Annot. to discuss'
import os

import supervisely as sly
import pandas as pd
from dotenv import load_dotenv

# import os
from functions import write_to_gsheet
# import openpyxl
import datetime

teamName = 'Endometriosis'
workspaceName = 'Data annotation'

# Definition of Parameters
if sly.is_development():
    load_dotenv(os.path.expanduser("~/supervisely.env"))
api = sly.Api.from_env()
tm = api.team.get_info_by_name(teamName)
ws = api.workspace.get_info_by_name(tm.id,workspaceName)
prs = api.project.get_list(ws.id)

nameList = []
projects = []
datasets = []
numTagged = []
Fr2Tag = []
Fr22Tag = []
tagger=[]
counter = 0
# get a list of workspace video names with their corresponding project and dataset name
for pr in prs:
    if pr.name != 'Endometriosis_WS10':
        continue
    dss = api.dataset.get_list(pr.id)
    for ds in dss:
        vds = api.video.get_list(ds.id)

        for vd in vds:
            # nameList.append(vd.name)
            # projects.append(pr.name)
            # datasets.append(ds.name)
            ans = api.video.annotation.download(vd.id)
            tags = ans['tags']

            # count the number of frames with the tag 'To Annotate'
            frtagged = []
            fr2tagged = []
            #print(vd.name)
            nt = 0
            for tg in tags:

                if tg['createdAt'] > '2024-04-27' or tg['updatedAt'] > '2024-04-27':
                    if tg['name'] == 'To Annotate':
                        nt += 1
                        #print(vd.name)
                        frtagged.append(tg['frameRange'][0])
                    if tg['name'] == 'Annot. to discuss':
                        fr2tagged.append(tg['frameRange'][0])
                        nt += 1
                    tagger_name = tg['labelerLogin']

            if  frtagged!=[] or fr2tagged!=[]:
                tagger.append(tagger_name)
                numTagged.append(nt)
                Fr2Tag.append(frtagged)
                Fr22Tag.append(fr2tagged)
                nameList.append(vd.name)
                projects.append(pr.name)
                datasets.append(ds.name)
            counter += 1
            print('video ' + str(counter) + ' done')

data_df = pd.DataFrame(
    {'Video Name': nameList, 'Project': projects, 'dataset': datasets, 'num of tags': numTagged,
     'Frames to Tag': Fr2Tag, 'Frames to discuss': Fr22Tag, 'Who':tagger})

sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1cflPYtcE0J2K92iTiNixPUvAsGM4aeGEhBIhCSojcGQ'
sheetName = teamName + '_' + workspaceName + '_' + str(datetime.date.today())
write_to_gsheet(sfpath, sheetID, sheetName, data_df)
