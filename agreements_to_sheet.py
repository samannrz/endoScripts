import argparse

import numpy as np
from trimesh.util import tolist

from functions import write_ndarray_to_gsheet
############# Set the Parameters ##########
juniorsornot = ''
juniorsornot = 'j'
###########################################

parser = argparse.ArgumentParser()
parser.add_argument('--batch', help = 'batch number')
args = parser.parse_args()
batch_num = args.batch

nb_ann = 2
NAME_LIST = ['Nicolas', 'Jean', 'Giuseppe', 'Filippo', 'Ervin', 'Ebbe']
NAME_LIST_juniors = ['Oscar', 'Anne.Sofie', 'Gry']
NAME_LIST_consensus = ['Juniors', 'Seniors']

NAME_LIST = NAME_LIST_consensus



# Treat_rates = np.load('Rates_agreement/Treat_rates'+juniorsornot+str(batch_num)+'.npy')
# Check_rates = np.load('Rates_agreement/Check_rates'+juniorsornot+str(batch_num)+'.npy')

Treat_rates = np.load('Rates_agreement/Treat_rates_juniors_seniors'+str(batch_num)+'.npy')
Check_rates = np.load('Rates_agreement/Check_rates_juniors_seniors'+str(batch_num)+'.npy')
# vidnames = np.load('Rates_agreement/videos'+str(batch_num)+'.npy')

Treat_matrix_flat = np.mean(Treat_rates, axis=0)
Treat_matrix = Treat_matrix_flat.reshape(nb_ann, nb_ann)
Check_matrix_flat = np.mean(Check_rates, axis=0)
Check_matrix = Check_matrix_flat.reshape(nb_ann, nb_ann)

ann_list = NAME_LIST

sfpath = 'keycode/my-gpysheets-3d8d13442005.json'
sheetID = '1HiWuZGv5_Y_BjxnV2gIgDN2VA7WVawuvUd545Wr5FlY'
sheetID = '171H6ZgzfzZVD-Zz8LFpry-3rVC_ORq59-xy2OIBHqyA'
wks_write=write_ndarray_to_gsheet(sfpath, sheetID, str(batch_num)+juniorsornot+'s', Treat_rates)
wks_write.clear('A1', None, '*')

data_list = Treat_matrix.tolist()
wks_write.update_values('A1',[['Treat']+ann_list])
wks_write.update_values('A2', [[c] for c in ann_list])
wks_write.update_values('B2', data_list)

data_list = Check_matrix.tolist()
wks_write.update_values('A10',[['Check']+ann_list])
wks_write.update_values('A11', [[c] for c in ann_list])
wks_write.update_values('B11', data_list)

# data_list=Treat_rates.tolist()
# wks_write.update_values('A20', [[c] for c in vidnames])
# wks_write.update_values('B20', data_list)

wks_write.frozen_rows = 1
wks_write.frozen_columns = 1

