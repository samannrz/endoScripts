import cv2
from functions import extractFrame

# '/data/DATA/SMOKE/VID007.mp4'
frame = extractFrame('/data/DATA/SMOKE/SMOKE_Batch2_videos/GAT2_GY_20221110_010_VID007.VOB', 12005)
cv2.imwrite('/data/DATA/SMOKE/VID000007.bmp', frame)
