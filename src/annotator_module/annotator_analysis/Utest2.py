import numpy as np
from set_batches import *


for batch_num in [21,22,23,24,25]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    Check_rates = np.load('Rates_agreement/Check_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_12345 = N_J_treat_12345 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_12345 = N_G_treat_12345 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_12345 = N_F_treat_12345 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_12345 = N_E_treat_12345 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_12345 = N_B_treat_12345 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_12345 = J_G_treat_12345 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_12345 = J_F_treat_12345 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_12345 = J_E_treat_12345 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_12345 = J_B_treat_12345 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_12345 = G_F_treat_12345 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_12345 = G_E_treat_12345 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_12345 = G_B_treat_12345 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_12345 = F_E_treat_12345 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_12345 = F_B_treat_12345 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_12345 = E_B_treat_12345 + [Treat_rates[i][29] for i in range(n_images)]

for batch_num in [27,28,29,210]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_78910 = N_J_treat_78910 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_78910 = N_G_treat_78910 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_78910 = N_F_treat_78910 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_78910 = N_E_treat_78910 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_78910 = N_B_treat_78910 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_78910 = J_G_treat_78910 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_78910 = J_F_treat_78910 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_78910 = J_E_treat_78910 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_78910 = J_B_treat_78910 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_78910 = G_F_treat_78910 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_78910 = G_E_treat_78910 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_78910 = G_B_treat_78910 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_78910 = F_E_treat_78910 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_78910 = F_B_treat_78910 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_78910 = E_B_treat_78910 + [Treat_rates[i][29] for i in range(n_images)]

for batch_num in [25,27]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_57 = N_J_treat_57 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_57 = N_G_treat_57 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_57 = N_F_treat_57 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_57 = N_E_treat_57 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_57 = N_B_treat_57 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_57 = J_G_treat_57 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_57 = J_F_treat_57 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_57 = J_E_treat_57 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_57 = J_B_treat_57 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_57 = G_F_treat_57 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_57 = G_E_treat_57 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_57 = G_B_treat_57 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_57 = F_E_treat_57 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_57 = F_B_treat_57 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_57 = E_B_treat_57 + [Treat_rates[i][29] for i in range(n_images)]
for batch_num in [210,29]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_89 = N_J_treat_89 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_89 = N_G_treat_89 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_89 = N_F_treat_89 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_89 = N_E_treat_89 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_89 = N_B_treat_89 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_89 = J_G_treat_89 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_89 = J_F_treat_89 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_89 = J_E_treat_89 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_89 = J_B_treat_89 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_89 = G_F_treat_89 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_89 = G_E_treat_89 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_89 = G_B_treat_89 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_89 = F_E_treat_89 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_89 = F_B_treat_89 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_89 = E_B_treat_89 + [Treat_rates[i][29] for i in range(n_images)]
##########################
##########################
for batch_num in [21, 22]:
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    n_images = len(Check_rates)
    #    print(n_images)
    N_J_check_12345 = N_J_check_12345 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_12345 = N_G_check_12345 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_12345 = N_F_check_12345 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_12345 = N_E_check_12345 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_12345 = N_B_check_12345 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_12345 = J_G_check_12345 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_12345 = J_F_check_12345 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_12345 = J_E_check_12345 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_12345 = J_B_check_12345 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_12345 = G_F_check_12345 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_12345 = G_E_check_12345 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_12345 = G_B_check_12345 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_12345 = F_E_check_12345 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_12345 = F_B_check_12345 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_12345 = E_B_check_12345 + [Check_rates[i][29] for i in range(n_images)]

for batch_num in [23,24]:
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    n_images = len(Check_rates)
    #    print(n_images)
    N_J_check_78910 = N_J_check_78910 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_78910 = N_G_check_78910 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_78910 = N_F_check_78910 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_78910 = N_E_check_78910 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_78910 = N_B_check_78910 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_78910 = J_G_check_78910 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_78910 = J_F_check_78910 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_78910 = J_E_check_78910 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_78910 = J_B_check_78910 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_78910 = G_F_check_78910 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_78910 = G_E_check_78910 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_78910 = G_B_check_78910 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_78910 = F_E_check_78910 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_78910 = F_B_check_78910 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_78910 = E_B_check_78910 + [Check_rates[i][29] for i in range(n_images)]

for batch_num in [25, 27]:
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    n_images = len(Check_rates)
    #    print(n_images)
    N_J_check_57 = N_J_check_57 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_57 = N_G_check_57 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_57 = N_F_check_57 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_57 = N_E_check_57 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_57 = N_B_check_57 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_57 = J_G_check_57 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_57 = J_F_check_57 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_57 = J_E_check_57 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_57 = J_B_check_57 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_57 = G_F_check_57 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_57 = G_E_check_57 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_57 = G_B_check_57 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_57 = F_E_check_57 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_57 = F_B_check_57 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_57 = E_B_check_57 + [Check_rates[i][29] for i in range(n_images)]

for batch_num in [210,29]:
    Check_rates = np.load('Rates_agreement/Check_rates'+str(batch_num)+'.npy')
    n_images = len (Check_rates)
#    print(n_images)
    N_J_check_89 = N_J_check_89 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_89 = N_G_check_89 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_89 = N_F_check_89 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_89 = N_E_check_89 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_89 = N_B_check_89 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_89 = J_G_check_89 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_89 = J_F_check_89 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_89 = J_E_check_89 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_89 = J_B_check_89 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_89 = G_F_check_89 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_89 = G_E_check_89 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_89 = G_B_check_89 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_89 = F_E_check_89 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_89 = F_B_check_89 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_89 = E_B_check_89 + [Check_rates[i][29] for i in range(n_images)]
##################
#################
for batch_num in [21, 22]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    #    print(n_images)
    N_J_merge_12345 = N_J_merge_12345 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_12345 = N_G_merge_12345 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_12345 = N_F_merge_12345 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_12345 = N_E_merge_12345 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_12345 = N_B_merge_12345 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_12345 = J_G_merge_12345 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_12345 = J_F_merge_12345 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_12345 = J_E_merge_12345 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_12345 = J_B_merge_12345 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_12345 = G_F_merge_12345 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_12345 = G_E_merge_12345 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_12345 = G_B_merge_12345 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_12345 = F_E_merge_12345 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_12345 = F_B_merge_12345 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_12345 = E_B_merge_12345 + [Merge_rates[i][29] for i in range(n_images)]

for batch_num in [23,24]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    #    print(n_images)
    N_J_merge_78910 = N_J_merge_78910 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_78910 = N_G_merge_78910 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_78910 = N_F_merge_78910 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_78910 = N_E_merge_78910 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_78910 = N_B_merge_78910 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_78910 = J_G_merge_78910 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_78910 = J_F_merge_78910 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_78910 = J_E_merge_78910 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_78910 = J_B_merge_78910 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_78910 = G_F_merge_78910 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_78910 = G_E_merge_78910 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_78910 = G_B_merge_78910 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_78910 = F_E_merge_78910 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_78910 = F_B_merge_78910 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_78910 = E_B_merge_78910 + [Merge_rates[i][29] for i in range(n_images)]

for batch_num in [25,27]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    N_J_merge_57 = N_J_merge_57 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_57 = N_G_merge_57 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_57 = N_F_merge_57 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_57 = N_E_merge_57 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_57 = N_B_merge_57 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_57 = J_G_merge_57 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_57 = J_F_merge_57 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_57 = J_E_merge_57 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_57 = J_B_merge_57 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_57 = G_F_merge_57 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_57 = G_E_merge_57 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_57 = G_B_merge_57 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_57 = F_E_merge_57 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_57 = F_B_merge_57 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_57 = E_B_merge_57 + [Merge_rates[i][29] for i in range(n_images)]
for batch_num in [210,29]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    #    print(n_images)
    N_J_merge_89 = N_J_merge_89 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_89 = N_G_merge_89 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_89 = N_F_merge_89 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_89 = N_E_merge_89 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_89 = N_B_merge_89 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_89 = J_G_merge_89 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_89 = J_F_merge_89 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_89 = J_E_merge_89 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_89 = J_B_merge_89 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_89 = G_F_merge_89 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_89 = G_E_merge_89 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_89 = G_B_merge_89 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_89 = F_E_merge_89 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_89 = F_B_merge_89 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_89 = E_B_merge_89 + [Merge_rates[i][29] for i in range(n_images)]
##################
##################
from scipy.stats import mannwhitneyu, wilcoxon


def remove_0_100(my_list):
    filtered_list = [x for x in my_list if x != 0 or x!=100]
    return filtered_list


# Mann-Whitney U test
# We specify alternative='less' to test if the second  > first
statistic, p_value = mannwhitneyu(remove_0_100(J_B_treat_12345), remove_0_100(J_B_treat_78910), alternative= 'less' )
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_0_100(J_B_check_12345), remove_0_100(J_B_check_78910), alternative='less')
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_0_100(J_B_merge_12345), remove_0_100(J_B_merge_78910), alternative='less')
print(f"P-value: {p_value}")


from scipy.stats import brunnermunzel
statistic, p_value = brunnermunzel(remove_0_100(J_B_treat_12345), remove_0_100(J_B_treat_78910))
print(p_value)
statistic, p_value = brunnermunzel(remove_0_100(J_B_check_12345), remove_0_100(J_B_check_78910))
print(p_value)
statistic, p_value = brunnermunzel(remove_0_100(J_B_merge_12345), remove_0_100(J_B_merge_78910))
print(p_value)

