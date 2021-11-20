# DETECTION VIA CLASSIFICATION FOR THE SURGERY MASKS WEARING ON FACES

During this COVID-19 crisis, wearing a mask is a necessity for public health. 
Controlling this pandemy propagation is an emergency since November 2019.

This front-end application is able to detect face masked or not. It could be used in any public area like public transport or either theater, cinema or shop. 


# Web Service 
A simple [Streamlit](https://www.streamlit.io/) frontend for face mask detection in images using a pre-trained [Keras](https://keras.io/) CNN model + [OpenCV](https://opencv.org/) and model interpretability.


# General info
It uses OpenCV to detect faces in the input images and a CNN as mask/no-mask binary classifier applied to the face ROI. The Deep Learning model currently used has the architecture suggested by Adrian Rosebrock [here](https://www.pyimagesearch.com/2020/05/04/covid-19-face-mask-detector-with-opencv-keras-tensorflow-and-deep-learning/) and has been trained using the image data set in the data folder. The trained model has been shared in this repo. The face detector algorithm comes from [here](https://github.com/Shiva486/facial_recognition): the Caffe model and its descriptor are into the *face_detector* directory.    


# Detection pipeline : 

Input : static or dynamic image of one or multiple people.

1/  Face Detector prediction from https://github.com/Shiva486/facial_recognition

2/  Mask detector applied on faces detected.

Output : annotated labelled image (with mask 1 or without_mask 0)
   


The mask detector was trained on a 10000 images balanced dataset. The model is based on  MobileNetV2. To learn more about the MobileNet Architecture [Click here (research paper)] (https://arxiv.org/pdf/1801.04381.pdf).


# Performances

MATRIX CONFUSION
ROC & AUC
Loss-accuracy plot

The model accuracy is 98% and the AUC is 91%.


# Command to run the application: 
$ Streamlit run app.py


# Command to populate the MongoDB:
``$ cd DB_Management
$ python to_populate_MongoDB_training_collection.py``



IMAGES

VIDEO 
Find an app demonstration in the /Demo/Video folder.


# Required packages 

    OpenCV
    Keras
    TensorFlow
    MobileNetV2
    Streamlit & Streamlit Webrtc



## Usage
After cloning this repository you need to create a virtual environment and install the application dependencies  
```pip install -r requirements.txt```  
Then you can execute the application through the *streamlit* command  
```streamlit run app.py```  



# Architecture 
[tree screenshot](Demo/images/tree.png)




# Improvement’s areas
Deployment on a Cloud Solution like Microsoft Azure
Keep improve the mask detector model performance, particularly on low quality images, or exposed to low luminescence


# Contact

For any questions, ping me on [Linkedin](https://www.linkedin.com/in/jasmine-banchereau-9a43a296/)!








