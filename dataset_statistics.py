import os
import cv2

def count_figures_in_masks(folder_path):
    """
    Counts the number of distinct figures (connected components) in each mask file in a folder.

    Args:
        folder_path (str): Path to the folder containing mask files.

    Returns:
        dict: A dictionary mapping file names to the number of figures in each mask.
    """
    figures_count = {}
    total_figures = 0
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        #if filename in os.listdir('/data/projects/IncisionDeepLab/input/incision/orig_data4/test_images')  :
        if True:
            file_path = os.path.join(folder_path, filename)

            # Load the mask image in grayscale
            mask = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)

            # Find connected components
            num_labels, _ = cv2.connectedComponents(mask)

            # Subtract 1 to ignore the background label (0)
            figures = num_labels - 1
            figures_count[filename] = figures
            total_figures+=figures
    return figures_count, total_figures

#_,t = count_figures_in_masks('/data/DATA/incision/23/mask/Check')
_,t = count_figures_in_masks('/data/DATA/incision/4/mask/Treat')

print(t)