import sqlite3
import cv2
import numpy as np
import io
import config
from PIL import Image

# DB Management
conn = sqlite3.connect('data.db',check_same_thread=False)
c = conn.cursor()


# DB  Functions

def createUsersTable():
    c.execute('CREATE TABLE IF NOT EXISTS usersTable(username TEXT, password TEXT, insertion_date TIMESTAMPS, id_user INTEGER PRIMARY KEY AUTOINCREMENT)')
    #c.execute('CREATE TABLE userstable(username TEXT,password TEXT, insertion_date TIMESTAMPS)')

def checkUserName(username):
    # If username exists already, return advertisement
    c.execute("SELECT COUNT(username) FROM userstable WHERE username = (?)", username)
    if len(c.fetchall()) == 0:
        return True


def insert_userdata(username,password, insertion_date):
    c.execute('INSERT INTO usersTable(username,password,insertion_date) VALUES (?,?,?)',(username,password, insertion_date))
    conn.commit()

def login_user(username,password):
    c.execute('SELECT * FROM usersTable WHERE username =? AND password = ?',(username,password))
    data = c.fetchall()
    return data


# # checkin the login
def login_user_log(username,password):
    check = login_user(username,verif(password,ha_pswd))
    if check:
        logging.info("{} acceed to the application".format(username))
    else:
        logging.error("Incorrect logins") 
    if check == []:
        return False
    else:
        return True

#test to check the test_login_user_message
def test_login_user_message():
    assert login_user_log(super_login, super_password) == False


def view_all_users():
    """ Method returning the usersTable """
    c.execute('SELECT username,insertion_date,id_user FROM usersTable')
    data = c.fetchall() 
    return data


def createUsersPicturesTable():
    c.execute('CREATE TABLE IF NOT EXISTS users_pictures(id_user INTEGER UNIQUE, id_picture INTEGER UNIQUE, id INTEGER AUTOINCREMENT PRIMARY KEY)')


def createPicturesTable():
    c.execute('CREATE TABLE IF NOT EXISTS picturesTable(id_picture INTEGER AUTOINCREMENT PRIMARY KEY , BytesIO TEXT)')



# def insert_picturedata(uploaded_pp):
#     image = cv2.imdecode(np.fromstring(uploaded_pp.read(), np.uint8), 1)
#     im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     im_resize=cv2.resize(im, (500,500))
    
#     is_ok, im_bystr_arr = cv2.imencode(uploaded_pp, im_resize)
#     bytes_im=im_bystr_arr.tobytes()
#     print(bytes_im)
#     #bytesIO.append(byte_im)
#     c.execute('INSERT INTO picturesTable(BytesIO) VALUES (?)',(bytes_im))
#     conn.commit()
#         # return 


def insert_picturedata(uploaded_pp):
    im = Image.open(uploaded_pp)
    im_resize = im.resize((500, 500))
    buf = io.BytesIO()
    #im_resize.save(buf, format='JPEG')
    bytes_im = buf.getvalue()
    c.execute('INSERT INTO picturesTable(BytesIO) VALUES (?)',([bytes_im]))
    conn.commit()

def view_all_pictures():
    """ Method returning the usersTable """
    c.execute('SELECT * FROM picturesTable')
    data = c.fetchall() 
    return data



# import io
# from PIL import Image

# im = Image.open(uploaded_pp)
# im_resize = im.resize((500, 500))
# buf = io.BytesIO()
# im_resize.save(buf, format='JPEG')
# byte_im = buf.getvalue()




# # This portion is part of my test code
# byteImgIO = io.BytesIO()
# byteImg = Image.open(uploaded_pp)
# byteImg.save(byteImgIO, "PNG")
# byteImgIO.seek(0)
# byteImg = byteImgIO.read()


# # Non test code
# dataBytesIO = io.BytesIO(byteImg)
# Image.open(dataBytesIO)