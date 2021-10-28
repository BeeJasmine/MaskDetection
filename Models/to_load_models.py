import os
import cv2
from tensorflow.keras.models import load_model


def load_cnn_model():
    """Method loading the model for mask detection on faces"""
    cnn_model = load_model("mask_detector.model")

    return cnn_model

def load_face_detector_and_model():

    prototxt_path = os.path.sep.join(["face_detector", "deploy.prototxt"])
    weights_path = os.path.sep.join(["face_detector",
                                    "res10_300x300_ssd_iter_140000.caffemodel"])
    cnn_net = cv2.dnn.readNet(prototxt_path, weights_path)

    return cnn_net