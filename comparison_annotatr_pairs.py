import numpy as np
from matplotlib import pyplot as plt

batch_num = 21
nb_ann = 6
NAME_LIST = ['Nicolas', 'Jean', 'Giuseppe', 'Filippo', 'Ervin', 'Ebbe']
Treat_rates = np.load('Rates_agreement/Treat_rates'+str(batch_num)+'.npy')
Check_rates = np.load('Rates_agreement/Check_rates'+str(batch_num)+'.npy')
#print(Treat_rates)

###################################################
### The Agreement Matrices between all annotators #####
###################################################
Treat_matrix_flat = np.mean(Treat_rates, axis=0)
Treat_matrix = Treat_matrix_flat.reshape(nb_ann, nb_ann)

Check_matrix_flat = np.mean(Check_rates, axis=0)
Check_matrix = Check_matrix_flat.reshape(nb_ann, nb_ann)
##################
Treat_matrix = np.tril(Treat_matrix)
# Create a figure and axis
fig, ax = plt.subplots()
# Create a heatmap with a custom color map
cax = ax.matshow(Treat_matrix, cmap='coolwarm', origin='lower')
# Add a color bar
cbar = plt.colorbar(cax)
# Add grid lines
ax.set_xticks(np.arange(Treat_matrix.shape[1]), minor=False)
ax.set_yticks(np.arange(Treat_matrix.shape[0]), minor=False)
ax.grid(which='minor', color='w', linestyle='-', linewidth=0)
# Set axis labels
ax.set_xticklabels(NAME_LIST)
ax.set_yticklabels(NAME_LIST)
for i in range(Treat_matrix.shape[0]):
    for j in range(Treat_matrix.shape[1]):
        if i > j:
            ax.text(j, i, str(round(Treat_matrix[i, j])), va='center', ha='center', color='black')

# Set title
plt.title('Pair-wise agreement rate')
# Show the plot
plt.savefig('Treat_rates' + str(batch_num) + '.png')
######################
Check_matrix = np.tril(Check_matrix)

# Create a figure and axis
fig, ax = plt.subplots()
# Create a heatmap with a custom color map
cax = ax.matshow(Check_matrix, cmap='coolwarm', origin='lower')
# Add a color bar
cbar = plt.colorbar(cax)
# Add grid lines
ax.set_xticks(np.arange(Check_matrix.shape[1]), minor=False)
ax.set_yticks(np.arange(Check_matrix.shape[0]), minor=False)
ax.grid(which='minor', color='w', linestyle='-', linewidth=0)
# Set axis labels
ax.set_xticklabels(NAME_LIST)
ax.set_yticklabels(NAME_LIST)
for i in range(Check_matrix.shape[0]):
    for j in range(Check_matrix.shape[1]):
        if i > j:
            ax.text(j, i, str(round(Check_matrix[i, j])), va='center', ha='center', color='black')

plt.title('Pair-wise agreement rate')
plt.savefig('Check_rates' + str(batch_num) + '.png')
