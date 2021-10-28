# filename = input("filename:")

# import smtplib, ssl

# port = 465  # For SSL
# password = input("Type your password and press enter: ")

# # Create a secure SSL context
# context = ssl.create_default_context()

# with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
#     server.login("my@gmail.com", password)
#     # TODO: Send email here



# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.base import MIMEBase
# from email import encoders
# #import streamlit as st 


# def sendmail(toaddr):
#     fromaddr = "abeille.beta.testeuse@gmail.com"
#     #toaddr = st.text_input("Enter The Email Adress You want to send to: ")
       
#     # instance of MIMEMultipart
#     msg = MIMEMultipart()
      
#     # storing the senders email address  
#     msg['From'] = fromaddr
      
#     # storing the receivers email address 
#     msg['To'] = toaddr
      
#     # storing the subject 
#     msg['Subject'] = "Logs"
#     # string to store the body of the mail
#     body = "Find the log file of the Mask Detector App in the attached file"
      
#     # attach the body with the msg instance
#     msg.attach(MIMEText(body, 'plain'))
      
#     # open the file to be sent 
#     filename = "tmp/app.log"
#     attachment = open(filename, "rb")
      
#     # instance of MIMEBase and named as p
#     p = MIMEBase('application', 'octet-stream')
      
#     # To change the payload into encoded form
#     p.set_payload((attachment).read())
      
#     # encode into base64
#     encoders.encode_base64(p)
       
#     p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      
#     # attach the instance 'p' to instance 'msg'
#     msg.attach(p)
      
#     # creates SMTP session
#     s = smtplib.SMTP('smtp.gmail.com', 587)
      
#     # start TLS for security
#     s.starttls()
      
#     # Authentication
#     s.login(fromaddr, "1Ab3ille!")
      
#     # Converts the Multipart msg into a string
#     text = msg.as_string()
      
#     # sending the mail
#     s.sendmail(fromaddr, toaddr, text)
      
#     # terminating the session
#     s.quit()

# toaddr = st.text_input("Enter the email adress you want to send to: ")
# sendmail(toaddr)