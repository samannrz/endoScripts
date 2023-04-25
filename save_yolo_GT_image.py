import os
import cv2

CLASSES_DICT = {
    'Adh Dense': 0, 'Adh Filmy': 1, 'Sup Black': 2, 'Sup White': 3,
    'Sup Red': 4, 'Sup Subtle': 5, 'Ov. Endometrioma': 6, 'Ov. Chocolate Fluid': 7, 'Deep Endometriosis': 8
}
image_path = '/data/projects/datasets/LesionDatasetImages'
label_path = '/data/projects/datasets/LesionLabelsYOLO'
NUM_TO_VISUALIZE = 20
detect_path = '/data/projects/yolov5/runs/detect/exp27/'


def find_key(num):
    for k, v in CLASSES_DICT.items():
        if int(v) == int(num):
            return k


def visualize_sample(image, annot_file):
    img_width = len(image[0])
    img_height = len(image)
    with open(annot_file) as f:
        box = [0] * 4
        for line in f:
            string = line.split(' ')
            label = find_key(string[0])
            width = float(string[3])
            height = float(string[4][:-1])
            xcenter = float(string[1])
            ycenter = float(string[2])
            box[0] = (xcenter - width / 2) * img_width
            box[1] = (ycenter - height / 2) * img_height
            box[2] = (xcenter + width / 2) * img_width
            box[3] = (ycenter + height / 2) * img_height
            cv2.rectangle(
                image,
                (int(box[0]), int(box[1])), (int(box[2]), int(box[3])),
                (255, 0, 0), 4
            )
            cv2.putText(
                image, label, (int(box[0]), int(box[1] - 5)),
                cv2.FONT_HERSHEY_SIMPLEX, .7, (255, 0, 0), 2
            )
        cv2.imwrite(detect_path + image_name, image)


images = os.listdir(detect_path)

for i in range(len(images)):
    image_name = images[i]
    visualize_sample(cv2.imread(os.path.join(detect_path, image_name)),
                     os.path.join(label_path, image_name[:-4] + '.txt'))
