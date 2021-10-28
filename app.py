# imports open sources librairies
from datetime import datetime
import time
import re
import pandas as pd
import numpy as np
import cv2
import os
import streamlit as st
from streamlit_webrtc import VideoTransformerBase, webrtc_streamer
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import imutils
import hashlib
import sqlite3 
import logging
import chime

# local imports
import config
from Security.hashing import make_hashes, check_hashes
from DB_Management.DB_Mongo import load_mongodb_Mask_Detector
from DB_Management.DB_SQLite import createUsersTable, createPicturesTable, checkUserName, insert_userdata, insert_picturedata, login_user, view_all_users, view_all_pictures
from Style.styles import set_style
from Models.to_load_models import load_cnn_model, load_face_detector_and_model
from Webcam_Video_Management.VideoTransformer import  get_masks, VideoTransformer
#from email_log import send_mail

# in case of depreciations advertisement
st.set_option('deprecation.showfileUploaderEncoding', False)


# to save the logs  # log connection
import logging
from imp import reload
reload(logging)
LOG_FILENAME = r'tmp/app.log'


logging.basicConfig(filename=LOG_FILENAME ,level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')
logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')


#logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
#logging.basicConfig(filename='app.log', encoding='utf-8', level=logging.DEBUG)
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='/tmp/app.log', filemode='w')
#logging.basicConfig(level=logging.DEBUG, filename='app.log')
#logging.basicConfig(filename='tmp/app.log', encoding='utf-8', filemode='w', level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
#logging.debug("You'll retrieve this message into the log file named app.log in the tmp folder")


def main():
    set_style('css/styles.css')
    st.title("Application de détection du masque")
    st.sidebar.subheader("Connectez-vous ou inscrivez-vous ici")
    menu = ["Connexion","Inscription"]
    choice = st.sidebar.selectbox("Menu",menu)

    if choice == "Connexion":

        username = st.sidebar.text_input("Nom d'utilisateur")
        password = st.sidebar.text_input("Mot de passe",type='password')

        # user's connection
        login_checkbox = st.sidebar.checkbox("Login")
        if login_checkbox:
            createUsersTable()
            hashed_pswd = make_hashes(password)
            result = login_user(username,check_hashes(password,hashed_pswd))

            if result:
                st.sidebar.success("Connecté en tant que {}".format(username))

                if username == config.super_login and password == config.super_pwd:
                    # log superconnection
                    logging.info("The Admin user is connected.")

                    # if st.button("Envoi des logs"):


                    #     toaddr = st.text_input("Entrer l'adresse email du destinataire des logs : ")
                    #     match = re.findall(r'[\w\.-]+@[\w\.-]+', toaddr)
                        
                    #     if match != None:
                    #         st.write(toaddr)
                    #         #sendmail(toaddr)
                    #         time.sleep(3)
                    #         st.success("Les logs ont bien été envoyés.")
                        # query = st.text_input("Entrez votre requête")
                        
                        # # filled query
                        # if query:
                        #     #logging.basicConfig(filename='tmp/app.log', encoding='utf-8', level=logging.DEBUG)
                        #     logging.info("The Admin user queried the SQLite database.")
                        #     conn = sqlite3.connect('data.db',check_same_thread=False)
                        #     c = conn.cursor()
                        #     c.execute(f"{query}")
                        #     #conn.commit()
                        #     data = c.fetchall()
                        #     clean_db = pd.DataFrame(data,columns=["Username","Insertion_date"])
                        #     st.dataframe(clean_db)
                        #     st.write(data)

                    if st.button("Voir la liste des utilisateurs ↓"):
                        # log view user exec
                        user_result = view_all_users()
                        clean_db = pd.DataFrame(user_result,columns=["Username","Insertion_date", "id_user"])
                        st.dataframe(clean_db)
                    if st.button("Voir la liste des photos de profil"):
                        pictures_result=view_all_pictures()
                        clean_db = pd.DataFrame(pictures_result,columns=["id_picture","BytesIO"])
                        st.dataframe(clean_db)

                task = st.selectbox("Tâches",["Détecteur de masque sur une photo","Webcam","Extraits de la base de données"])

                if task == "Détecteur de masque sur une photo":
                    st.write("← Chargez votre image dans la barre latérale")
                    st.sidebar.markdown('# Détecteur de masque')

                    logging.info("Model loading")                    
                    faceDetector = load_face_detector_and_model()
                    model = load_cnn_model()

                    logging.info("Model loaded")
                    uploaded_image = st.sidebar.file_uploader("Choisissez un fichier JPG", type=["jpg", "png", "jpeg"])
                    confidence_value = 0.8
                    logging.info("The confidence value is fixed at 0.80.")
                    if uploaded_image:

                        logging.info("Image loaded.")
                        st.sidebar.info('Image chargée :')
                        st.sidebar.image(uploaded_image, width=240)
                        image = cv2.imdecode(np.fromstring(uploaded_image.read(), np.uint8), 1)
                        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                        copy = image.copy()
                        (h, w) = image.shape[:2]
                        blob = cv2.dnn.blobFromImage(image, 1.0, (300, 300),
                                                     (104.0, 177.0, 123.0))
                        faceDetector.setInput(blob)
                        detections = faceDetector.forward()
                        #logging.basicConfig(filename='tmp/app.log', encoding='utf-8', level=logging.DEBUG)
                        if detections.shape[0]==1:
                            logging.info(f"The model detected {detections.shape[0]} face.")
                        else:
                            logging.info(f"The model detected {detections.shape[0]} faces.")

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
                                #logging.basicConfig(filename='tmp/app.log', encoding='utf-8', level=logging.DEBUG)
                                logging.info("The Mask_Detector prediction coming.")
                                predicted_class = 0
                                label = "Pas de Masque"
                                if mask > withoutMask:
                                    label = "Masque"
                                    predicted_class = 1
                                    logging.info(f"One mask detected.")

                                color = (255, 0, 255) if label == "Pas de Masque" else (0, 255, 0)
                                label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)
                                cv2.putText(image, label, (startX, startY - 10),
                                            cv2.FONT_HERSHEY_SIMPLEX, 0.42, color, 2)
                                cv2.rectangle(image, (startX, startY), (endX, endY), color, 2)
                                st.image(image, width=640)
                                st.write('### ' + label)

                                logging.info(f"The model detected the {label} label for this face.")


                elif task == "Webcam":
                    st.markdown('<h2 align="center">Détection depuis la Webcam</h2>', unsafe_allow_html=True)
                    webrtc_streamer(key="detection", video_transformer_factory=VideoTransformer)

                    logging.info("The Webcam Streamlit Component is opened in the application.")


                elif task == "Extraits de la base de données":
                    #st.write("Choisissez un nombre :")
                    #choice = st.slider("2nd", 0,100, value=100)
                    #st.write(type(choice))

                    #client = client_mongodb()
                    training=load_mongodb_Mask_Detector()
                    # mydb = client["Mask_Detector"]
                    # training = mydb["training"]

                    logging.info("The MongoDB database {mydb} is loaded.")
                    logging.info("The application is connected to the training collection: {training} hosted by MongoDB.")

                    df = pd.DataFrame(list(training.find()))
                    if st.button(f"Afficher la base de données d'entraînement"):
                        #st.write(len(df))
                        st.dataframe(df)
                        logging.info(f"The user {username} clicked on 'Afficher la base de données d'entraînement' to show the usersTable")

            else:
                st.warning("Incorrect Username/Password")

                logging.debug("The user entered wrong Username/Password couple.")




    elif choice == "Inscription":


        st.subheader("Création d'un nouveau compte")
        new_user = st.text_input("Nom d'utilisateur")
        new_password = st.text_input("Mot de passe",type='password')
        uploaded_image = st.file_uploader("Choisissez un fichier JPG", type=["jpg", "png", "jpeg"])
        # encode upladed_newpp


        #new_user_id
        st.image(uploaded_image, width=240)

        logging.info(f"The user {new_user} is completed the inscription form.")


        if st.button("Inscrivez-vous ici"):
            # uploaded_pp = st.file_uploader("Choisissez un fichier JPG", type=["jpg", "png", "jpeg"])
            # st.image(uploaded_pp, width=240)
            createUsersTable()
            createPicturesTable()
            # if checkUserName(new_user)!=0:
            #     st.info("Please enter another username this one is already taken.")
            now = datetime.utcnow()
            # checkUserName(new_user)
            # if len(checkUserName(new_user))== False:
            #     st.warning("Votre nom d'utilisateur est déjà utilisé. Choisissez en un autre.")
            # else:
            # insert_userdata(new_user,make_hashes(new_password),now)

            #insert_picturedata("/home/jasminelabeille/Bureau/MaskWearingOrNot/DB_Management/Gay.png")
            #insert_picturedata("/home/jasminelabeille/Bureau/MaskWearingOrNot/DB_Management/Vasi.JPG")


            insert_userdata(new_user,make_hashes(new_password),now)
            if len([uploaded_image]) !=0:
                insert_picturedata(uploaded_image)

            st.success("Bravo ! Votre compte utilisateur est valide")
            st.info("Rendez-vous dans le menu de gauche pour vous connecter.")



if __name__ == '__main__':
    main()
