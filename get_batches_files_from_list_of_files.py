import os
import shutil

list_consensus_8 = os.listdir('/data/DATA/DELPHI_incision/consensus8')
list_consensus_9 = os.listdir('/data/DATA/DELPHI_incision/consensus9')

list8 = [im[:-6] + im[-4:] for im in list_consensus_8]
list9 = [im[:-6] + im[-4:] for im in list_consensus_9]

list8_9 = list(set(list8)) + list(set(list9))

ann_folder = '/data/DATA/incision/2/image'
dest_folder = '/data/DATA/Annotators/G/Batch8-9/image'

for filename in list8_9:
    source_path = os.path.join(ann_folder, filename)
    dest_path = os.path.join(dest_folder, filename)

    if os.path.exists(source_path):
        shutil.copy(source_path, dest_path)
        print(f"Copying {filename} to {dest_path}")
    else:
        print(f"{filename} does not exist in {ann_folder}")