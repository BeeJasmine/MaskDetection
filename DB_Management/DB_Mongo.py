import pymongo

def load_mongodb_Mask_Detector():
    client = pymongo.MongoClient()
    mydb = client["Mask_Detector"]
    training = mydb["training"]
    return training




# def client_mongodb():
#     client = pymongo.MongoClient()
#     return client