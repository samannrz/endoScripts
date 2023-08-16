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

fn_treat_3 = np.array(b3['GG-NB Treat'])[:-1]
fn_treat_4 = np.array(b4['GG-NB Treat'])[:-1]
fn_treat_5 = np.array(b5['GG-NB Treat'])[:-1]

fn_treat_6 = np.array(b6['GG-NB Treat'])[:-1]
fn_treat_7 = np.array(b7['GG-NB Treat'])[:-1]
fn_treat_8 = np.array(b8['GG-NB Treat'])[:-1]

fn_treat_9 = np.array(b9['GG-NB Treat'])[:-1]
fn_treat_10 = np.array(b10['GG-NB Treat'])[:-1]
fn_treat_11 = np.array(b11['GG-NB Treat'])[:-1]

fn_treat_345 = np.concatenate((fn_treat_3, fn_treat_4, fn_treat_5))
fn_treat_678 = np.concatenate((fn_treat_6, fn_treat_7, fn_treat_8))
fn_treat_91011 = np.concatenate((fn_treat_9, fn_treat_10, fn_treat_11))
t_stat, p_val = stats.ttest_ind(np.concatenate((fn_treat_3, fn_treat_4)),
                                np.concatenate((fn_treat_5, fn_treat_6)))
# t_stat, p_val = stats.ttest_ind(fn_treat_91011, fn_treat_345)
print('Treat')
print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
#####################
# Treat

fn_check_3 = np.array(b3['GG-NB Check'])[:-1]
fn_check_4 = np.array(b4['GG-NB Check'])[:-1]
fn_check_5 = np.array(b5['GG-NB Check'])[:-1]

fn_check_6 = np.array(b6['GG-NB Check'])[:-1]
fn_check_7 = np.array(b7['GG-NB Check'])[:-1]
fn_check_8 = np.array(b8['GG-NB Check'])[:-1]

fn_check_9 = np.array(b9['GG-NB Check'])[:-1]
fn_check_10 = np.array(b10['GG-NB Check'])[:-1]
fn_check_11 = np.array(b11['GG-NB Check'])[:-1]

fn_check_345 = np.concatenate((fn_check_3, fn_check_4, fn_check_5))
fn_check_678 = np.concatenate((fn_check_6, fn_check_7, fn_check_8))
fn_check_91011 = np.concatenate((fn_check_9, fn_check_10, fn_check_11))


t_stat, p_val = stats.ttest_ind(np.concatenate((fn_check_3, fn_check_4)),
                                np.concatenate((fn_check_5, fn_check_6)))
# t_stat, p_val = stats.ttest_ind(fn_check_91011, fn_check_345)

print('Check')

print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
#########
fn_merge_3 = np.array(b3['GG-NB Merge'])[:-1]
fn_merge_4 = np.array(b4['GG-NB Merge'])[:-1]
fn_merge_5 = np.array(b5['GG-NB Merge'])[:-1]

fn_merge_6 = np.array(b6['GG-NB Merge'])[:-1]
fn_merge_7 = np.array(b7['GG-NB Merge'])[:-1]
fn_merge_8 = np.array(b8['GG-NB Merge'])[:-1]

fn_merge_9 = np.array(b9['GG-NB Merge'])[:-1]
fn_merge_10 = np.array(b10['GG-NB Merge'])[:-1]
fn_merge_11 = np.array(b11['GG-NB Merge'])[:-1]

fn_merge_345 = np.concatenate((fn_merge_3, fn_merge_4, fn_merge_5))
fn_merge_678 = np.concatenate((fn_merge_6, fn_merge_7, fn_merge_8))
fn_merge_91011 = np.concatenate((fn_merge_9, fn_merge_10, fn_merge_11))

t_stat, p_val = stats.ttest_ind(np.concatenate((fn_merge_3, fn_merge_4)),
                                np.concatenate((fn_merge_5, fn_merge_6)))

# t_stat, p_val = stats.ttest_ind(fn_merge_91011, fn_merge_345)
print('merge')
print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
