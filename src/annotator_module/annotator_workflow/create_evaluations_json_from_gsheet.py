'''
To create the evaluation_json file it uses the 'tagged_info'
Args:
    start_row: define the row nul in gsheet
    end_row: define the row num in g_sheet
'''

# Define the range of rows to read (e.g., rows 30 to 310)
start_row = 314
end_row = 320
frame_col = 1   # Column index for 'video nale' (A = 1, B = 2, etc.)
index_col = 6   # Column index for 'annotated frames'
import pygsheets, re
# Authenticate and connect to Google Sheets
gc = pygsheets.authorize(service_account_file='../../../data/keycode/my-gpysheets-3d8d13442005.json')  # Use your credentials file
# Open the Google Sheet
spreadsheet = gc.open_by_key('1cflPYtcE0J2K92iTiNixPUvAsGM4aeGEhBIhCSojcGQ')  # Replace with your sheet name
# Select the first worksheet
worksheet = spreadsheet[1]

# Fetch data from the sheet
frames = worksheet.get_values(start=(start_row, frame_col), end=(end_row, frame_col))
indexes = worksheet.get_values(start=(start_row, index_col), end=(end_row, index_col))
# Populate the dictionary
data = {'evals': []}
for frame, index in zip(frames, indexes):
    # Extract the number from the [num] format
    num = re.search(r'\[(\d+)\]', index[0])  # Matches the number inside square brackets
    if num:
        incremented_index = [int(num.group(1))]  # Increment the number and wrap it in a list
    else:
        incremented_index = None  # Default to an empty list if no valid index is found

    # Append to the dictionary
    data['evals'].append({'frame': frame[0], 'index': incremented_index})
# save the populated dictionary
import json
json_object = json.dumps(data, indent=4)
batch_num = '15'
# Writing to .json
with open('../../../data/Evaluations_json/'+'Evaluation' + str(batch_num) + '.json', 'w') as outfile:
    outfile.write(json_object)