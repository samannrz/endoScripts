import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Train', 'Evaluation', 'Test']
legends = ['Images', 'Treat Inst.', 'Check Inst.']
values = {
    'Images': [243, 20, 40],
    'Treat Inst.': [380, 49, 71],
    'Check Inst.': [527, 33, 61]
}
# values = {
#     'Images': [1781, 170, 40],
#     'Treat Inst.': [2456, 222, 71],
#     'Check Inst.': [3413, 363, 61]
# }

# Parameters for plot
x = np.arange(len(categories))  # the label locations
width = 0.25  # the width of the bars

# Create the figure and axes
fig, ax = plt.subplots(figsize=(8, 5))

# Plot each bar group
for i, legend in enumerate(legends):
    ax.bar(x + i * width, values[legend], width, label=legend)

# Customize the chart
#ax.set_xlabel('Categories')
ax.set_ylabel('Counts')
#ax.set_title('Data Distribution Across Categories')
ax.set_xticks(x + width)
ax.set_xticklabels(categories)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

# Save the figure as a PNG file
plt.tight_layout()

# Add grid and show plot
ax.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('dataSplit_consensus.png',dpi=300)
