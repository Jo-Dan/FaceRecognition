# -*- coding: utf-8 -*-
"""
Get Images and Labels for Face Recognition

Created on Tue Apr 12 16:00:47 2016

@author: Jo-dan
"""
import os
from PIL import Image
import numpy as np
import cv2

cascadepath = "haarcascade_frontalface_default.xml"
facecascade = cv2.CascadeClassifier(cascadepath)

def get_images_and_labels(path):
    #get all images and labels except "sad"
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    images = []
    labels = []
    for image_path in image_paths:
        #read and make grey
        image_pil = Image.open(image_path).convert('L')
        #convert img to numpy array
        image = np.array(image_pil, 'uint8')
        #get image label
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        #detect faces in image
        faces = facecascade.detectMultiScale(image)
        #if face detected append face to images and label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            cv2.imshow("Adding faces to training set...", image[y: y + h, x: x + w])
            cv2.waitKey(1)
    #return the images and labels lists
    return images, labels