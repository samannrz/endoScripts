import re

import pygsheets

# Authenticate and connect to Google Sheets
gc = pygsheets.authorize(service_account_file='keycode/my-gpysheets-3d8d13442005.json')  # Use your credentials file

# Open the Google Sheet by title or URL
spreadsheet = gc.open_by_key('1cflPYtcE0J2K92iTiNixPUvAsGM4aeGEhBIhCSojcGQ')  # Replace with your sheet name

# Select the first worksheet (you can also use index or name)
worksheet = spreadsheet[1]

# Define the range of rows to read (e.g., rows S to E)
start_row = 274  # Row S (adjust for your data)
end_row = 304    # Row E (adjust for your data)
frame_col = 1   # Column index for 'frame' (A = 1, B = 2, etc.)
index_col = 6   # Column index for 'index' (adjust for your data)

# Fetch data from the sheet
frames = worksheet.get_values(start=(start_row, frame_col), end=(end_row, frame_col))
indexes = worksheet.get_values(start=(start_row, index_col), end=(end_row, index_col))
# Populate the dictionary
data = {'evals': []}
for frame, index in zip(frames, indexes):
    # Extract the number from the [num] format
    num = re.search(r'\[(\d+)\]', index[0])  # Matches the number inside square brackets
    extracted_index = int(num.group(1))  if num else None  # Increment the number by 1

    # Append to the dictionary
    data['evals'].append({'frame': frame[0], 'index': extracted_index})

# save the populated dictionary
import json

json_object = json.dumps(data, indent=4)
batch_num = '212'
# Writing to sample.json
with open('Evaluations_json/'+'Evaluation' + str(batch_num) + '.json', 'w') as outfile:
    outfile.write(json_object)