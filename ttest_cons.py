import numpy as np
from scipy import stats
import pandas as pd

# Treat

b3 = pd.read_pickle("pkl_files/c_batch3.pkl")
b4 = pd.read_pickle("pkl_files/c_batch4.pkl")
b5 = pd.read_pickle("pkl_files/c_batch5.pkl")
b6 = pd.read_pickle("pkl_files/c_batch6.pkl")
b7 = pd.read_pickle("pkl_files/c_batch7.pkl")
b8 = pd.read_pickle("pkl_files/c_batch8.pkl")
b9 = pd.read_pickle("pkl_files/c_batch9.pkl")
b10 = pd.read_pickle("pkl_files/c_batch10.pkl")
b11 = pd.read_pickle("pkl_files/c_batch11.pkl")

n_3 = np.array(b3.iloc[:, 2:5])[:-1]
n_4 = np.array(b4.iloc[:, 2:5])[:-1]
n_5 = np.array(b5.iloc[:, 2:5])[:-1]
n_6 = np.array(b6.iloc[:, 2:5])[:-1]
n_7 = np.array(b7.iloc[:, 2:5])[:-1]
n_8 = np.array(b8.iloc[:, 2:5])[:-1]
n_9 = np.array(b9.iloc[:, 2:5])[:-1]
n_10 = np.array(b10.iloc[:, 2:5])[:-1]
n_11 = np.array(b11.iloc[:, 2:5])[:-1]
t_stat, p_val = stats.ttest_ind(np.concatenate((n_3[:,0], n_4[:,0])),
                                np.concatenate((n_9[:,0], n_10[:,0])))
# t_stat, p_val = stats.ttest_ind(fn_treat_91011, fn_treat_345)
print('Treat')
print("p-value = " + str(p_val))
t_stat, p_val = stats.ttest_ind(np.concatenate((n_3[:,1], n_4[:,1])),
                                np.concatenate((n_9[:,1], n_10[:,1])))
print('Check')
print("p-value = " + str(p_val))

t_stat, p_val = stats.ttest_ind(np.concatenate((n_3[:,2], n_4[:,2])),
                                np.concatenate((n_9[:,2], n_10[:,2])))
# t_stat, p_val = stats.ttest_ind(fn_merge_678, fn_merge_345)
print('merge')
# print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
###################
########JEAN LUC###########
##################
print('\n Jean')
b3 = pd.read_pickle("pkl_files/c_batch3.pkl")
b4 = pd.read_pickle("pkl_files/c_batch4.pkl")
b5 = pd.read_pickle("pkl_files/c_batch5.pkl")
b6 = pd.read_pickle("pkl_files/c_batch6.pkl")
b7 = pd.read_pickle("pkl_files/c_batch7.pkl")
b8 = pd.read_pickle("pkl_files/c_batch8.pkl")
b9 = pd.read_pickle("pkl_files/c_batch9.pkl")
b10 = pd.read_pickle("pkl_files/c_batch10.pkl")
b11 = pd.read_pickle("pkl_files/c_batch11.pkl")

j_3 = np.array(b3.iloc[:, 11:14])[:-1]
j_4 = np.array(b4.iloc[:, 11:14])[:-1]
j_5 = np.array(b5.iloc[:, 11:14])[:-1]
j_6 = np.array(b6.iloc[:, 11:14])[:-1]
j_7 = np.array(b7.iloc[:, 11:14])[:-1]
j_8 = np.array(b8.iloc[:, 11:14])[:-1]
j_9 = np.array(b9.iloc[:, 11:14])[:-1]
j_10 = np.array(b10.iloc[:, 11:14])[:-1]
j_11 = np.array(b11.iloc[:, 11:14])[:-1]
t_stat, p_val = stats.ttest_ind(np.concatenate((j_3[:,0], j_4[:,0])),
                                np.concatenate((j_10[:,0], j_9[:,0])))
print('Treat')
print("p-value = " + str(p_val))
t_stat, p_val = stats.ttest_ind(np.concatenate((j_3[:,1], j_4[:,1])),
                                np.concatenate((j_9[:,1],j_10[:,1])))
print('Check')
print("p-value = " + str(p_val))

t_stat, p_val = stats.ttest_ind(np.concatenate((j_3[:,2], j_4[:,2])),
                                np.concatenate((j_9[:,2],j_10[:,2])))
print('merge')
# print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
###################
########Giuseppe###########
##################
print('\n Giuseppe')
b3 = pd.read_pickle("pkl_files/c_batch3.pkl")
b4 = pd.read_pickle("pkl_files/c_batch4.pkl")
b5 = pd.read_pickle("pkl_files/c_batch5.pkl")
b6 = pd.read_pickle("pkl_files/c_batch6.pkl")
b7 = pd.read_pickle("pkl_files/c_batch7.pkl")
b8 = pd.read_pickle("pkl_files/c_batch8.pkl")
b9 = pd.read_pickle("pkl_files/c_batch9.pkl")
b10 = pd.read_pickle("pkl_files/c_batch10.pkl")
b11 = pd.read_pickle("pkl_files/c_batch11.pkl")

G_3 = np.array(b3.iloc[:, 5:8])[:-1]
G_4 = np.array(b4.iloc[:, 5:8])[:-1]
G_5 = np.array(b5.iloc[:, 5:8])[:-1]
G_6 = np.array(b6.iloc[:, 5:8])[:-1]
G_7 = np.array(b7.iloc[:, 5:8])[:-1]
G_8 = np.array(b8.iloc[:, 5:8])[:-1]
G_9 = np.array(b9.iloc[:, 5:8])[:-1]
G_10 = np.array(b10.iloc[:, 5:8])[:-1]
G_11 = np.array(b11.iloc[:, 5:8])[:-1]
t_stat, p_val = stats.ttest_ind(np.concatenate((G_3[:,0], G_4[:,0])),
                                np.concatenate((G_10[:,0], G_9[:,0])))
print('Treat')
print("p-value = " + str(p_val))
t_stat, p_val = stats.ttest_ind(np.concatenate((G_3[:,1], G_4[:,1])),
                                np.concatenate((G_9[:,1],G_10[:,1])))
print('Check')
print("p-value = " + str(p_val))

t_stat, p_val = stats.ttest_ind(np.concatenate((G_3[:,2], G_4[:,2])),
                                np.concatenate((G_9[:,1],G_10[:,2])))
print('merge')
# print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))
###################
########Filippo###########
##################
print('\n Filippo')
b3 = pd.read_pickle("pkl_files/c_batch3.pkl")
b4 = pd.read_pickle("pkl_files/c_batch4.pkl")
b5 = pd.read_pickle("pkl_files/c_batch5.pkl")
b6 = pd.read_pickle("pkl_files/c_batch6.pkl")
b7 = pd.read_pickle("pkl_files/c_batch7.pkl")
b8 = pd.read_pickle("pkl_files/c_batch8.pkl")
b9 = pd.read_pickle("pkl_files/c_batch9.pkl")
b10 = pd.read_pickle("pkl_files/c_batch10.pkl")
b11 = pd.read_pickle("pkl_files/c_batch11.pkl")

F_3 = np.array(b3.iloc[:, 8:11])[:-1]
F_4 = np.array(b4.iloc[:, 8:11])[:-1]
F_5 = np.array(b5.iloc[:, 8:11])[:-1]
F_6 = np.array(b6.iloc[:, 8:11])[:-1]
F_7 = np.array(b7.iloc[:, 8:11])[:-1]
F_8 = np.array(b8.iloc[:, 8:11])[:-1]
F_9 = np.array(b9.iloc[:, 8:11])[:-1]
F_10 = np.array(b10.iloc[:, 8:11])[:-1]
F_11 = np.array(b11.iloc[:, 8:11])[:-1]
t_stat, p_val = stats.ttest_ind(np.concatenate((F_3[:,0], F_4[:,0])),
                                np.concatenate((F_9[:,0],F_10[:,0])))
print('Treat')
print("p-value = " + str(p_val))
t_stat, p_val = stats.ttest_ind(np.concatenate((F_3[:,1], F_4[:,1])),
                                np.concatenate((F_9[:,0],F_10[:,1])))
print('Check')
print("p-value = " + str(p_val))

t_stat, p_val = stats.ttest_ind(np.concatenate((F_3[:,2], F_4[:,2])),
                                np.concatenate((F_9[:,2],F_10[:,2])))
print('merge')
# print("t-statistic = " + str(t_stat))
print("p-value = " + str(p_val))