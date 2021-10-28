import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer

import pandas as pd
import numpy as np

from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import imutils
import cv2
import chime



from Models.to_load_models import load_cnn_model, load_face_detector_and_model

# to find faces predicted on the webcam  image taken
def get_masks(frame, faceNet, maskNet):
    (h, w) = frame.shape[:2]

    # resizing to prepare the entry of the face detection model for mean substraction
    # imageNet RGB mean values are respectively: 103.93 116.77 123.68
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),
                                 (104.0, 177.0, 123.0))
    faceNet.setInput(blob)
    
    # get the results
    detections = faceNet.forward()
    faces = []
    preds = []
    locs = []

    CONFIDENCE = 0.6

    # get confidence values for eache detection
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        st.write(confidence)
        
        # ensuring the confidence is greater than the minimum fixed
        if confidence > CONFIDENCE:
            
            # face detection 
            # need array object to obtain int
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            # selection of the pixels recognized as face
            face = frame[startY:endY, startX:endX]
            
            # set values in right order for MobileNetV2
            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            
            # resizing: the fine-tuned MobileNetV2 is taking 224*224images 
            face = cv2.resize(face, (224, 224))
            
            # convert to array 
            face = img_to_array(face)
            
            # method imported from keras to prepare the input
            face = preprocess_input(face)
            
            # list the matrixes & coordinates to predict in real time
            faces.append(face)
            locs.append((startX, startY, endX, endY))

    # run the mask's prediction for each 
    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        # same batch size than training
        preds = maskNet.predict(faces, batch_size=32)

    return (locs, preds)



class VideoTransformer(VideoTransformerBase):
    def transform(self, frame):
        
        frame = frame.to_ndarray(format="bgr24")
        frame = imutils.resize(frame, width=400)
        faceDetector = load_face_detector_and_model()

        # detect faces in the frame and determine if they are wearing a face mask or not
        (locs, preds) = get_masks(frame, faceDetector, load_model("mask_detector.model"))
        print('Mask wearing predictions')

        # loop over the detected faces coordinates to draw boxes 
        # zip method combines the two iterable (or more)
        for (box, pred) in zip(locs, preds):
            
            # locate each box
            (startX, startY, endX, endY) = box
            
            # the prediction for each class for each faces recognized w the get_masks function
            (mask, withoutMask) = pred
            print('loading predictions')

            # save class label and corresponding color
            label = "Mask" if mask > withoutMask else "No Mask"
            color = (0, 255, 0) if label == "Mask" else (0, 0, 255)
            # sound alert           
            if label != "Mask":
                chime.success()
            print('printing the mask detections')

            # draw the box w label on frame detected
            cv2.putText(frame, label, (startX, startY - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.38, color, 2)
            cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
            print('finishing process')

        return frame