import numpy as np
from set_batches import *


for batch_num in [21,22,23]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    Check_rates = np.load('Rates_agreement/Check_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_123 = N_J_treat_123 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_123 = N_G_treat_123 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_123 = N_F_treat_123 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_123 = N_E_treat_123 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_123 = N_B_treat_123 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_123 = J_G_treat_123 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_123 = J_F_treat_123 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_123 = J_E_treat_123 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_123 = J_B_treat_123 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_123 = G_F_treat_123 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_123 = G_E_treat_123 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_123 = G_B_treat_123 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_123 = F_E_treat_123 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_123 = F_B_treat_123 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_123 = E_B_treat_123 + [Treat_rates[i][29] for i in range(n_images)]

for batch_num in [24,25,27]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    Check_rates = np.load('Rates_agreement/Check_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_457 = N_J_treat_457 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_457 = N_G_treat_457 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_457 = N_F_treat_457 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_457 = N_E_treat_457 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_457 = N_B_treat_457 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_457 = J_G_treat_457 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_457 = J_F_treat_457 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_457 = J_E_treat_457 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_457 = J_B_treat_457 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_457 = G_F_treat_457 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_457 = G_E_treat_457 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_457 = G_B_treat_457 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_457 = F_E_treat_457 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_457 = F_B_treat_457 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_457 = E_B_treat_457 + [Treat_rates[i][29] for i in range(n_images)]

for batch_num in [28,29,210]:
    Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
    Check_rates = np.load('Rates_agreement/Check_rates'+str(batch_num)+'.npy')
    n_images = len (Treat_rates)
#    print(n_images)
    N_J_treat_8910 = N_J_treat_8910 + [Treat_rates[i][1] for i in range(n_images)]
    N_G_treat_8910 = N_G_treat_8910 + [Treat_rates[i][2] for i in range(n_images)]
    N_F_treat_8910 = N_F_treat_8910 + [Treat_rates[i][3] for i in range(n_images)]
    N_E_treat_8910 = N_E_treat_8910 + [Treat_rates[i][4] for i in range(n_images)]
    N_B_treat_8910 = N_B_treat_8910 + [Treat_rates[i][5] for i in range(n_images)]

    J_G_treat_8910 = J_G_treat_8910 + [Treat_rates[i][8] for i in range(n_images)]
    J_F_treat_8910 = J_F_treat_8910 + [Treat_rates[i][9] for i in range(n_images)]
    J_E_treat_8910 = J_E_treat_8910 + [Treat_rates[i][10] for i in range(n_images)]
    J_B_treat_8910 = J_B_treat_8910 + [Treat_rates[i][11] for i in range(n_images)]

    G_F_treat_8910 = G_F_treat_8910 + [Treat_rates[i][15] for i in range(n_images)]
    G_E_treat_8910 = G_E_treat_8910 + [Treat_rates[i][16] for i in range(n_images)]
    G_B_treat_8910 = G_B_treat_8910 + [Treat_rates[i][17] for i in range(n_images)]

    F_E_treat_8910 = F_E_treat_8910 + [Treat_rates[i][22] for i in range(n_images)]
    F_B_treat_8910 = F_B_treat_8910 + [Treat_rates[i][23] for i in range(n_images)]

    E_B_treat_8910 = E_B_treat_8910 + [Treat_rates[i][29] for i in range(n_images)]
##########################
##########################
for batch_num in [21, 22, 23]:
    Treat_rates = np.load('Rates_agreement/Treat_rates' + str(batch_num) + '.npy')
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    n_images = len(Check_rates)
    #    print(n_images)
    N_J_check_123 = N_J_check_123 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_123 = N_G_check_123 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_123 = N_F_check_123 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_123 = N_E_check_123 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_123 = N_B_check_123 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_123 = J_G_check_123 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_123 = J_F_check_123 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_123 = J_E_check_123 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_123 = J_B_check_123 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_123 = G_F_check_123 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_123 = G_E_check_123 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_123 = G_B_check_123 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_123 = F_E_check_123 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_123 = F_B_check_123 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_123 = E_B_check_123 + [Check_rates[i][29] for i in range(n_images)]

for batch_num in [24, 25, 27]:
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    n_images = len(Check_rates)
    #    print(n_images)
    N_J_check_457 = N_J_check_457 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_457 = N_G_check_457 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_457 = N_F_check_457 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_457 = N_E_check_457 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_457 = N_B_check_457 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_457 = J_G_check_457 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_457 = J_F_check_457 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_457 = J_E_check_457 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_457 = J_B_check_457 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_457 = G_F_check_457 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_457 = G_E_check_457 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_457 = G_B_check_457 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_457 = F_E_check_457 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_457 = F_B_check_457 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_457 = E_B_check_457 + [Check_rates[i][29] for i in range(n_images)]

for batch_num in [28, 29, 210]:
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    Check_rates = np.load('Rates_agreement/Check_rates' + str(batch_num) + '.npy')
    n_images = len(Check_rates)
    #    print(n_images)
    N_J_check_8910 = N_J_check_8910 + [Check_rates[i][1] for i in range(n_images)]
    N_G_check_8910 = N_G_check_8910 + [Check_rates[i][2] for i in range(n_images)]
    N_F_check_8910 = N_F_check_8910 + [Check_rates[i][3] for i in range(n_images)]
    N_E_check_8910 = N_E_check_8910 + [Check_rates[i][4] for i in range(n_images)]
    N_B_check_8910 = N_B_check_8910 + [Check_rates[i][5] for i in range(n_images)]

    J_G_check_8910 = J_G_check_8910 + [Check_rates[i][8] for i in range(n_images)]
    J_F_check_8910 = J_F_check_8910 + [Check_rates[i][9] for i in range(n_images)]
    J_E_check_8910 = J_E_check_8910 + [Check_rates[i][10] for i in range(n_images)]
    J_B_check_8910 = J_B_check_8910 + [Check_rates[i][11] for i in range(n_images)]

    G_F_check_8910 = G_F_check_8910 + [Check_rates[i][15] for i in range(n_images)]
    G_E_check_8910 = G_E_check_8910 + [Check_rates[i][16] for i in range(n_images)]
    G_B_check_8910 = G_B_check_8910 + [Check_rates[i][17] for i in range(n_images)]

    F_E_check_8910 = F_E_check_8910 + [Check_rates[i][22] for i in range(n_images)]
    F_B_check_8910 = F_B_check_8910 + [Check_rates[i][23] for i in range(n_images)]

    E_B_check_8910 = E_B_check_8910 + [Check_rates[i][29] for i in range(n_images)]
##################
#################
for batch_num in [21, 22, 23]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    #    print(n_images)
    N_J_merge_123 = N_J_merge_123 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_123 = N_G_merge_123 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_123 = N_F_merge_123 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_123 = N_E_merge_123 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_123 = N_B_merge_123 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_123 = J_G_merge_123 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_123 = J_F_merge_123 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_123 = J_E_merge_123 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_123 = J_B_merge_123 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_123 = G_F_merge_123 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_123 = G_E_merge_123 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_123 = G_B_merge_123 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_123 = F_E_merge_123 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_123 = F_B_merge_123 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_123 = E_B_merge_123 + [Merge_rates[i][29] for i in range(n_images)]

for batch_num in [24, 25, 27]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    #    print(n_images)
    N_J_merge_457 = N_J_merge_457 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_457 = N_G_merge_457 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_457 = N_F_merge_457 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_457 = N_E_merge_457 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_457 = N_B_merge_457 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_457 = J_G_merge_457 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_457 = J_F_merge_457 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_457 = J_E_merge_457 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_457 = J_B_merge_457 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_457 = G_F_merge_457 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_457 = G_E_merge_457 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_457 = G_B_merge_457 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_457 = F_E_merge_457 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_457 = F_B_merge_457 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_457 = E_B_merge_457 + [Merge_rates[i][29] for i in range(n_images)]

for batch_num in [28, 29, 210]:
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    Merge_rates = np.load('Rates_agreement/Merge_rates' + str(batch_num) + '.npy')
    n_images = len(Merge_rates)
    #    print(n_images)
    N_J_merge_8910 = N_J_merge_8910 + [Merge_rates[i][1] for i in range(n_images)]
    N_G_merge_8910 = N_G_merge_8910 + [Merge_rates[i][2] for i in range(n_images)]
    N_F_merge_8910 = N_F_merge_8910 + [Merge_rates[i][3] for i in range(n_images)]
    N_E_merge_8910 = N_E_merge_8910 + [Merge_rates[i][4] for i in range(n_images)]
    N_B_merge_8910 = N_B_merge_8910 + [Merge_rates[i][5] for i in range(n_images)]

    J_G_merge_8910 = J_G_merge_8910 + [Merge_rates[i][8] for i in range(n_images)]
    J_F_merge_8910 = J_F_merge_8910 + [Merge_rates[i][9] for i in range(n_images)]
    J_E_merge_8910 = J_E_merge_8910 + [Merge_rates[i][10] for i in range(n_images)]
    J_B_merge_8910 = J_B_merge_8910 + [Merge_rates[i][11] for i in range(n_images)]

    G_F_merge_8910 = G_F_merge_8910 + [Merge_rates[i][15] for i in range(n_images)]
    G_E_merge_8910 = G_E_merge_8910 + [Merge_rates[i][16] for i in range(n_images)]
    G_B_merge_8910 = G_B_merge_8910 + [Merge_rates[i][17] for i in range(n_images)]

    F_E_merge_8910 = F_E_merge_8910 + [Merge_rates[i][22] for i in range(n_images)]
    F_B_merge_8910 = F_B_merge_8910 + [Merge_rates[i][23] for i in range(n_images)]

    E_B_merge_8910 = E_B_merge_8910 + [Merge_rates[i][29] for i in range(n_images)]
##################
##################
from scipy.stats import mannwhitneyu, wilcoxon


def remove_0_100(my_list):
    filtered_list = [x for x in my_list if x != 0 or x!=100]
    return filtered_list


# Mann-Whitney U test
# We specify alternative='less' to test if the second  > first
statistic, p_value = mannwhitneyu(remove_0_100(G_E_treat_123), remove_0_100(G_E_treat_457), alternative= 'less' )
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_0_100(G_E_check_123), remove_0_100(G_E_check_457), alternative='less')
print(f"P-value: {p_value}")
statistic, p_value = mannwhitneyu(remove_0_100(G_E_merge_123), remove_0_100(G_E_merge_457), alternative='less')
print(f"P-value: {p_value}")


from scipy.stats import brunnermunzel
statistic, p_value = brunnermunzel(remove_0_100(G_E_treat_123), remove_0_100(G_E_treat_457))
print(p_value)
statistic, p_value = brunnermunzel(remove_0_100(G_E_check_123), remove_0_100(G_E_check_457))
print(p_value)
statistic, p_value = brunnermunzel(remove_0_100(G_E_merge_123), remove_0_100(G_E_merge_457))
print(p_value)

