# This is the same thing as main_endo_video_lesions
import supervisely as sly
import pandas as pd
from dotenv import load_dotenv

# import os
from functions import write_to_gsheet
# import openpyxl
import datetime


def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]


def findClass(key, objects):
    for obj in objects:
        if key == obj['id']:
            return obj['classTitle']

import os
import cv2
import numpy as np



def getvidlist(teamName, workspaceName):
    # start using supervisely API
    if sly.is_development():
        load_dotenv(os.path.expanduser("~/supervisely.env"))
    api = sly.Api.from_env()
    # getting team, workspace and projects
    tm = api.team.get_info_by_name(teamName)
    ws = api.workspace.get_info_by_name(tm.id, workspaceName)
    prs = api.project.get_list(ws.id)

    nameList = []
    projects = []
    datasets = []
    annsList = []
    CheckList = []
    TreatList = []
    consensusList = []
    GiuList = []
    FilList = []
    NicList = []
    JeaList = []
    ErvList = []
    EbbList = []
    annNumList = []
    byOneList = []
    byTwoList = []
    byThreeList = []
    byFourList = []

    # get a list of workspace video names with their corresponding project and dataset name
    for pr in prs:
        print('Processing project: %s' % pr.name)
        print(pr.type)
        if pr.type=='images':
            continue
        dss = api.dataset.get_list(pr.id)
        for ds in dss:
            vds = api.video.get_list(ds.id)
            Tnum = 0
            Cnum = 0
            Fnum = 0
            consNum = 0
            GiuNum = 0
            FilNum = 0
            NicNum = 0
            JeaNum = 0
            ErvNum = 0
            EbbNum = 0
            byOne = 0
            byTwo = 0
            byThree = 0
            byFour = 0
            for vd in vds:
                ans = api.video.annotation.download(vd.id)
                frames = ans['frames']
                for fr in frames:
                    FrameCounted = False
                    FrameCounted_Fil = False
                    FrameCounted_Giu = False
                    FrameCounted_Nic = False
                    FrameCounted_Jean = False
                    FrameCounted_inc = False
                    FrameCounted_Ervin = False
                    FrameCounted_Ebbe = False


                    figs = fr['figures']
                    for fig in figs:
                        if fig['geometryType'] == 'rectangle':
                            continue  # go to next object in the frame if it is not a rectangle
                        classobj = findClass(fig['objectId'], ans['objects'])
                        if classobj != 'To Treat' and classobj != 'To Check':
                            continue
                        if classobj == 'To Treat':
                            Tnum += 1
                        if classobj == 'To Check':
                            Cnum += 1
                        if (Tnum > 0 or Cnum > 0) and FrameCounted == False:
                            Fnum += 1
                            FrameCounted = True
                        if fig['labelerLogin'] == 'incision.consensus' and FrameCounted_inc == False:
                            consNum += 1
                            FrameCounted_inc = True
                        if fig['labelerLogin'] == 'giuseppe.giacomello' and FrameCounted_Giu == False:
                            GiuNum += 1
                            FrameCounted_Giu = True
                        if fig['labelerLogin'] == 'filippo.ferrari' and FrameCounted_Fil == False:
                            FilNum += 1
                            FrameCounted_Fil = True
                        if fig['labelerLogin'] == 'nicolas.bourdel' and FrameCounted_Nic == False:
                            NicNum += 1
                            FrameCounted_Nic = True
                        if fig['labelerLogin'] == 'Jean-Luc.Pouly' and FrameCounted_Jean == False:
                            JeaNum += 1
                            FrameCounted_Jean = True
                        if fig['labelerLogin'] == 'Ervin.Kallfa' and FrameCounted_Ervin == False:
                            ErvNum += 1
                            FrameCounted_Ervin = True
                        if fig['labelerLogin'] == 'ebbe.thinggaard' and FrameCounted_Ebbe == False:
                            EbbNum += 1
                            FrameCounted_Ebbe = True
                        if pr.name == 'Endometriosis_WS5' and ds.name=='Sao Paulo':
                            if FrameCounted_Giu ^ FrameCounted_Fil == False:
                                print(vd.name)
                                print(fr['index'])


                    annNum = sum([FrameCounted_Jean, FrameCounted_Nic, FrameCounted_Fil, FrameCounted_Giu, FrameCounted_Ervin,FrameCounted_Ebbe])

                    if annNum == 1:
                        byOne += 1
                    if annNum == 2:
                        byTwo += 1
                    if annNum == 3:
                        byThree += 1
                    if annNum == 4:
                        byFour += 1

            projects.append(pr.name)
            datasets.append(ds.name)
            annsList.append(Fnum)
            TreatList.append(Tnum)
            CheckList.append(Cnum)
            consensusList.append(consNum)
            GiuList.append(GiuNum)
            FilList.append(FilNum)
            JeaList.append(JeaNum)
            NicList.append(NicNum)
            ErvList.append(ErvNum)
            EbbList.append(EbbNum)
            byOneList.append(byOne)
            byTwoList.append(byTwo)
            byThreeList.append(byThree)
            byFourList.append(byFour)

    return projects, datasets, annsList, TreatList, CheckList, consensusList, GiuList, FilList, NicList, JeaList, ErvList, EbbList, byOneList, byTwoList, byThreeList, byFourList


def main():
    teamName = 'Endometriosis'
    workspaceName = 'Data annotation'

    prList, dsList, annsList, TreatList, CheckList, consensusList, GiuList, FilList, NicList, JeaList, ErvList, EbbList, byOneList, byTwoList, byThreeList, byFourList = getvidlist(
        teamName, workspaceName)

    data_df = pd.DataFrame(
        {'Project': prList, 'Dataset': dsList, 'annotated Imgs': annsList, 'Treat': TreatList, 'Check': CheckList,
         'Giuseppe Imgs': GiuList, 'Filippo Imgs': FilList, 'Jean-Luc Imgs': JeaList, 'Nicolas Imgs': NicList,
         'Ervin Imgs': ErvList,'Ebbe Imgs': EbbList,
         'Consensus': consensusList, '1 Ann': byOneList, '2 Ann': byTwoList, '3 Ann': byThreeList, '4 Ann': byFourList})
    sfpath = '../../../data/keycode/my-gpysheets-3d8d13442005.json'
    sheetID = '1NJRSg0Y1YIj7E217yw-_X7lof7KOlxtTugF4NeVXPA8'
    sheetName = str(datetime.date.today())
    write_to_gsheet(sfpath, sheetID, sheetName, data_df)


if __name__ == '__main__':
    main()
