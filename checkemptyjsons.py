import os
import json

# Set the directory that contains the JSON files
directory = '/media/saman/data/PycharmProjects/endoDetection/LesionDataset/LesionDataset'

# Iterate through all the files in the directory
for filename in os.listdir(directory):
    # Only consider files that have a .json extension
    if filename.endswith('.json'):
        # Load the JSON file
        with open(os.path.join(directory, filename), 'r') as f:
            data = json.load(f)

            # Check if the dictionary is empty
            if len(data['bb'])==0:
                os.remove(os.path.join(directory, filename))
                jpeg_file = filename.replace('.json', '.jpg')
                os.remove(os.path.join(directory, jpeg_file))
                print(filename + ' removed'+'\n')


