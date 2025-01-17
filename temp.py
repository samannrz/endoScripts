import os

def find_missing_file(folder1, folder2):
    """
    Finds the file(s) present in folder1 but missing in folder2.

    Args:
        folder1 (str): Path to the first folder (reference folder).
        folder2 (str): Path to the second folder (to be compared).

    Returns:
        list: A list of filenames present in folder1 but missing in folder2.
    """
    # Get the list of filenames in both folders
    files_in_folder1 = set(os.listdir(folder1))
    files_in_folder2 = set(os.listdir(folder2))

    # Find files in folder1 that are not in folder2
    missing_files = list(files_in_folder1 - files_in_folder2)
    return missing_files

# Example usage
folder1 = "/data/projects/IncisionDeepLab/input/incision/orig_data4/valid_masks"  # Replace with the path to your first folder
folder2 = "/data/projects/IncisionDeepLab/input/incision/orig_data4/valid_images"  # Replace with the path to your second folder

missing_files = find_missing_file(folder1, folder2)

if missing_files:
    print("Missing files in folder2:")
    for file in missing_files:
        print(f"  {file}")
else:
    print("No files are missing in folder2.")
