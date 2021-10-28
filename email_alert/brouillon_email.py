from mailer import Mailer
from mailer import Message

message = Message(From='abeille.beta.testeuse@gmail.com',
                  To=["jasmine.banchereau@gmail.com"],
                  Subject="Cute Cat")
message.Body = """Kittens with dynamite"""
message.attach("tmp/app.log")

sender = Mailer('abeille.beta.testeuse@gmail.com', '1Ab3ille!', 'smtp.gmail.com')
sender.send(message)





# import stmplib as s
# #from win32com.client import Dispatch
# import smtplib, ssl

# file=open('tmp/app.log')


# pip install mailer
# This Module Support Gmail & Microsoft Accounts (hotmail, outlook etc..)
# from mailer import Mailer

# mail = Mailer('abeille.beta.testeuse@gmail.com', '1Ab3ille!')

# mail.attach("picture.png", mimetype="tmp/app.log")

# mail.send(receiver='someone@example.com', subject='TEST', message='From Python!')

# "abeille.beta.testeuse@gmail.com""1Ab3ille!"

# insta: @9_tay