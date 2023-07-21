import os
import shutil

list_consensus_8 = os.listdir('/data/DATA/DELPHI_incision/consensus8')
list_consensus_9 = os.listdir('/data/DATA/DELPHI_incision/consensus9')

list8 = [im[:-6] + im[-4:] for im in list_consensus_8]
list9 = [im[:-6] + im[-4:] for im in list_consensus_9]

list8_9 = list(set(list8)) + list(set(list9))

for im in os.listdir('/data/projects/IncisionDeepLab/input/incision/orig_data_all/valid_images'):
    if im in list8_9:
        os.remove('/data/projects/IncisionDeepLab/input/incision/orig_data_all/valid_images/'+im)
        os.remove('/data/projects/IncisionDeepLab/input/incision/orig_data_all/valid_masks/' + im)
        print(im, ' removed')

# inference_path = '/data/projects/IncisionDeepLab/input/inference_data'
# for im in list8_9:
#     try:
#         shutil.copy('/data/DATA/incision/4/image/' + im, os.path.join(inference_path, 'images'))
#         shutil.copy('/data/DATA/incision/4/mask/Treat/' + im, os.path.join(inference_path, 'masks', 'Treat'))
#         shutil.copy('/data/DATA/incision/4/mask/Check/' + im, os.path.join(inference_path, 'masks', 'Check'))
#     except:
#         print('exception')
#
