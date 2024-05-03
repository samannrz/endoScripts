import cv2

from metrics import *
from PIL import Image, ImageDraw, ImageFont
import os

mask_pred_path = '/data/DATA/Incision_predictions/test1-28_Deeplab_consensus_1-28_scheduler/mask/Treat/'
mask_gt_path = '/data/DATA/incision/4/mask/Treat/'

for filename in os.listdir(mask_pred_path):
    mask_pred_path2 = os.path.join(mask_pred_path[:-11], 'final', filename)
    mask_gt_path2 = os.path.join(mask_gt_path[:-11], 'final', filename)
    # Load images
    image_gt = Image.open(mask_gt_path2)
    image_pred = Image.open(mask_pred_path2)

    # height = max(image_gt.height, image_pred.height)
    height = image_gt.height

    # Create a blank image with the width of the two images combined and the height of the tallest image
    merged_width = image_gt.width + 10 + image_pred.width
    merged_image = Image.new("RGB", (merged_width, height + 40), color=(0, 100, 0))

    # Paste images onto the blank image
    merged_image.paste(image_gt, (0, 40))
    merged_image.paste(image_pred, (image_gt.width + 10, 40))

    mask_pred_path1 = os.path.join(mask_pred_path, filename)
    mask_gt_path1 = os.path.join(mask_gt_path, filename)
    mask_gt_cal = cv2.imread(mask_gt_path1, cv2.IMREAD_GRAYSCALE).astype(bool)
    mask_pred_cal = cv2.imread(mask_pred_path1, cv2.IMREAD_GRAYSCALE).astype(bool)

    a = compute_surface_distances(mask_gt_cal, mask_pred_cal, (1, 1))
    # NSD = compute_surface_dice_at_tolerance(a, tolerance_mm=100)
    NSD=(compute_NSD(mask_gt_cal, mask_pred_cal, 20, 100))
    DICE=(compute_dice_coefficient(mask_gt_cal, mask_pred_cal))
    IOU=(calculate_iou(mask_gt_cal, mask_pred_cal))
    # Draw text on the top
    draw = ImageDraw.Draw(merged_image)
    text = 'NSD:' + str(round(NSD, 2)) + ', ' + 'IOU:' + str(round(IOU, 2)) + ', ' + 'DICE:' + str(round(DICE, 2))
    font = ImageFont.truetype("arial.ttf", 30)  # Change the font and size as needed
    text_width, text_height = draw.textsize(text, font=font)
    text_position = ((merged_width - text_width) // 2, 00)
    draw.text(text_position, text, fill=(255, 255, 255), font=font)

    # Save the final image
    merged_image.save('metric-Results/' + filename)

