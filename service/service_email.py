from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib


def fmtp_server(msg):
    PASSWORD = "qdkpvssijqftpify"
    EMAIL = "tobias.aditya@gmail.com"
    #create server
    server = smtplib.SMTP('smtp.gmail.com: 587')
    server.starttls()
    
    # Login Credentials for sending the mail
    server.login(EMAIL, PASSWORD)
    
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()

def email(receiver:str,otp:str):
    # create message object instance
    msg = MIMEMultipart()

    # setup the parameters of the message
   
    msg['From'] = "tobias.aditya@gmail.com"
    msg['To'] = receiver
    msg['Subject'] = "Account Activation"
    
    # add in the message body
    msg.attach(MIMEText(f"OTP = {otp}", 'plain'))

    # with open(request.attachment, 'rb') as f:
    #     lampiran = f.read()

    # file_name = request.attachment.split('/')[-1]
    
    # #Add attachment
    # msg.attach(MIMEApplication(lampiran, Name=file_name))
    
    #Send using ftmp
    fmtp_server(msg)