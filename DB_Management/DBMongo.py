import pymongo


def client_mongodb():

	# TO DO: create username & pwd via MongoDBAtlas
    client = pymongo.MongoClient('localhost',27017)

    return client


    # client = get_client_mongodb()
    # mydb = client["Mask_Detector"]
    # w_mask = mydb["w_mask_collection"]
    # wo_mask = mydb["w_mask_collection"]

    # df_w = pd.DataFrame(list(w_mask.find()))
    # df_wo = pd.DataFrame(list(wo_mask.find()))

    # logging.info("Voici la base de données contenant l'ensemble des données. Pour la voir, appuyez sur le bouton 'Afficher la base de données'")

    # if st.button("Afficher la base de données d'entraînement"):
    #     st.dataframe(Dat)
    #     st.dataframe(Dat)

    # client = pymongo.MongoClient('localhost',27017)
    # mydb = client["Mask_Detector"]
    # w_mask = mydb["w_mask_collection"]
    # wo_mask = mydb["w_mask_collection"]




        # if username == config.super_login and password == config.super_pwd:
        # st.subheader("Base de données Utilisateurs")
        # if st.button("Base de données"):
        #     st.write(admin())