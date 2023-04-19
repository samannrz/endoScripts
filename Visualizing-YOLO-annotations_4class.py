#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 12:19:17 2023

@author: mina
"""

from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
#code adapted from https://blog.paperspace.com/train-yolov5-custom-data/
def plot_bounding_box(image, annotation_list):
    annotations = np.array(annotation_list)
    w, h = image.size
    
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    
    try: 
        transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
        transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h 
    
        transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
        transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
        transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
        transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]
    except:
        transformed_annotations[[1,3]] = annotations[[1,3]] * w
        transformed_annotations[[2,4]] = annotations[[2,4]] * h 
    
        transformed_annotations[1] = transformed_annotations[1] - (transformed_annotations[3] / 2)
        transformed_annotations[2] = transformed_annotations[2] - (transformed_annotations[4] / 2)
        transformed_annotations[3] = transformed_annotations[1] + transformed_annotations[3]
        transformed_annotations[4] = transformed_annotations[2] + transformed_annotations[4]  
    
    class_color_dict = {
        0: "#ff0000", # class 0 is red
        1: "#FF82AB", # class 1 is green
        2: "#FF8247" , # class 2 is blue
        3: "#CDCD00"
    }
    
    legend = []
    
    for ann in transformed_annotations:
        try:
            obj_cls, x0, y0, x1, y1 = ann
            color = class_color_dict[int(obj_cls)]
            plotted_image.rectangle(((x0,y0), (x1,y1)), width = 10, outline=color)
            legend.append((int(obj_cls), color))
        
        except: 
            obj_cls= transformed_annotations[0]
            x0=transformed_annotations[1]
            y0=transformed_annotations[2]
            x1=transformed_annotations[3]
            y1=transformed_annotations[4]
            color = class_color_dict[int(obj_cls)]
            plotted_image.rectangle(((x0,y0), (x1,y1)), width = 10, outline=color)
            legend.append((int(obj_cls), color))
    

inputImgPath = "/home/mina/datasets/just3class/inputs/"
inputtxtPath = "/home/mina/datasets//mask_lesion/"
outputImgPath = "/home/mina/datasets/raw_lesion_2/"


ld = os.listdir(inputtxtPath)

for fileF in ld: 
    #get an annotation file
    annotation_file = inputtxtPath + fileF
    image_file = fileF.replace("txt", "png")
    #Get the corresponding image file
    #image_file = annotation_file.replace("txt", "png")
    #assert os.path.exists(image_file)
    #Load the image
    image = Image.open(inputImgPath + image_file)
    #Plot the Bounding Box
    plot_bounding_box(image, np.loadtxt(annotation_file))
    image.save(outputImgPath + image_file)