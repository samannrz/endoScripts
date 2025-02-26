import pygsheets

sheet_id = '11e7eDQZcPBAAgFsTG364kiMY7Jw8bftkvVUnbXVS7Zc'

gc = pygsheets.authorize(service_file='../../keycode/my-gpysheets-3d8d13442005.json')
sh = gc.open_by_key(sheet_id)
wks = sh[10]

script_lines = ''
i = 116
j = 1
video_num = wks.cell('D' + str(i)).value
video_name = wks.cell('C' + str(i)).value
video_name_full = video_name + '_' + video_num + '.mp4'
while i < 124:
    print(i, video_name_full)

    start_time = wks.cell('E' + str(i)).value
    end_time = wks.cell('F' + str(i)).value
    new_line = 'ffmpeg -i /data/Videos/endodata/orig/' + video_name_full + ' -ss ' \
                   + start_time + ' -to ' + end_time + ' -c:v copy /data/Videos/endodata/sequ/' + video_name_full[
                                                                                                  :-4] \
                   + '_trim' + str(j) + '.mp4' + '\n'  # video_name_new[-4:] or .mp4
    script_lines = script_lines + new_line
    print(new_line)
    i += 1
    video_num_new = wks.cell('D' + str(i)).value
    if video_num_new != '':
        video_num = video_num_new
        j = 1
    else:
        j += 1
    video_name_new = wks.cell('C' + str(i)).value

    if video_name_new != '':
        video_name = video_name_new
        script_lines = script_lines + '\n'
    video_name_full = video_name + '_' + video_num + '.mp4'

with open('extract_bash_WS10_CF_4.sh', 'w') as f:
    f.write('#!/bin/sh\n')
    f.write(script_lines)
