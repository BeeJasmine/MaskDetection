from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input


import cv2
import os
import numpy as np




def load_cnn_model():
    """Method loading the model for mask detection on faces"""
    cnn_model = load_model("mask_detector.model")
    return cnn_model

def load_face_detector_and_model():

    prototxt_path = os.path.sep.join(["face_detector", "deploy.prototxt"])
    weights_path = os.path.sep.join(["face_detector", "res10_300x300_ssd_iter_140000.caffemodel"])
    cnn_net = cv2.dnn.readNet(prototxt_path, weights_path)

    return cnn_net



def prediction(image_input):

	faceDetector = load_face_detector_and_model()
	model = load_cnn_model()
	confidence_value = 0.8
	img=open(image_input, 'rb')
	image = cv2.imdecode(np.frombuffer(img.read()), 1)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	(h, w) = image.shape[:2]
	blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
	                             (104.0, 177.0, 123.0))
	faceDetector.setInput(blob)
	detections = faceDetector.forward()

	for i in range(0, detections.shape[2]):
	    confidence = detections[0, 0, i, 2]
	    if confidence > confidence_value:
	        box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
	        (startX, startY, endX, endY) = box.astype("int")
	        (startX, startY) = (max(0, startX), max(0, startY))
	        (endX, endY) = (min(w - 1, endX), min(h - 1, endY))
	        face = image[startY:endY, startX:endX]
	        face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
	        face = cv2.resize(face, (224, 224))
	        face = img_to_array(face)
	        face = preprocess_input(face)
	        expanded_face = np.expand_dims(face, axis=0)
	        (mask, withoutMask) = model.predict(expanded_face)[0]
	        predicted_class = 0
	        label = "Pas de Masque"
	        if mask > withoutMask:
	            label = "Masque"
	            predicted_class = 1
	            return "Masque détecté"
	        else:
	        	return "Pas de masque"


image_input="Demo/images/nohossat.jpeg"

def test_prediction():
    print("\nInput = Masque. Output =", prediction(image_input))
    assert prediction(image_input) == "Masque détecté"