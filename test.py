import os
import shutil

dest_folder = '/data/DATA/DELPHI_incision/image/'

for f in os.listdir(dest_folder):

    shutil.move(dest_folder+f ,dest_folder[:-6]+'consensus/'+f[:-4]+'_'+'0'+'.png')
