import pygsheets

sheet_id_JL = '1mnzXSZkhnKa67_aRjVHb8HvjZ3cH7rrakRfNUHsVS7o'
sheet_id_G = '1QErFg8OXCMLTS5DhEn-yvmHXigaDKAXhZV0OwAsCR_w'
gc = pygsheets.authorize(service_file='keycode/my-gpysheets-3d8d13442005.json')
sh = gc.open_by_key(sheet_id_G)
wks = sh.sheet1

script_lines = ''
i = 3
j = 1
video_name_new = wks.cell('A' + str(i)).value
while video_name_new:
    print(i, video_name_new)
    condition_passed = False
    start_time = wks.cell('B' + str(i)).value
    end_time = wks.cell('C' + str(i)).value
    if start_time.startswith('0') and not wks.cell('E' + str(i)).value:
        condition_passed = True
        script_lines = script_lines + 'ffmpeg -i /data/Videos/endodata/orig/' + video_name_new + ' -ss ' \
                       + start_time + ' -to ' + end_time + ' -c:v copy /data/Videos/endodata/sequ/' + video_name_new[
                                                                                                      :-4] \
                       + '_trim' + str(j) + video_name_new[-4:] + '\n'
    video_name_old = video_name_new
    i += 1
    video_name_new = wks.cell('A' + str(i)).value
    if video_name_new == video_name_old:
        if condition_passed:
            j += 1
    else:
        j = 1
        script_lines = script_lines + '\n'
#
# hh = 32
# while hh < 39:
#     wks.update_value('A' + str(hh), wks.cell('A' + str(hh)).value + '.VOB')
#     hh = hh + 1

print(script_lines)
with open('/data/Videos/endodata/extract_bash_G.sh', 'w') as f:
    f.write('#!/bin/sh\n')
    f.write(script_lines)
