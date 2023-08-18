import numpy as np
from scipy import stats
import pandas as pd

#### Filippo and Nicolas ####
# Treat

b3 = pd.read_pickle("batch3.pkl")
b4 = pd.read_pickle("batch4.pkl")
b5 = pd.read_pickle("batch5.pkl")
b6 = pd.read_pickle("batch6.pkl")
b7 = pd.read_pickle("batch7.pkl")
b8 = pd.read_pickle("batch8.pkl")
b9 = pd.read_pickle("batch9.pkl")
b10 = pd.read_pickle("batch10.pkl")
b11 = pd.read_pickle("batch11.pkl")

n_treat_3 = np.array(b3['NB Treat'])[:-1]
n_treat_4 = np.array(b4['NB Treat'])[:-1]
n_treat_5 = np.array(b5['NB Treat'])[:-1]
n_treat_6 = np.array(b6['NB Treat'])[:-1]
n_treat_7 = np.array(b7['NB Treat'])[:-1]
n_treat_8 = np.array(b8['NB Treat'])[:-1]
n_treat_9 = np.array(b9['NB Treat'])[:-1]
n_treat_10 = np.array(b10['NB Treat'])[:-1]
n_treat_11 = np.array(b11['NB Treat'])[:-1]

t_stat, p_val = stats.ttest_ind(np.concatenate((n_treat_3, n_treat_4)),
                                np.concatenate((n_treat_5, n_treat_6)))
# t_stat, p_val = stats.ttest_ind(fn_treat_91011, fn_treat_345)
print('Treat')
print("p-value = " + str(p_val))
t_stat, p_val = stats.ttest_ind(np.concatenate((n_check_3, n_check_4)),
                                np.concatenate((n_check_5, n_check_6)))
print('Check')
print("p-value = " + str(p_val))

t_stat, p_val = stats.ttest_ind(np.concatenate((fn_merge_3, fn_merge_4)),
                                np.concatenate((fn_merge_5, fn_merge_6)))
# t_stat, p_val = stats.ttest_ind(fn_merge_678, fn_merge_345)
print('merge')
print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
