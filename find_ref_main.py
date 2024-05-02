import os

images = os.listdir('annotationData26/image')
for image_name in images:
    with open("find_ref_all.py") as f:
        exec(f.read())