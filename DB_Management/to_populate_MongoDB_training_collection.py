import os
import cv2
import pandas as pd
import pymongo
import math


client = pymongo.MongoClient('localhost',27017)
mydb = client["Mask_Detector"]

# 2 path pour 2 label differents dans la collection training 
path_w="/home/jasminelabeille/Bureau/data/w"
path_wo="/home/jasminelabeille/Bureau/data/wo"
training = mydb["training"]


listfold = os.listdir(path_wo)

for i in range(len(listfold)):
        for file in listfold[0:49]:
            print('insert')
            print(file)
            print(path_wo+"/"+file)
            im=cv2.imread(path_wo+"/"+file)
            print(im.shape)
            im_resize=cv2.resize(im, (500,500))
            is_ok, im_bystr_arr = cv2.imencode(file, im_resize)
            byte_im=im_bystr_arr.tobytes()
            label=0
            text_label="wo_masks"
            data = []
            data.append ({"dossier":f"{path_wo}/{file}", "image":file, "label":"wo_mask","ByteStringIO":byte_im, "image":file, "label":label, "text_label":text_label})
            training.insert_many(data)
            print('done')
            
            
            
listfold = os.listdir(path_w)

for i in range(len(listfold)):
        for file in listfold[0:49]:
            print('insert')
            print(file)
            print(path_w+"/"+file)
            im=cv2.imread(path_w+"/"+file)
            print(im.shape)
            im_resize=cv2.resize(im, (500,500))
            is_ok, im_bystr_arr = cv2.imencode(file, im_resize)
            byte_im=im_bystr_arr.tobytes()
            label=1
            text_label="w_masks"
            data = []
            data.append ({"dossier":f"{path_w}/{file}", "image":file, "label":"w_mask","ByteStringIO":byte_im, "image":file, "label":label, "text_label":text_label})
            training.insert_many(data)
            print('done')