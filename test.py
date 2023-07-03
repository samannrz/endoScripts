import os
import shutil

import pandas as pd

from functions import write_to_gsheet

dest_folder = '/data/DATA/DELPHI_incision/all_consensus/'

file_list = [f[:-6] for f in os.listdir(dest_folder)]
print(len(file_list))
file_list = set(file_list)
print(len(file_list))
print(file_list)

data_df = pd.DataFrame(
    {'Image Name': list(file_list)})
sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1wOejlwXos2UCTMLDJxkCC8T71zVubFwh4GoxyUOzhqg'
sheetName = 'list'
write_to_gsheet(sfpath, sheetID, sheetName, data_df)



